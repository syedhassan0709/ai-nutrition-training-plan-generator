# Configuration settings for Nutrition App

# OpenRouter API Configuration
OPENROUTER_API_KEY = "your-openrouter-api-key-here"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "anthropic/claude-3-haiku"

# Local LLM Configuration
LOCAL_MODEL_PATH = "models/ggml-gpt4all-j-v1.3-groovy.bin"
USE_LOCAL_LLM = False  # Set to True for offline mode

# Application Settings
OUTPUT_DIR = "output"
TEMPLATES_DIR = "templates"
CHARTS_DIR = "charts"
LOG_LEVEL = "INFO"

# GUI Settings
WINDOW_TITLE = "Nutrition & Training Plan Generator"
WINDOW_SIZE = "800x600"

# Chart Settings
CHART_DPI = 300
CHART_SIZE = (10, 8)

# Supported file types
SUPPORTED_PDF_EXTENSIONS = [".pdf"]
SUPPORTED_DOCX_EXTENSIONS = [".docx"]
