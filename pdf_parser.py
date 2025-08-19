"""
PDF Parser Module for Nutrition App
Extracts structured and free-text data from PDF questionnaires.
"""

import fitz  # PyMuPDF
import logging
import re
import json
from typing import Dict, List, Any, Optional


class PDFParser:
    """Extracts structured and free-text data from PDF questionnaires."""
    
    def __init__(self, pdf_path: str):
        """
        Initialize PDFParser with path to PDF file.
        
        Args:
            pdf_path (str): Path to the PDF questionnaire file
        """
        self.pdf_path = pdf_path
        self.logger = logging.getLogger(__name__)
        
    def parse(self) -> Dict[str, Any]:
        """
        Parse PDF and extract structured data.
        
        Returns:
            Dict containing parsed questionnaire data
            
        Raises:
            FileNotFoundError: If PDF file doesn't exist
            Exception: If PDF parsing fails
        """
        try:
            self.logger.info(f"Starting PDF parsing for: {self.pdf_path}")
            
            # Open PDF document
            doc = fitz.open(self.pdf_path)
            extracted_data = {
                "personal_info": {},
                "health_metrics": {},
                "fitness_goals": {},
                "dietary_preferences": {},
                "scale_responses": {},
                "free_text_responses": {},
                "checkboxes": {}
            }
            
            # Extract text and form fields from all pages
            full_text = ""
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # Extract text
                page_text = page.get_text()
                full_text += page_text + "\n"
                
                # Extract form fields if any
                form_fields = self._extract_form_fields(page)
                if form_fields:
                    extracted_data.update(form_fields)
            
            doc.close()
            
            # Parse structured data from text
            parsed_data = self._parse_text_content(full_text)
            extracted_data.update(parsed_data)
            
            self.logger.info("PDF parsing completed successfully")
            return extracted_data
            
        except FileNotFoundError:
            self.logger.error(f"PDF file not found: {self.pdf_path}")
            raise
        except Exception as e:
            self.logger.error(f"Error parsing PDF: {str(e)}")
            raise
    
    def _extract_form_fields(self, page) -> Dict[str, Any]:
        """Extract form fields from a PDF page."""
        form_data = {}
        
        try:
            # Get form fields (widgets) from the page
            widgets = page.widgets()
            
            for widget in widgets:
                field_name = widget.field_name
                field_value = widget.field_value
                field_type = widget.field_type
                
                if field_name and field_value:
                    form_data[field_name] = {
                        "value": field_value,
                        "type": self._get_field_type_name(field_type)
                    }
                    
        except Exception as e:
            self.logger.warning(f"Could not extract form fields: {str(e)}")
            
        return form_data
    
    def _get_field_type_name(self, field_type: int) -> str:
        """Convert field type number to readable name."""
        field_types = {
            1: "button",
            2: "text",
            3: "choice",
            4: "signature"
        }
        return field_types.get(field_type, "unknown")
    
    def _parse_text_content(self, text: str) -> Dict[str, Any]:
        """Parse structured content from extracted text."""
        parsed_data = {
            "personal_info": self._extract_personal_info(text),
            "health_metrics": self._extract_health_metrics(text),
            "fitness_goals": self._extract_fitness_goals(text),
            "dietary_preferences": self._extract_dietary_preferences(text),
            "scale_responses": self._extract_scale_responses(text),
            "free_text_responses": self._extract_free_text_responses(text),
            "checkboxes": self._extract_checkboxes(text)
        }
        
        return parsed_data
    
    def _extract_personal_info(self, text: str) -> Dict[str, str]:
        """Extract personal information from text."""
        personal_info = {}
        
        # Common patterns for personal info
        patterns = {
            "name": r"name[:\s]+([a-zA-Z\s]+)",
            "age": r"age[:\s]+(\d+)",
            "gender": r"gender[:\s]+(male|female|other)",
            "height": r"height[:\s]+(\d+['\"]\s*\d*[\"]*|\d+\s*cm|\d+\s*ft)",
            "weight": r"weight[:\s]+(\d+\s*lbs?|\d+\s*kg)",
            "email": r"email[:\s]+([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})"
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                personal_info[key] = match.group(1).strip()
        
        return personal_info
    
    def _extract_health_metrics(self, text: str) -> Dict[str, Any]:
        """Extract health-related metrics."""
        health_metrics = {}
        
        patterns = {
            "bmi": r"bmi[:\s]+(\d+\.?\d*)",
            "body_fat": r"body\s*fat[:\s]+(\d+\.?\d*%?)",
            "blood_pressure": r"blood\s*pressure[:\s]+(\d+/\d+)",
            "resting_heart_rate": r"resting\s*heart\s*rate[:\s]+(\d+)",
            "activity_level": r"activity\s*level[:\s]+(sedentary|light|moderate|active|very\s*active)"
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                health_metrics[key] = match.group(1).strip()
        
        return health_metrics
    
    def _extract_fitness_goals(self, text: str) -> List[str]:
        """Extract fitness goals from text."""
        goals = []
        goal_patterns = [
            r"lose\s*weight",
            r"gain\s*muscle",
            r"improve\s*endurance",
            r"increase\s*strength",
            r"general\s*fitness",
            r"sport\s*specific",
            r"rehabilitation"
        ]
        
        for pattern in goal_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                goals.append(pattern.replace(r"\s*", " ").replace("\\", ""))
        
        return goals
    
    def _extract_dietary_preferences(self, text: str) -> Dict[str, Any]:
        """Extract dietary preferences and restrictions."""
        dietary_info = {
            "restrictions": [],
            "preferences": [],
            "allergies": []
        }
        
        # Dietary restrictions
        restriction_patterns = [
            r"vegetarian", r"vegan", r"gluten[-\s]*free",
            r"dairy[-\s]*free", r"keto", r"paleo",
            r"low[-\s]*carb", r"mediterranean"
        ]
        
        for pattern in restriction_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                dietary_info["restrictions"].append(
                    pattern.replace(r"[-\s]*", "-").replace("\\", "")
                )
        
        # Allergies
        allergy_match = re.search(r"allergies?[:\s]+([^.]+)", text, re.IGNORECASE)
        if allergy_match:
            allergies = [a.strip() for a in allergy_match.group(1).split(",")]
            dietary_info["allergies"] = allergies
        
        return dietary_info
    
    def _extract_scale_responses(self, text: str) -> Dict[str, int]:
        """Extract numeric scale responses (1-10 ratings)."""
        scale_responses = {}
        
        # Common scale question patterns
        scale_patterns = {
            "fitness_level": r"fitness\s*level[:\s]+(\d+)",
            "energy_level": r"energy\s*level[:\s]+(\d+)",
            "stress_level": r"stress\s*level[:\s]+(\d+)",
            "sleep_quality": r"sleep\s*quality[:\s]+(\d+)",
            "motivation": r"motivation[:\s]+(\d+)",
            "nutrition_knowledge": r"nutrition\s*knowledge[:\s]+(\d+)"
        }
        
        for key, pattern in scale_patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value = int(match.group(1))
                if 1 <= value <= 10:  # Validate scale range
                    scale_responses[key] = value
        
        return scale_responses
    
    def _extract_free_text_responses(self, text: str) -> Dict[str, str]:
        """Extract free-text responses from common question areas."""
        free_text = {}
        
        # Common free-text question patterns
        patterns = {
            "goals_description": r"describe\s+your\s+goals[:\s]+([^?]+?)(?=\n|\?|$)",
            "medical_conditions": r"medical\s+conditions[:\s]+([^?]+?)(?=\n|\?|$)",
            "exercise_history": r"exercise\s+history[:\s]+([^?]+?)(?=\n|\?|$)",
            "food_preferences": r"food\s+preferences[:\s]+([^?]+?)(?=\n|\?|$)",
            "additional_notes": r"additional\s+notes[:\s]+([^?]+?)(?=\n|\?|$)"
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                response = match.group(1).strip()
                if len(response) > 5:  # Only include meaningful responses
                    free_text[key] = response
        
        return free_text
    
    def _extract_checkboxes(self, text: str) -> Dict[str, List[str]]:
        """Extract checkbox selections from text."""
        checkboxes = {}
        
        # Look for checkbox patterns
        checkbox_patterns = {
            "equipment_available": [
                "dumbbells", "barbells", "resistance bands",
                "cardio machines", "yoga mat", "pull-up bar"
            ],
            "workout_times": [
                "morning", "afternoon", "evening", "flexible"
            ],
            "experience_level": [
                "beginner", "intermediate", "advanced"
            ]
        }
        
        for category, options in checkbox_patterns.items():
            selected = []
            for option in options:
                if re.search(rf"\b{option}\b", text, re.IGNORECASE):
                    selected.append(option)
            if selected:
                checkboxes[category] = selected
        
        return checkboxes
    
    def save_parsed_data(self, data: Dict[str, Any], output_path: str) -> None:
        """Save parsed data to JSON file for debugging/verification."""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Parsed data saved to: {output_path}")
        except Exception as e:
            self.logger.error(f"Error saving parsed data: {str(e)}")


if __name__ == "__main__":
    # Test the PDF parser
    logging.basicConfig(level=logging.INFO)
    
    # Example usage
    try:
        parser = PDFParser("sample_questionnaire.pdf")
        data = parser.parse()
        parser.save_parsed_data(data, "parsed_data_debug.json")
        print("PDF parsing completed successfully!")
        print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"Error: {e}")
