"""
Test Suite for Nutrition App
Run comprehensive tests on all modules.
"""

import unittest
import os
import sys
import tempfile
import json
from unittest.mock import Mock, patch, MagicMock

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import our modules
from pdf_parser import PDFParser
from llm_engine import LLMEngine
from chart_builder import ChartBuilder
from report_generator import ReportGenerator
import config


class TestPDFParser(unittest.TestCase):
    """Test cases for PDF Parser module."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sample_text = """
        HEALTH QUESTIONNAIRE
        Name: John Doe
        Age: 30
        Gender: Male
        Height: 6'0"
        Weight: 180 lbs
        
        Fitness Level: 6
        Energy Level: 7
        Motivation: 8
        
        Goals: lose weight, gain muscle
        Exercise History: I have been moderately active for 5 years
        """
        
    def test_personal_info_extraction(self):
        """Test extraction of personal information."""
        # Create a mock parser
        parser = PDFParser("dummy.pdf")
        
        # Test the text parsing method directly
        personal_info = parser._extract_personal_info(self.sample_text)
        
        self.assertEqual(personal_info.get("name"), "John Doe")
        self.assertEqual(personal_info.get("age"), "30")
        self.assertEqual(personal_info.get("gender"), "Male")
        
    def test_scale_responses_extraction(self):
        """Test extraction of scale responses."""
        parser = PDFParser("dummy.pdf")
        
        scale_responses = parser._extract_scale_responses(self.sample_text)
        
        self.assertEqual(scale_responses.get("fitness_level"), 6)
        self.assertEqual(scale_responses.get("energy_level"), 7)
        self.assertEqual(scale_responses.get("motivation"), 8)
        
    def test_fitness_goals_extraction(self):
        """Test extraction of fitness goals."""
        parser = PDFParser("dummy.pdf")
        
        goals = parser._extract_fitness_goals(self.sample_text)
        
        self.assertIn("lose weight", [g.replace("\\", "") for g in goals])
        self.assertIn("gain muscle", [g.replace("\\", "") for g in goals])


class TestLLMEngine(unittest.TestCase):
    """Test cases for LLM Engine module."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sample_data = {
            "personal_info": {"name": "John Doe", "age": "30"},
            "scale_responses": {"fitness_level": 6, "energy_level": 7},
            "fitness_goals": ["lose weight", "gain muscle"]
        }
        
    def test_prompt_building(self):
        """Test LLM prompt building."""
        engine = LLMEngine("openrouter", "dummy-key")
        
        summary_prompt = engine._build_summary_prompt(self.sample_data)
        training_prompt = engine._build_training_prompt(self.sample_data)
        nutrition_prompt = engine._build_nutrition_prompt(self.sample_data)
        
        # Check that prompts contain expected content
        self.assertIn("John Doe", summary_prompt)
        self.assertIn("fitness_level", summary_prompt)
        self.assertIn("training program", training_prompt.lower())
        self.assertIn("nutrition", nutrition_prompt.lower())
        
    def test_fallback_content(self):
        """Test fallback content generation."""
        engine = LLMEngine("openrouter", "dummy-key")
        
        summary_fallback = engine._get_fallback_content("summary_report")
        training_fallback = engine._get_fallback_content("training_plan")
        nutrition_fallback = engine._get_fallback_content("nutrition_plan")
        
        self.assertIn("SUMMARY REPORT", summary_fallback)
        self.assertIn("TRAINING PLAN", training_fallback)
        self.assertIn("NUTRITION PLAN", nutrition_fallback)


class TestChartBuilder(unittest.TestCase):
    """Test cases for Chart Builder module."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.chart_builder = ChartBuilder(self.temp_dir)
        self.sample_data = {
            "fitness_level": 6,
            "energy_level": 7,
            "strength": 5,
            "endurance": 4
        }
        
    def test_chart_builder_initialization(self):
        """Test chart builder initialization."""
        self.assertTrue(os.path.exists(self.temp_dir))
        
    def test_category_name_formatting(self):
        """Test category name formatting."""
        formatted = self.chart_builder._format_category_name("fitness_level")
        self.assertEqual(formatted, "Fitness Level")
        
        formatted = self.chart_builder._format_category_name("body_fat")
        self.assertEqual(formatted, "Body Fat %")
        
    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.subplots')
    def test_radar_chart_creation(self, mock_subplots, mock_savefig):
        """Test radar chart creation (mocked)."""
        # Mock matplotlib components
        mock_fig = Mock()
        mock_ax = Mock()
        mock_subplots.return_value = (mock_fig, mock_ax)
        
        output_path = os.path.join(self.temp_dir, "test_chart.png")
        
        result_path = self.chart_builder.build_radar_chart(
            self.sample_data, output_path
        )
        
        self.assertEqual(result_path, output_path)
        mock_savefig.assert_called_once()


class TestReportGenerator(unittest.TestCase):
    """Test cases for Report Generator module."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_templates = tempfile.mkdtemp()
        self.temp_output = tempfile.mkdtemp()
        self.report_gen = ReportGenerator(self.temp_templates, self.temp_output)
        
        self.sample_data = {
            "personal_info": {"name": "John Doe", "age": "30"},
            "scale_responses": {"fitness_level": 6},
            "fitness_goals": ["lose weight"],
            "dietary_preferences": {"restrictions": ["vegetarian"]},
            "health_metrics": {"bmi": "24.5"}
        }
        
        self.sample_content = {
            "summary": "Test summary content",
            "training": "Test training content",
            "nutrition": "Test nutrition content"
        }
        
    def test_report_generator_initialization(self):
        """Test report generator initialization."""
        self.assertTrue(os.path.exists(self.temp_templates))
        self.assertTrue(os.path.exists(self.temp_output))
        
    def test_timestamp_generation(self):
        """Test timestamp generation for file naming."""
        timestamp = self.report_gen._get_timestamp()
        self.assertIsInstance(timestamp, str)
        self.assertTrue(len(timestamp) > 0)
        
    @patch('docx.Document')
    def test_document_creation(self, mock_document):
        """Test document creation (mocked)."""
        # Mock Document class
        mock_doc = Mock()
        mock_document.return_value = mock_doc
        
        # Mock paragraph methods
        mock_paragraph = Mock()
        mock_run = Mock()
        mock_paragraph.add_run.return_value = mock_run
        mock_doc.add_paragraph.return_value = mock_paragraph
        
        # Test template loading
        doc = self.report_gen._load_or_create_template("test_template.docx")
        
        self.assertIsNotNone(doc)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete workflow."""
    
    def setUp(self):
        """Set up integration test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        
        # Sample questionnaire data
        self.questionnaire_data = {
            "personal_info": {
                "name": "Jane Smith",
                "age": "28",
                "gender": "Female",
                "height": "5'6\"",
                "weight": "140 lbs"
            },
            "scale_responses": {
                "fitness_level": 7,
                "energy_level": 8,
                "motivation": 9,
                "stress_management": 6
            },
            "fitness_goals": ["lose weight", "improve endurance"],
            "dietary_preferences": {
                "restrictions": ["gluten-free"],
                "allergies": ["shellfish"]
            },
            "health_metrics": {
                "bmi": "22.8",
                "activity_level": "moderate"
            },
            "checkboxes": {
                "equipment_available": ["dumbbells", "yoga mat"],
                "workout_times": ["morning"]
            }
        }
        
    def test_data_flow(self):
        """Test data flow between components."""
        # Test LLM Engine with sample data
        llm_engine = LLMEngine("openrouter", "dummy-key")
        
        # This should return fallback content since we don't have a real API key
        summary = llm_engine.generate_summary_report(self.questionnaire_data)
        training = llm_engine.generate_training_plan(self.questionnaire_data)
        nutrition = llm_engine.generate_nutrition_plan(self.questionnaire_data)
        
        self.assertIsInstance(summary, str)
        self.assertIsInstance(training, str)
        self.assertIsInstance(nutrition, str)
        self.assertTrue(len(summary) > 0)
        self.assertTrue(len(training) > 0)
        self.assertTrue(len(nutrition) > 0)
        
    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.subplots')
    def test_chart_integration(self, mock_subplots, mock_savefig):
        """Test chart generation integration."""
        # Mock matplotlib
        mock_fig = Mock()
        mock_ax = Mock()
        mock_subplots.return_value = (mock_fig, mock_ax)
        
        chart_builder = ChartBuilder(self.temp_dir)
        chart_path = os.path.join(self.temp_dir, "integration_test_chart.png")
        
        result = chart_builder.build_radar_chart(
            self.questionnaire_data["scale_responses"],
            chart_path,
            "Integration Test Chart"
        )
        
        self.assertEqual(result, chart_path)
        
    def test_config_loading(self):
        """Test configuration loading."""
        # Test that config values are accessible
        self.assertIsInstance(config.OUTPUT_DIR, str)
        self.assertIsInstance(config.TEMPLATES_DIR, str)
        self.assertIsInstance(config.WINDOW_TITLE, str)


class TestErrorHandling(unittest.TestCase):
    """Test error handling and edge cases."""
    
    def test_empty_data_handling(self):
        """Test handling of empty or invalid data."""
        # Test PDF parser with empty text
        parser = PDFParser("dummy.pdf")
        result = parser._extract_personal_info("")
        self.assertIsInstance(result, dict)
        
        # Test chart builder with empty data
        temp_dir = tempfile.mkdtemp()
        chart_builder = ChartBuilder(temp_dir)
        
        with patch('matplotlib.pyplot.savefig'):
            result = chart_builder.build_radar_chart({}, "empty_chart.png")
            self.assertIsInstance(result, str)
            
    def test_invalid_file_paths(self):
        """Test handling of invalid file paths."""
        # Test PDF parser with non-existent file
        parser = PDFParser("/invalid/path/to/file.pdf")
        
        with self.assertRaises(Exception):
            parser.parse()
            
    def test_api_error_handling(self):
        """Test API error handling in LLM engine."""
        llm_engine = LLMEngine("openrouter", "invalid-key")
        
        # This should fall back to default content
        result = llm_engine.generate_summary_report({})
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)


def run_basic_tests():
    """Run basic tests without external dependencies."""
    print("Running Basic Component Tests...")
    print("=" * 50)
    
    # Test 1: Configuration
    print("Testing configuration...")
    try:
        import config
        print("✓ Configuration loaded successfully")
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        
    # Test 2: Module imports
    print("Testing module imports...")
    modules = [
        ("pdf_parser", "PDFParser"),
        ("llm_engine", "LLMEngine"), 
        ("chart_builder", "ChartBuilder"),
        ("report_generator", "ReportGenerator"),
        ("app_gui", "AppGUI")
    ]
    
    for module_name, class_name in modules:
        try:
            module = __import__(module_name)
            getattr(module, class_name)
            print(f"✓ {module_name} imported successfully")
        except Exception as e:
            print(f"✗ {module_name} import error: {e}")
    
    # Test 3: Basic functionality
    print("Testing basic functionality...")
    
    try:
        # Test LLM fallback content
        llm = LLMEngine("openrouter", "dummy")
        content = llm._get_fallback_content("summary_report")
        assert len(content) > 0
        print("✓ LLM fallback content generation works")
    except Exception as e:
        print(f"✗ LLM fallback test failed: {e}")
    
    try:
        # Test PDF parser text processing
        parser = PDFParser("dummy.pdf")
        result = parser._extract_personal_info("Name: Test User Age: 25")
        assert "Test User" in result.get("name", "")
        print("✓ PDF text parsing works")
    except Exception as e:
        print(f"✗ PDF parsing test failed: {e}")
    
    print("=" * 50)
    print("Basic tests completed!")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test the Nutrition App")
    parser.add_argument("--basic", action="store_true", 
                       help="Run basic tests without external dependencies")
    parser.add_argument("--full", action="store_true",
                       help="Run full test suite (requires all dependencies)")
    
    args = parser.parse_args()
    
    if args.basic or (not args.basic and not args.full):
        # Default to basic tests
        run_basic_tests()
        
    elif args.full:
        # Run full unittest suite
        print("Running Full Test Suite...")
        print("=" * 50)
        
        # Discover and run all tests
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromModule(sys.modules[__name__])
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        if result.wasSuccessful():
            print("\n✓ All tests passed!")
        else:
            print(f"\n✗ {len(result.failures)} test(s) failed")
            print(f"✗ {len(result.errors)} test(s) had errors")
