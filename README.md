# Nutrition & Training Plan Generator

A comprehensive Windows application that processes PDF questionnaires and generates personalized health, fitness, and nutrition reports with AI-powered insights.

## 🚀 Features

### Core Functionality
- **PDF Processing**: Extracts structured data from health questionnaires using PyMuPDF
- **AI-Powered Analysis**: Generates personalized insights using OpenRouter API or local LLMs
- **Professional Reports**: Creates three detailed Word documents:
  - Health & Fitness Summary Report with radar chart
  - Personalized Training Plan
  - Custom Nutrition Plan
- **Interactive Charts**: Generates radar (spider web) charts for health assessments
- **Dual Interface**: Both GUI and CLI modes available

### Technical Features
- **Cloud & Local AI**: Support for OpenRouter API and local GPT4All models
- **Flexible Input**: Handles various PDF questionnaire formats
- **Professional Output**: Generates publication-ready Word documents
- **Batch Processing**: Process multiple questionnaires simultaneously
- **Comprehensive Logging**: Detailed logs for debugging and monitoring

## 📋 Requirements

### Python Version
- Python 3.10 or higher

### Dependencies
```bash
pip install -r requirements.txt
```

### Key Libraries
- **PyMuPDF (fitz)**: PDF text and form extraction
- **python-docx**: Word document generation
- **matplotlib**: Chart creation
- **numpy**: Numerical computations
- **requests**: API communication
- **tkinter**: GUI interface (included with Python)
- **gpt4all**: Local LLM support (optional)

## 🛠️ Installation

### 1. Clone or Download
```bash
# If using Git
git clone <repository-url>
cd Nutirtion_app

# Or download and extract the ZIP file
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API (Optional)
For cloud-based AI features, get an API key from [OpenRouter](https://openrouter.ai):
1. Sign up at openrouter.ai
2. Generate an API key
3. Enter it in the GUI or set it in `config.py`

### 4. Verify Installation
```bash
python main.py --validate
```

## 🖥️ Usage

### GUI Mode (Recommended)
```bash
python main.py
```

The GUI provides an intuitive interface with:
- File selection dialogs
- Model configuration options
- Real-time processing logs
- Progress indicators

### CLI Mode
```bash
# Basic usage
python main.py --cli questionnaire.pdf

# With custom output directory
python main.py --cli questionnaire.pdf --output ./my_reports

# Using local LLM
python main.py --cli questionnaire.pdf --model local

# With specific API key
python main.py --cli questionnaire.pdf --api-key your-api-key-here
```

### Batch Processing
```bash
python main.py --batch ./pdf_folder ./output_folder
```

## 📊 Input Requirements

### PDF Questionnaire Format
The application can process questionnaires containing:

#### Personal Information
- Name, age, gender
- Height, weight
- Email address

#### Health Metrics
- BMI, body fat percentage
- Blood pressure
- Resting heart rate
- Activity level

#### Scale Responses (1-10)
- Fitness level
- Energy level
- Stress level
- Sleep quality
- Motivation
- Nutrition knowledge

#### Free-Text Responses
- Health goals description
- Medical conditions
- Exercise history
- Food preferences
- Additional notes

#### Checkboxes/Multiple Choice
- Available equipment
- Preferred workout times
- Experience level
- Dietary restrictions

### Sample Questionnaire Structure
```
HEALTH & FITNESS QUESTIONNAIRE

Personal Information:
Name: John Doe
Age: 30
Gender: Male
Height: 6'0"
Weight: 180 lbs

Assessment Scales (Rate 1-10):
Fitness Level: 6
Energy Level: 7
Motivation: 8

Goals:
☑ Lose weight
☑ Gain muscle
☐ Improve endurance

Available Equipment:
☑ Dumbbells
☑ Yoga mat
☐ Cardio machines
```

## 📄 Output Files

### Generated Reports

#### 1. Summary Report (`Summary_Report_YYYYMMDD_HHMMSS.docx`)
- Personal information overview
- Health assessment radar chart
- Scale responses summary
- AI-generated insights and recommendations
- Goal analysis

#### 2. Training Plan (`Training_Plan_YYYYMMDD_HHMMSS.docx`)
- 4-week progressive training program
- Exercise descriptions and form cues
- Equipment-specific modifications
- Progress tracking guidelines
- Recovery protocols

#### 3. Nutrition Plan (`Nutrition_Plan_YYYYMMDD_HHMMSS.docx`)
- Daily nutrition targets
- Macronutrient breakdown
- Meal planning strategies
- Food recommendations
- Supplement suggestions (if appropriate)

#### Additional Files
- **Radar Chart**: Health assessment visualization (PNG)
- **Debug Data**: Parsed questionnaire data (JSON)
- **Logs**: Processing logs for troubleshooting

## ⚙️ Configuration

### `config.py` Settings

```python
# API Configuration
OPENROUTER_API_KEY = "your-api-key-here"
OPENROUTER_MODEL = "anthropic/claude-3-haiku"

# Directories
OUTPUT_DIR = "output"
TEMPLATES_DIR = "templates"
CHARTS_DIR = "charts"

# Local LLM
LOCAL_MODEL_PATH = "models/ggml-gpt4all-j-v1.3-groovy.bin"
USE_LOCAL_LLM = False

# GUI Settings
WINDOW_TITLE = "Nutrition & Training Plan Generator"
WINDOW_SIZE = "800x600"
```

### Model Options

#### OpenRouter (Cloud)
- **Pros**: High-quality responses, no local setup required
- **Cons**: Requires internet, API costs
- **Models**: GPT-4, Claude, Llama, etc.

#### GPT4All (Local)
- **Pros**: Works offline, no API costs, privacy
- **Cons**: Requires model download, slower processing
- **Setup**: Download model to `models/` directory

## 🔧 Troubleshooting

### Common Issues

#### "Import could not be resolved" errors
These are IDE linting warnings. Install dependencies:
```bash
pip install -r requirements.txt
```

#### PDF parsing fails
- Ensure PDF is not password-protected
- Check if PDF contains searchable text
- Try a different PDF file

#### API connection errors
- Verify internet connection
- Check API key validity
- Confirm OpenRouter account has credits

#### Chart generation fails
- Ensure matplotlib is installed
- Check if output directory is writable
- Verify sufficient disk space

#### Word document errors
- Install python-docx: `pip install python-docx`
- Check write permissions in output directory
- Ensure sufficient disk space

### Getting Help

1. **Check Logs**: Review `logs/nutrition_app_YYYYMMDD.log`
2. **Validate Setup**: Run `python main.py --validate`
3. **Test Components**: Use individual module test functions
4. **Debug Mode**: Set `LOG_LEVEL = "DEBUG"` in config.py

### Performance Tips

- **Large PDFs**: May take longer to process
- **Batch Processing**: Process during off-peak hours
- **Local LLM**: Slower but more private
- **Memory**: Close other applications for better performance

## 🏗️ Development

### Project Structure
```
Nutirtion_app/
├── main.py                 # Main application entry point
├── pdf_parser.py           # PDF processing module
├── llm_engine.py          # AI/LLM integration
├── report_generator.py    # Word document generation
├── chart_builder.py       # Chart creation
├── app_gui.py             # GUI interface
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── templates/             # Word document templates
├── output/               # Generated reports
├── charts/               # Generated charts
├── assets/               # Sample files
└── logs/                 # Application logs
```

### Modular Design
Each module is self-contained and can be tested independently:

```python
# Test PDF parser
from pdf_parser import PDFParser
parser = PDFParser("sample.pdf")
data = parser.parse()

# Test chart builder
from chart_builder import ChartBuilder
chart = ChartBuilder()
chart.create_sample_chart("test_chart.png")
```

### Extending the Application

#### Adding New Chart Types
```python
# In chart_builder.py
def build_custom_chart(self, data, output_path):
    # Your custom chart logic
    pass
```

#### Adding New Report Sections
```python
# In report_generator.py
def _add_custom_section(self, doc, data):
    # Your custom section logic
    pass
```

#### Supporting New PDF Formats
```python
# In pdf_parser.py
def _parse_custom_format(self, text):
    # Your custom parsing logic
    pass
```

## 📦 Packaging for Distribution

### Create Standalone Executable
```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed main.py

# Or use the provided spec file
pyinstaller main.spec
```

### Distribution Package
```bash
# Create distribution folder
mkdir nutrition_app_dist
cp -r templates/ nutrition_app_dist/
cp -r assets/ nutrition_app_dist/
cp requirements.txt nutrition_app_dist/
cp README.md nutrition_app_dist/
cp dist/main.exe nutrition_app_dist/nutrition_app.exe
```

## 📝 License

This project is provided as-is for educational and personal use.

## 🤝 Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Contact Us

Email: syed.hassan0709@gmail.com
Phone + Whatsapp: +923359549776

## 📞 Support

For support and questions:

1. Check the troubleshooting section
2. Review the logs for error details
3. Test individual components
4. Validate your setup with `--validate`

---

**Built with ❤️ for health and fitness enthusiasts**
