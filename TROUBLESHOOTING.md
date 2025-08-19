# 🔧 Dependency Installation Troubleshooting Guide

## ❌ Problem: Package Installation Failed

You're seeing errors like:
- `ERROR: Could not find a version that satisfies the requirement...`
- `ERROR: No matching distribution found...`
- `ImportError: No module named '...'`

## 🎯 Quick Fixes (Try in Order)

### Fix 1: Use Updated Requirements
```bash
# The requirements.txt has been updated with flexible versions
setup_venv.bat
```

### Fix 2: Install Core Packages Only (If Fix 1 fails)
```bash
# Activate your virtual environment first
activate_env.bat

# Install minimal requirements
pip install -r requirements_minimal.txt
```

### Fix 3: Manual Installation (If Fix 2 fails)
```bash
# Activate virtual environment
activate_env.bat

# Install packages one by one
pip install PyMuPDF
pip install python-docx  
pip install matplotlib
pip install numpy
pip install requests
pip install Pillow

# Optional (skip if causing issues)
pip install gpt4all
pip install openai
```

### Fix 4: Upgrade Python (If still failing)
Your Python version might be too old or new. 
- **Download Python 3.10 or 3.11** from [python.org](https://python.org)
- Avoid Python 3.12+ (some packages not compatible yet)

## 🔍 Diagnostic Tools

### Check What's Wrong
```bash
# Run diagnostic script
troubleshoot.bat
```

### Check Python Version
```bash
python --version
# Should show 3.10.x or 3.11.x for best compatibility
```

### Check Virtual Environment
```bash
# Make sure you're in the virtual environment
activate_env.bat
where python
# Should show path ending with \venv\Scripts\python.exe
```

## 🎮 Alternative Installation Methods

### Method A: Minimal Installation (Cloud AI Only)
If you only want to use cloud AI and don't need local models:

```bash
# Create fresh virtual environment
rmdir /s venv
python -m venv venv
call venv\Scripts\activate.bat

# Install only essential packages
pip install PyMuPDF python-docx matplotlib numpy requests Pillow
```

### Method B: Without Virtual Environment (Not Recommended)
If virtual environment keeps failing:

```bash
# Install globally (may conflict with other projects)
pip install PyMuPDF python-docx matplotlib numpy requests Pillow

# Run app directly
python main.py
```

### Method C: Conda Environment (Alternative)
If you have Anaconda/Miniconda:

```bash
# Create conda environment
conda create -n nutrition_app python=3.11
conda activate nutrition_app

# Install packages via conda
conda install numpy matplotlib pillow requests
pip install PyMuPDF python-docx gpt4all

# Run app
python main.py
```

## 🔧 Specific Error Solutions

### Error: "gpt4all version not found"
```bash
# Skip GPT4All for now, install everything else
pip install PyMuPDF python-docx matplotlib numpy requests Pillow

# The app will work with cloud AI only
```

### Error: "Microsoft Visual C++ required"
Some packages need C++ compiler on Windows:
1. Download "Microsoft C++ Build Tools" from Microsoft
2. Or install "Visual Studio Community" 
3. Restart and try installation again

### Error: "SSL Certificate verify failed"
```bash
# Upgrade pip and certificates
python -m pip install --upgrade pip
pip install --upgrade certifi
```

### Error: "Access denied" or "Permission error"
```bash
# Run Command Prompt as Administrator
# Or try:
pip install --user PyMuPDF python-docx matplotlib numpy requests Pillow
```

## ✅ Test Your Installation

After fixing, test that everything works:

```bash
# Run diagnostic
troubleshoot.bat

# Test the app
python main.py --validate

# Try processing a sample file
python main.py --cli assets\sample_questionnaire.txt
```

## 🎯 Minimal Working Configuration

At minimum, you need these packages for the app to work:
- ✅ **PyMuPDF** - PDF processing
- ✅ **python-docx** - Word document creation  
- ✅ **matplotlib** - Chart generation
- ✅ **numpy** - Math operations
- ✅ **requests** - API calls
- ✅ **Pillow** - Image processing
- ✅ **tkinter** - GUI (included with Python)

Optional packages:
- ⚠️ **gpt4all** - Local AI (can skip and use cloud AI)
- ⚠️ **openai** - OpenAI API (can use OpenRouter instead)

## 📞 Still Having Issues?

### Last Resort Options:

1. **Use Cloud-Only Mode**
   - Skip local LLM installation
   - Use OpenRouter API for all AI features
   - Much simpler setup

2. **Try Different Python Version**
   - Uninstall current Python
   - Install Python 3.10.11 (very stable)
   - Retry setup

3. **Use Pre-built Executable**
   - Skip Python setup entirely
   - Use the standalone .exe file (when available)

### Debug Information to Collect:
If you need help, collect this info:

```bash
# Run these commands and save the output:
python --version
pip --version  
python -c "import sys; print(sys.executable)"
python -c "import platform; print(platform.platform())"
pip list
```

---

## 🎉 Success Indicators

You'll know everything is working when:
- ✅ `troubleshoot.bat` shows all ✓ marks
- ✅ `python main.py --validate` passes all checks
- ✅ GUI opens without errors
- ✅ You can process a sample PDF file

**The app is designed to be forgiving - even if some optional packages fail, the core functionality will still work!**
