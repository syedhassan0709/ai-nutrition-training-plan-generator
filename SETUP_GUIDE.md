# 🚀 Complete Setup Guide - Nutrition & Training Plan Generator

## 📋 Prerequisites
- **Windows 10/11** (primary support)
- **Python 3.10 or higher** - Download from [python.org](https://python.org)
- **Internet connection** (for initial setup and cloud AI features)

## 🛠️ Virtual Environment Setup (Recommended)

### Step 1: Initial Setup
1. **Download/Extract** the project to your desired folder
2. **Open Command Prompt** in the project folder
3. **Run the setup script**:
   ```bash
   # Windows
   setup_venv.bat
   
   # Linux/macOS  
   chmod +x setup_venv.sh
   ./setup_venv.sh
   ```

### Step 2: Verify Installation
The setup script will:
- ✅ Create a virtual environment in `venv/` folder
- ✅ Install all required Python packages
- ✅ Set up the project structure
- ✅ Verify dependencies

## 🎯 How to Run the Application

### Method 1: Easy Launch (Windows)
```bash
# Double-click this file or run:
run_app_venv.bat
```

### Method 2: Manual Activation
```bash
# Windows
activate_env.bat
python main.py

# Linux/macOS
source venv/bin/activate
python main.py
```

### Method 3: Command Line Interface
```bash
# Activate environment first, then:
python main.py --cli questionnaire.pdf
python main.py --help
```

## 🔧 Different Running Modes

### GUI Mode (Default)
```bash
python main.py
```
- **User-friendly interface**
- **File selection dialogs**
- **Real-time progress tracking**
- **Built-in help and validation**

### CLI Mode
```bash
# Basic usage
python main.py --cli questionnaire.pdf

# With custom settings
python main.py --cli sample.pdf --output ./reports --model local

# Batch processing
python main.py --batch ./pdf_folder ./output_folder
```

### Validation Mode
```bash
python main.py --validate
```
- **Check all dependencies**
- **Verify system compatibility**
- **Test API connections**

## 🤖 AI Model Configuration

### Option 1: Cloud AI (OpenRouter)
1. **Get API Key**: Visit [openrouter.ai](https://openrouter.ai)
2. **Configure**: Enter API key in GUI or edit `config.py`
3. **Benefits**: High-quality responses, latest models
4. **Requirements**: Internet connection, API credits

### Option 2: Local AI (Offline)
1. **Download Model**: App can auto-download GPT4All model
2. **Configure**: Select "Local Model" in GUI
3. **Benefits**: Privacy, no internet needed, no costs
4. **Requirements**: ~3GB disk space, longer processing time

## 📁 Project Structure After Setup
```
Nutirtion_app/
├── venv/                    # Virtual environment (created by setup)
├── main.py                  # Main application
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── setup_venv.bat         # Virtual environment setup (Windows)
├── setup_venv.sh          # Virtual environment setup (Linux/macOS)
├── run_app_venv.bat       # Run app with venv (Windows)
├── run_app_venv.sh        # Run app with venv (Linux/macOS)
├── activate_env.bat       # Activate venv manually (Windows)
├── build_exe_venv.bat     # Build standalone executable
├── templates/             # Word document templates
├── output/               # Generated reports (created at runtime)
├── charts/               # Generated charts (created at runtime)
├── logs/                 # Application logs (created at runtime)
└── assets/               # Sample files and resources
```

## 🎮 Usage Examples

### Example 1: First Time User
```bash
1. setup_venv.bat           # Install everything
2. run_app_venv.bat         # Start GUI
3. Select PDF file          # Use file browser
4. Enter API key            # Or choose local model
5. Click "Generate Reports" # Wait for completion
6. Open output folder       # View results
```

### Example 2: Power User (CLI)
```bash
# Activate environment
activate_env.bat

# Process single file
python main.py --cli questionnaire.pdf --output ./my_reports

# Batch process multiple files
python main.py --batch ./questionnaires ./all_reports

# Use local model for privacy
python main.py --cli sample.pdf --model local
```

### Example 3: Developer/Testing
```bash
# Activate environment
activate_env.bat

# Run tests
python tests.py --basic

# Validate setup
python main.py --validate

# Debug mode
python main.py --cli sample.pdf --log-level DEBUG
```

## 🔧 Troubleshooting

### Common Issues & Solutions

#### 1. "Python not found"
```bash
# Solution: Install Python from python.org
# Ensure "Add to PATH" is checked during installation
```

#### 2. "Virtual environment activation failed"
```bash
# Solution: Run setup_venv.bat again
# Or manually create: python -m venv venv
```

#### 3. "Dependencies installation failed"
```bash
# Solution: Check internet connection
# Try: python -m pip install --upgrade pip
# Then run setup_venv.bat again
```

#### 4. "PDF parsing errors"
```bash
# Solution: Ensure PDF contains searchable text
# Try different PDF file
# Check logs for specific error details
```

#### 5. "API connection failed"
```bash
# Solution: Check internet connection
# Verify API key is correct
# Try local model instead
```

#### 6. "Chart generation failed"
```bash
# Solution: Ensure matplotlib is installed
# Check disk space in output folder
# Try running with --no-chart flag
```

## 📦 Creating Standalone Executable

For distribution without Python installation:

```bash
# From activated virtual environment
build_exe_venv.bat

# Result: dist/NutritionApp.exe (single file, ~100MB)
```

Benefits of standalone executable:
- ✅ No Python installation required
- ✅ All dependencies included
- ✅ Easy distribution
- ✅ Professional deployment

## 🔍 Monitoring and Logs

### Log Files Location
- **Application logs**: `logs/nutrition_app_YYYYMMDD.log`
- **Error details**: Check console output or GUI log panel
- **Debug info**: Set `LOG_LEVEL = "DEBUG"` in config.py

### Performance Monitoring
- **Processing time**: Displayed in GUI
- **Memory usage**: Monitor via Task Manager
- **File sizes**: Check output folder

## 🌐 Network Requirements

### For Cloud AI
- **Outbound HTTPS**: openrouter.ai (port 443)
- **Data usage**: ~1-5KB per request
- **Latency**: 2-10 seconds per AI generation

### For Local AI
- **No network required** after initial setup
- **Initial download**: ~3GB model file
- **Processing time**: 30-120 seconds per generation

## 🔐 Privacy & Security

### Data Handling
- **PDF content**: Processed locally, sent to AI only
- **API keys**: Stored locally, never logged
- **Generated reports**: Saved locally only
- **Local mode**: Complete privacy, no data leaves your machine

### Recommendations
- **Use local models** for sensitive health data
- **Secure API keys** - don't share or commit to version control
- **Regular backups** of important reports

## 📞 Getting Help

### Self-Help Steps
1. **Check logs**: Review error messages in detail
2. **Validate setup**: Run `python main.py --validate`
3. **Test components**: Use individual module tests
4. **Try CLI mode**: Often provides clearer error messages

### Advanced Debugging
```bash
# Activate environment
activate_env.bat

# Run with maximum logging
python main.py --cli sample.pdf --log-level DEBUG

# Test individual components
python tests.py --basic

# Check Python environment
python -c "import sys; print(sys.executable, sys.version)"
```

---

## ✅ Quick Checklist

Before first use:
- [ ] Python 3.10+ installed
- [ ] Virtual environment created (`setup_venv.bat`)
- [ ] Dependencies installed (done by setup script)
- [ ] Sample PDF file ready
- [ ] API key obtained (for cloud AI) OR local model ready
- [ ] Output directory writable

For each use:
- [ ] Virtual environment activated
- [ ] Application runs without errors
- [ ] PDF file is readable and contains expected content
- [ ] Output directory has write permissions
- [ ] Internet connection available (for cloud AI)

---

**🎉 You're all set! The Nutrition & Training Plan Generator is ready to create personalized health and fitness reports.**
