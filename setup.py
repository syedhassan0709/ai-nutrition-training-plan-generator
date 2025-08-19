"""
Installation and Setup Script for Nutrition App
Run this script to set up the application environment.
"""

import subprocess
import sys
import os
import platform
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print(f"✗ Python 3.10+ required. Current version: {version.major}.{version.minor}")
        return False
    print(f"✓ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True


def install_dependencies():
    """Install required Python packages."""
    print("\nInstalling Python dependencies...")
    
    # Upgrade pip first
    if not run_command(f"{sys.executable} -m pip install --upgrade pip", 
                      "Upgrading pip"):
        return False
    
    # Install packages from requirements.txt
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", 
                      "Installing required packages"):
        return False
    
    return True


def create_directories():
    """Create necessary directories."""
    print("\nCreating application directories...")
    
    directories = [
        "output",
        "templates", 
        "charts",
        "logs",
        "models",
        "assets"
    ]
    
    for directory in directories:
        try:
            Path(directory).mkdir(exist_ok=True)
            print(f"✓ Created directory: {directory}")
        except Exception as e:
            print(f"✗ Failed to create directory {directory}: {e}")
            return False
    
    return True


def download_sample_model():
    """Download a sample local LLM model (optional)."""
    print("\nLocal LLM model download (optional)...")
    print("This will download a ~3GB model file for offline use.")
    
    response = input("Download GPT4All model? (y/N): ").lower().strip()
    
    if response == 'y':
        try:
            print("Downloading GPT4All model (this may take a while)...")
            import gpt4all
            
            # This will download the model if it doesn't exist
            model = gpt4all.GPT4All("ggml-gpt4all-j-v1.3-groovy.bin")
            print("✓ GPT4All model downloaded successfully")
            return True
            
        except ImportError:
            print("⚠ GPT4All not available. Skipping model download.")
            return True
        except Exception as e:
            print(f"✗ Failed to download model: {e}")
            return False
    else:
        print("⚠ Skipping model download. You can use cloud APIs instead.")
        return True


def test_installation():
    """Test if the installation is working."""
    print("\nTesting installation...")
    
    try:
        # Test imports
        import fitz
        print("✓ PyMuPDF (PDF processing) available")
    except ImportError:
        print("✗ PyMuPDF not available")
        return False
    
    try:
        from docx import Document
        print("✓ python-docx (Word documents) available")
    except ImportError:
        print("✗ python-docx not available")
        return False
    
    try:
        import matplotlib.pyplot as plt
        print("✓ matplotlib (charts) available")
    except ImportError:
        print("✗ matplotlib not available")
        return False
    
    try:
        import numpy as np
        print("✓ numpy (numerical computing) available")
    except ImportError:
        print("✗ numpy not available")
        return False
    
    try:
        import requests
        print("✓ requests (API communication) available")
    except ImportError:
        print("✗ requests not available")
        return False
    
    try:
        import tkinter as tk
        print("✓ tkinter (GUI) available")
    except ImportError:
        print("✗ tkinter not available (install python3-tk on Linux)")
        return False
    
    # Test optional imports
    try:
        import gpt4all
        print("✓ GPT4All (local LLM) available")
    except ImportError:
        print("⚠ GPT4All not available (cloud APIs can be used instead)")
    
    return True


def create_desktop_shortcut():
    """Create desktop shortcut (Windows only)."""
    if platform.system() != "Windows":
        return True
    
    print("\nCreate desktop shortcut...")
    response = input("Create desktop shortcut? (y/N): ").lower().strip()
    
    if response == 'y':
        try:
            import winshell
            from win32com.client import Dispatch
            
            desktop = winshell.desktop()
            path = os.path.join(desktop, "Nutrition App.lnk")
            target = os.path.join(os.getcwd(), "main.py")
            wDir = os.getcwd()
            icon = target
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = sys.executable
            shortcut.Arguments = f'"{target}"'
            shortcut.WorkingDirectory = wDir
            shortcut.IconLocation = icon
            shortcut.save()
            
            print("✓ Desktop shortcut created")
            return True
            
        except ImportError:
            print("⚠ Cannot create shortcut (pywin32 not available)")
            return True
        except Exception as e:
            print(f"✗ Failed to create shortcut: {e}")
            return True
    
    return True


def main():
    """Main setup function."""
    print("=" * 60)
    print("NUTRITION & TRAINING PLAN GENERATOR")
    print("Setup and Installation Script")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        print("\nPlease install Python 3.10 or higher and try again.")
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        print("\nSetup failed during directory creation.")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\nSetup failed during dependency installation.")
        print("You may need to run this script as administrator.")
        sys.exit(1)
    
    # Test installation
    if not test_installation():
        print("\nSetup completed with errors. Some features may not work.")
        print("Please check the error messages above.")
    else:
        print("\n✓ All core components installed successfully!")
    
    # Optional: Download local model
    download_sample_model()
    
    # Optional: Create desktop shortcut
    create_desktop_shortcut()
    
    print("\n" + "=" * 60)
    print("SETUP COMPLETE!")
    print("=" * 60)
    print("\nTo run the application:")
    print("  GUI Mode: python main.py")
    print("  CLI Mode: python main.py --cli sample.pdf")
    print("  Validate: python main.py --validate")
    print("\nFor help: python main.py --help")
    print("\nSee README.md for detailed usage instructions.")
    print("=" * 60)


if __name__ == "__main__":
    main()
