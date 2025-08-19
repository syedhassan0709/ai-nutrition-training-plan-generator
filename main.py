"""
Main Application Entry Point for Nutrition App
Coordinates all components and provides unified interface.
"""

import logging
import os
import sys
import argparse
from datetime import datetime
from typing import Dict, Any, Optional

# Import our custom modules
from pdf_parser import PDFParser
from llm_engine import LLMEngine
from report_generator import ReportGenerator
from chart_builder import ChartBuilder
from app_gui import AppGUI, CLIHandler
import config


class NutritionApp:
    """Main application class that coordinates all components."""
    
    def __init__(self, log_level: str = "INFO"):
        """
        Initialize the Nutrition App.
        
        Args:
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        """
        self.setup_logging(log_level)
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing Nutrition & Training Plan Generator")
        
        # Create necessary directories
        self.ensure_directories()
        
    def setup_logging(self, log_level: str):
        """Set up application logging."""
        # Create logs directory
        os.makedirs("logs", exist_ok=True)
        
        # Configure logging
        log_file = f"logs/nutrition_app_{datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            level=getattr(logging, log_level.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
    def ensure_directories(self):
        """Create necessary application directories."""
        directories = [
            config.OUTPUT_DIR,
            config.TEMPLATES_DIR,
            config.CHARTS_DIR,
            "logs",
            "models"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            self.logger.debug(f"Ensured directory exists: {directory}")
    
    def run_gui(self):
        """Run the application with GUI interface."""
        try:
            self.logger.info("Starting GUI application")
            app = AppGUI()
            app.run()
        except Exception as e:
            self.logger.error(f"GUI application error: {str(e)}")
            raise
    
    def run_cli(self, pdf_path: str, output_dir: Optional[str] = None, 
                model_type: str = "openrouter", api_key: Optional[str] = None):
        """
        Run the application in CLI mode.
        
        Args:
            pdf_path: Path to PDF questionnaire
            output_dir: Output directory for reports
            model_type: Type of LLM model to use
            api_key: API key for cloud models
        """
        try:
            self.logger.info("Starting CLI application")
            cli = CLIHandler()
            cli.run_cli(pdf_path, output_dir, model_type, api_key)
        except Exception as e:
            self.logger.error(f"CLI application error: {str(e)}")
            raise
    
    def process_single_file(self, pdf_path: str, output_dir: Optional[str] = None,
                           model_type: str = "openrouter", api_key: Optional[str] = None,
                           generate_chart: bool = True) -> Dict[str, str]:
        """
        Process a single PDF file and generate reports.
        
        Args:
            pdf_path: Path to PDF questionnaire
            output_dir: Output directory for reports
            model_type: Type of LLM model to use
            api_key: API key for cloud models
            generate_chart: Whether to generate radar chart
            
        Returns:
            Dictionary with paths to generated files
        """
        try:
            self.logger.info(f"Processing single file: {pdf_path}")
            
            # Set defaults
            if not output_dir:
                output_dir = config.OUTPUT_DIR
            
            # Validate inputs
            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"PDF file not found: {pdf_path}")
            
            # Create output directory
            os.makedirs(output_dir, exist_ok=True)
            
            # Initialize components
            self.logger.info("Initializing processing components")
            pdf_parser = PDFParser(pdf_path)
            llm_engine = LLMEngine(model_type, api_key)
            report_generator = ReportGenerator(config.TEMPLATES_DIR, output_dir)
            chart_builder = ChartBuilder(output_dir) if generate_chart else None
            
            # Create templates if they don't exist
            report_generator.create_sample_templates()
            
            # Step 1: Parse PDF
            self.logger.info("Step 1: Parsing PDF questionnaire")
            questionnaire_data = pdf_parser.parse()
            
            # Save parsed data for debugging
            debug_file = os.path.join(output_dir, f"parsed_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            pdf_parser.save_parsed_data(questionnaire_data, debug_file)
            
            # Step 2: Generate chart (optional)
            chart_path = None
            if generate_chart and chart_builder:
                self.logger.info("Step 2: Creating health assessment chart")
                scale_responses = questionnaire_data.get('scale_responses', {})
                if scale_responses:
                    chart_path = os.path.join(output_dir, f"health_assessment_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
                    chart_builder.build_radar_chart(scale_responses, chart_path)
                else:
                    self.logger.warning("No scale responses found for chart generation")
            
            # Step 3: Generate AI content
            self.logger.info("Step 3: Generating AI content")
            llm_content = {
                "summary": llm_engine.generate_summary_report(questionnaire_data),
                "training": llm_engine.generate_training_plan(questionnaire_data),
                "nutrition": llm_engine.generate_nutrition_plan(questionnaire_data)
            }
            
            # Step 4: Generate reports
            self.logger.info("Step 4: Generating Word documents")
            generated_reports = report_generator.generate_all_reports(
                questionnaire_data, llm_content, chart_path
            )
            
            # Add chart path to results if generated
            if chart_path:
                generated_reports["chart"] = chart_path
            
            # Add debug data path
            generated_reports["debug_data"] = debug_file
            
            self.logger.info("Processing completed successfully")
            return generated_reports
            
        except Exception as e:
            self.logger.error(f"Error processing file: {str(e)}")
            raise
    
    def batch_process(self, pdf_directory: str, output_directory: str,
                     model_type: str = "openrouter", api_key: Optional[str] = None) -> Dict[str, Dict[str, str]]:
        """
        Process multiple PDF files in batch mode.
        
        Args:
            pdf_directory: Directory containing PDF files
            output_directory: Base output directory
            model_type: Type of LLM model to use
            api_key: API key for cloud models
            
        Returns:
            Dictionary mapping PDF filenames to their generated files
        """
        try:
            self.logger.info(f"Starting batch processing: {pdf_directory}")
            
            # Find all PDF files
            pdf_files = [f for f in os.listdir(pdf_directory) if f.lower().endswith('.pdf')]
            
            if not pdf_files:
                raise ValueError(f"No PDF files found in directory: {pdf_directory}")
            
            self.logger.info(f"Found {len(pdf_files)} PDF files to process")
            
            results = {}
            
            for i, pdf_file in enumerate(pdf_files, 1):
                try:
                    self.logger.info(f"Processing file {i}/{len(pdf_files)}: {pdf_file}")
                    
                    pdf_path = os.path.join(pdf_directory, pdf_file)
                    file_output_dir = os.path.join(output_directory, os.path.splitext(pdf_file)[0])
                    
                    # Process the file
                    file_results = self.process_single_file(
                        pdf_path, file_output_dir, model_type, api_key
                    )
                    
                    results[pdf_file] = file_results
                    self.logger.info(f"✓ Completed processing: {pdf_file}")
                    
                except Exception as e:
                    self.logger.error(f"✗ Failed to process {pdf_file}: {str(e)}")
                    results[pdf_file] = {"error": str(e)}
            
            self.logger.info(f"Batch processing completed. {len([r for r in results.values() if 'error' not in r])}/{len(pdf_files)} files processed successfully")
            return results
            
        except Exception as e:
            self.logger.error(f"Batch processing error: {str(e)}")
            raise
    
    def validate_setup(self) -> Dict[str, bool]:
        """
        Validate application setup and dependencies.
        
        Returns:
            Dictionary with validation results
        """
        validation_results = {}
        
        try:
            # Check directories
            validation_results["directories"] = all(
                os.path.exists(d) for d in [config.OUTPUT_DIR, config.TEMPLATES_DIR]
            )
            
            # Check PDF parsing capability
            try:
                import fitz
                validation_results["pdf_parsing"] = True
            except ImportError:
                validation_results["pdf_parsing"] = False
            
            # Check Word document generation
            try:
                from docx import Document
                validation_results["docx_generation"] = True
            except ImportError:
                validation_results["docx_generation"] = False
            
            # Check chart generation
            try:
                import matplotlib.pyplot as plt
                validation_results["chart_generation"] = True
            except ImportError:
                validation_results["chart_generation"] = False
            
            # Check local LLM capability
            try:
                import gpt4all
                validation_results["local_llm"] = True
            except ImportError:
                validation_results["local_llm"] = False
            
            # Check network connectivity for cloud LLM
            try:
                import requests
                response = requests.get("https://openrouter.ai", timeout=5)
                validation_results["cloud_llm_connectivity"] = response.status_code == 200
            except:
                validation_results["cloud_llm_connectivity"] = False
            
            # Overall status
            critical_components = ["pdf_parsing", "docx_generation", "chart_generation"]
            validation_results["overall"] = all(
                validation_results.get(comp, False) for comp in critical_components
            )
            
            return validation_results
            
        except Exception as e:
            self.logger.error(f"Validation error: {str(e)}")
            return {"overall": False, "error": str(e)}
    
    def print_system_info(self):
        """Print system information and setup status."""
        print("=" * 60)
        print("NUTRITION & TRAINING PLAN GENERATOR")
        print("=" * 60)
        
        # Basic info
        print(f"Python version: {sys.version}")
        print(f"Platform: {sys.platform}")
        print(f"Working directory: {os.getcwd()}")
        print(f"Output directory: {config.OUTPUT_DIR}")
        
        # Validation results
        print("\nCOMPONENT VALIDATION:")
        print("-" * 30)
        
        validation = self.validate_setup()
        
        status_symbols = {True: "✓", False: "✗"}
        
        components = {
            "directories": "Required directories",
            "pdf_parsing": "PDF parsing (PyMuPDF)",
            "docx_generation": "Word document generation (python-docx)",
            "chart_generation": "Chart generation (matplotlib)",
            "local_llm": "Local LLM support (GPT4All)",
            "cloud_llm_connectivity": "Cloud LLM connectivity"
        }
        
        for key, description in components.items():
            status = validation.get(key, False)
            symbol = status_symbols[status]
            print(f"{symbol} {description}")
        
        print("-" * 30)
        overall_status = validation.get("overall", False)
        print(f"Overall Status: {status_symbols[overall_status]} {'Ready' if overall_status else 'Issues detected'}")
        
        if not overall_status:
            print("\nPlease install missing dependencies with:")
            print("pip install -r requirements.txt")
        
        print("=" * 60)


def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(
        description="Nutrition & Training Plan Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run GUI application
  python main.py
  
  # Process single PDF file
  python main.py --cli sample.pdf
  
  # Process with custom output directory
  python main.py --cli sample.pdf --output ./my_reports
  
  # Use local LLM model
  python main.py --cli sample.pdf --model local
  
  # Batch process multiple PDFs
  python main.py --batch ./pdfs_folder ./output_folder
  
  # Validate setup
  python main.py --validate
        """
    )
    
    # Mode selection
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument("--gui", action="store_true", default=True,
                           help="Run GUI application (default)")
    mode_group.add_argument("--cli", metavar="PDF_FILE",
                           help="Run CLI mode with specified PDF file")
    mode_group.add_argument("--batch", nargs=2, metavar=("PDF_DIR", "OUTPUT_DIR"),
                           help="Batch process PDFs in directory")
    mode_group.add_argument("--validate", action="store_true",
                           help="Validate application setup")
    
    # Configuration options
    parser.add_argument("--output", metavar="DIR",
                       help="Output directory for generated reports")
    parser.add_argument("--model", choices=["openrouter", "local"], default="openrouter",
                       help="LLM model type (default: openrouter)")
    parser.add_argument("--api-key", metavar="KEY",
                       help="API key for cloud LLM services")
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                       default="INFO", help="Logging level (default: INFO)")
    parser.add_argument("--no-chart", action="store_true",
                       help="Skip chart generation")
    
    args = parser.parse_args()
    
    # Initialize application
    app = NutritionApp(args.log_level)
    
    try:
        if args.validate:
            # Validation mode
            app.print_system_info()
            
        elif args.cli:
            # CLI mode
            results = app.process_single_file(
                args.cli, args.output, args.model, args.api_key,
                generate_chart=not args.no_chart
            )
            
            print("\nGenerated files:")
            for file_type, path in results.items():
                print(f"  {file_type}: {path}")
            
        elif args.batch:
            # Batch mode
            pdf_dir, output_dir = args.batch
            results = app.batch_process(pdf_dir, output_dir, args.model, args.api_key)
            
            print(f"\nBatch processing results:")
            successful = sum(1 for r in results.values() if 'error' not in r)
            print(f"Successfully processed: {successful}/{len(results)} files")
            
            # Show details
            for filename, result in results.items():
                if 'error' in result:
                    print(f"  ✗ {filename}: {result['error']}")
                else:
                    print(f"  ✓ {filename}")
            
        else:
            # GUI mode (default)
            app.run_gui()
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {str(e)}")
        app.logger.error(f"Application error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
