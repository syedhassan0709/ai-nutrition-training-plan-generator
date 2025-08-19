"""
LLM Engine Module for Nutrition App
Handles communication with OpenRouter API and local LLMs.
"""

import requests
import json
import logging
import os
from typing import Dict, Any, Optional, List
from datetime import datetime

try:
    import gpt4all
    GPT4ALL_AVAILABLE = True
except ImportError:
    GPT4ALL_AVAILABLE = False
    logging.warning("GPT4All not available. Only cloud models will work. Install with: pip install gpt4all")

import config


class LLMEngine:
    """Handles communication with OpenRouter API or local LLMs."""
    
    def __init__(self, model_type: str = "openrouter", api_key: Optional[str] = None):
        """
        Initialize LLM Engine.
        
        Args:
            model_type (str): Either "openrouter" or "local"
            api_key (str, optional): API key for cloud services
        """
        self.model_type = model_type
        self.api_key = api_key or config.OPENROUTER_API_KEY
        self.logger = logging.getLogger(__name__)
        
        # Initialize local model if needed
        self.local_model = None
        if model_type == "local" and GPT4ALL_AVAILABLE:
            self._initialize_local_model()
    
    def _initialize_local_model(self):
        """Initialize local GPT4All model."""
        try:
            if os.path.exists(config.LOCAL_MODEL_PATH):
                self.local_model = gpt4all.GPT4All(config.LOCAL_MODEL_PATH)
                self.logger.info("Local model initialized successfully")
            else:
                self.logger.warning(f"Local model not found at: {config.LOCAL_MODEL_PATH}")
        except Exception as e:
            self.logger.error(f"Failed to initialize local model: {str(e)}")
    
    def generate_summary_report(self, questionnaire_data: Dict[str, Any]) -> str:
        """
        Generate summary report content based on questionnaire data.
        
        Args:
            questionnaire_data: Parsed questionnaire data
            
        Returns:
            Generated summary text
        """
        prompt = self._build_summary_prompt(questionnaire_data)
        return self._generate_content(prompt, "summary_report")
    
    def generate_training_plan(self, questionnaire_data: Dict[str, Any]) -> str:
        """
        Generate personalized training plan.
        
        Args:
            questionnaire_data: Parsed questionnaire data
            
        Returns:
            Generated training plan text
        """
        prompt = self._build_training_prompt(questionnaire_data)
        return self._generate_content(prompt, "training_plan")
    
    def generate_nutrition_plan(self, questionnaire_data: Dict[str, Any]) -> str:
        """
        Generate personalized nutrition plan.
        
        Args:
            questionnaire_data: Parsed questionnaire data
            
        Returns:
            Generated nutrition plan text
        """
        prompt = self._build_nutrition_prompt(questionnaire_data)
        return self._generate_content(prompt, "nutrition_plan")
    
    def _generate_content(self, prompt: str, content_type: str) -> str:
        """
        Generate content using the selected model.
        
        Args:
            prompt: The prompt to send to the LLM
            content_type: Type of content being generated
            
        Returns:
            Generated content
        """
        try:
            if self.model_type == "openrouter":
                return self._generate_with_openrouter(prompt, content_type)
            elif self.model_type == "local":
                return self._generate_with_local_model(prompt, content_type)
            else:
                raise ValueError(f"Unknown model type: {self.model_type}")
                
        except Exception as e:
            self.logger.error(f"Error generating {content_type}: {str(e)}")
            return self._get_fallback_content(content_type)
    
    def _generate_with_openrouter(self, prompt: str, content_type: str) -> str:
        """Generate content using OpenRouter API."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": config.OPENROUTER_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a professional fitness and nutrition expert. Provide detailed, personalized advice based on the questionnaire data provided."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 2000,
            "temperature": 0.7
        }
        
        response = requests.post(
            config.OPENROUTER_API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            self.logger.info(f"Successfully generated {content_type} with OpenRouter")
            return content
        else:
            error_msg = f"OpenRouter API error: {response.status_code} - {response.text}"
            self.logger.error(error_msg)
            raise Exception(error_msg)
    
    def _generate_with_local_model(self, prompt: str, content_type: str) -> str:
        """Generate content using local GPT4All model."""
        if not self.local_model:
            raise Exception("Local model not initialized")
        
        try:
            # Generate response with local model
            response = self.local_model.generate(
                prompt=prompt,
                max_tokens=1500,
                temp=0.7,
                top_p=0.9
            )
            
            self.logger.info(f"Successfully generated {content_type} with local model")
            return response
            
        except Exception as e:
            self.logger.error(f"Local model generation error: {str(e)}")
            raise
    
    def _build_summary_prompt(self, data: Dict[str, Any]) -> str:
        """Build prompt for summary report generation."""
        personal_info = data.get('personal_info', {})
        health_metrics = data.get('health_metrics', {})
        scale_responses = data.get('scale_responses', {})
        fitness_goals = data.get('fitness_goals', [])
        
        prompt = f"""
Based on the following questionnaire data, create a comprehensive health and fitness summary report:

PERSONAL INFORMATION:
{json.dumps(personal_info, indent=2)}

HEALTH METRICS:
{json.dumps(health_metrics, indent=2)}

SCALE RESPONSES (1-10):
{json.dumps(scale_responses, indent=2)}

FITNESS GOALS:
{', '.join(fitness_goals) if fitness_goals else 'Not specified'}

Please provide:
1. A comprehensive assessment of the individual's current health and fitness status
2. Key insights based on their scale responses and metrics
3. Identification of strengths and areas for improvement
4. Recommendations for achieving their stated goals
5. Any potential concerns or considerations

Format the response as a professional report with clear sections and actionable insights.
"""
        return prompt
    
    def _build_training_prompt(self, data: Dict[str, Any]) -> str:
        """Build prompt for training plan generation."""
        personal_info = data.get('personal_info', {})
        fitness_goals = data.get('fitness_goals', [])
        scale_responses = data.get('scale_responses', {})
        equipment = data.get('checkboxes', {}).get('equipment_available', [])
        experience = data.get('checkboxes', {}).get('experience_level', [])
        workout_times = data.get('checkboxes', {}).get('workout_times', [])
        
        prompt = f"""
Create a personalized 4-week training plan based on this information:

PERSONAL INFO:
{json.dumps(personal_info, indent=2)}

FITNESS GOALS:
{', '.join(fitness_goals) if fitness_goals else 'General fitness'}

FITNESS LEVEL & METRICS:
{json.dumps(scale_responses, indent=2)}

AVAILABLE EQUIPMENT:
{', '.join(equipment) if equipment else 'Basic bodyweight exercises'}

EXPERIENCE LEVEL:
{', '.join(experience) if experience else 'Beginner'}

PREFERRED WORKOUT TIMES:
{', '.join(workout_times) if workout_times else 'Flexible'}

Please create a detailed 4-week progressive training plan including:

1. WEEK-BY-WEEK BREAKDOWN:
   - Weekly schedule (days per week, duration)
   - Specific exercises with sets, reps, and progression
   - Rest days and recovery protocols

2. EXERCISE DESCRIPTIONS:
   - Proper form cues for key exercises
   - Modifications for different fitness levels
   - Safety considerations

3. PROGRESSION STRATEGY:
   - How to increase intensity each week
   - When and how to add new exercises
   - Signs to progress or regress

4. RECOVERY AND MOBILITY:
   - Warm-up routines
   - Cool-down stretches
   - Rest day activities

Format as a clear, actionable plan that can be followed step-by-step.
"""
        return prompt
    
    def _build_nutrition_prompt(self, data: Dict[str, Any]) -> str:
        """Build prompt for nutrition plan generation."""
        personal_info = data.get('personal_info', {})
        health_metrics = data.get('health_metrics', {})
        dietary_preferences = data.get('dietary_preferences', {})
        fitness_goals = data.get('fitness_goals', [])
        free_text = data.get('free_text_responses', {})
        
        prompt = f"""
Create a personalized nutrition plan based on this information:

PERSONAL INFO:
{json.dumps(personal_info, indent=2)}

HEALTH METRICS:
{json.dumps(health_metrics, indent=2)}

FITNESS GOALS:
{', '.join(fitness_goals) if fitness_goals else 'General health'}

DIETARY PREFERENCES & RESTRICTIONS:
{json.dumps(dietary_preferences, indent=2)}

ADDITIONAL NOTES:
{json.dumps(free_text, indent=2)}

Please create a comprehensive nutrition plan including:

1. DAILY NUTRITION TARGETS:
   - Estimated daily caloric needs
   - Macronutrient breakdown (protein, carbs, fats)
   - Key micronutrients to focus on

2. MEAL PLANNING:
   - Sample daily meal plan
   - Pre and post-workout nutrition
   - Healthy snack options
   - Hydration guidelines

3. FOOD RECOMMENDATIONS:
   - Best protein sources for their goals
   - Complex carbohydrates to include
   - Healthy fats to incorporate
   - Vegetables and fruits to prioritize

4. MEAL PREP STRATEGIES:
   - Weekly meal prep tips
   - Quick and healthy meal ideas
   - Portion control guidelines

5. SUPPLEMENTS (if appropriate):
   - Evidence-based supplement recommendations
   - Timing and dosage suggestions

6. SPECIAL CONSIDERATIONS:
   - Account for any dietary restrictions or allergies
   - Adaptations for their specific goals
   - Tips for dining out and social situations

Format as a practical, easy-to-follow nutrition guide.
"""
        return prompt
    
    def _get_fallback_content(self, content_type: str) -> str:
        """Provide fallback content when LLM generation fails."""
        fallback_content = {
            "summary_report": """
HEALTH & FITNESS SUMMARY REPORT

Thank you for completing the questionnaire. Based on your responses, here are some general recommendations:

CURRENT STATUS:
Your questionnaire responses have been recorded and will be used to create personalized recommendations.

KEY RECOMMENDATIONS:
1. Maintain consistency with your current exercise routine
2. Focus on balanced nutrition with adequate protein intake
3. Ensure proper hydration throughout the day
4. Prioritize quality sleep for recovery
5. Track your progress regularly

NEXT STEPS:
1. Review your detailed training plan
2. Follow the personalized nutrition guidelines
3. Monitor your progress weekly
4. Adjust plans as needed based on results

Note: This is a basic summary. For detailed recommendations, please ensure your LLM connection is working properly.
""",
            
            "training_plan": """
PERSONALIZED TRAINING PLAN

GENERAL 4-WEEK TRAINING PROGRAM

WEEK 1-2: Foundation Building
- 3-4 workouts per week
- Focus on form and movement patterns
- 2-3 sets of 8-12 repetitions
- Rest 48-72 hours between sessions

WEEK 3-4: Progressive Overload
- 4-5 workouts per week
- Increase intensity and volume
- 3-4 sets of 6-15 repetitions
- Include variety in exercises

SAMPLE WORKOUT STRUCTURE:
1. Warm-up (10 minutes)
2. Strength training (30-45 minutes)
3. Cardio (15-20 minutes)
4. Cool-down and stretching (10 minutes)

BASIC EXERCISES:
- Bodyweight squats
- Push-ups (modified as needed)
- Planks
- Walking or light jogging
- Basic stretching routine

Note: This is a general plan. For personalized recommendations, please ensure your LLM connection is working properly.
""",
            
            "nutrition_plan": """
PERSONALIZED NUTRITION PLAN

GENERAL NUTRITION GUIDELINES

DAILY NUTRITION FRAMEWORK:
- Eat 3 balanced meals and 2 healthy snacks
- Include protein with every meal
- Fill half your plate with vegetables
- Choose whole grains over refined carbs
- Stay hydrated with 8+ glasses of water daily

SAMPLE DAILY MEAL STRUCTURE:

BREAKFAST:
- Protein source (eggs, Greek yogurt, protein smoothie)
- Complex carbs (oatmeal, whole grain toast)
- Fruits and/or vegetables

LUNCH:
- Lean protein (chicken, fish, legumes)
- Vegetables (variety of colors)
- Healthy carbs (quinoa, brown rice, sweet potato)

DINNER:
- Protein source
- Large portion of vegetables
- Moderate healthy carbs
- Small amount of healthy fats

SNACKS:
- Nuts and fruits
- Vegetables with hummus
- Greek yogurt with berries

GENERAL TIPS:
- Plan meals in advance
- Prep ingredients on weekends
- Listen to hunger and fullness cues
- Allow for occasional treats in moderation

Note: This is a general plan. For personalized recommendations, please ensure your LLM connection is working properly.
"""
        }
        
        return fallback_content.get(content_type, "Content generation failed. Please check your LLM configuration.")
    
    def test_connection(self) -> bool:
        """Test LLM connection and functionality."""
        try:
            test_prompt = "Please respond with 'Connection successful' to confirm the LLM is working."
            response = self._generate_content(test_prompt, "test")
            
            if "successful" in response.lower() or len(response) > 0:
                self.logger.info(f"LLM connection test passed for {self.model_type}")
                return True
            else:
                self.logger.warning(f"LLM connection test failed for {self.model_type}")
                return False
                
        except Exception as e:
            self.logger.error(f"LLM connection test error: {str(e)}")
            return False


if __name__ == "__main__":
    # Test the LLM engine
    logging.basicConfig(level=logging.INFO)
    
    # Test with mock data
    test_data = {
        "personal_info": {"name": "John Doe", "age": "30", "weight": "180 lbs"},
        "fitness_goals": ["lose weight", "gain muscle"],
        "scale_responses": {"fitness_level": 5, "energy_level": 6},
        "dietary_preferences": {"restrictions": ["vegetarian"]},
        "checkboxes": {"equipment_available": ["dumbbells", "yoga mat"]}
    }
    
    # Test OpenRouter (will use fallback if no API key)
    llm = LLMEngine("openrouter")
    
    print("Testing LLM Engine...")
    print("=" * 50)
    
    if llm.test_connection():
        print("✓ LLM connection successful")
    else:
        print("⚠ LLM connection failed - using fallback content")
    
    print("\nGenerating sample content...")
    summary = llm.generate_summary_report(test_data)
    print("Summary generated successfully!")
    
    training = llm.generate_training_plan(test_data)
    print("Training plan generated successfully!")
    
    nutrition = llm.generate_nutrition_plan(test_data)
    print("Nutrition plan generated successfully!")
