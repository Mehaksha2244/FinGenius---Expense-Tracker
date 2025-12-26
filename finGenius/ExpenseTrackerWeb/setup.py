#!/usr/bin/env python3
"""
Setup script for Personal Expense Tracker
Automatically installs dependencies and sets up the application
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible!")
    return True

def install_tesseract():
    """Install Tesseract OCR based on the operating system"""
    system = platform.system().lower()
    
    if system == "windows":
        print("🔄 Please install Tesseract OCR manually on Windows:")
        print("1. Download from: https://github.com/UB-Mannheim/tesseract/wiki")
        print("2. Install and add to PATH")
        print("3. Update the path in ocr_processor.py if needed")
        return True
    elif system == "darwin":  # macOS
        return run_command("brew install tesseract", "Installing Tesseract OCR")
    elif system == "linux":
        return run_command("sudo apt-get update && sudo apt-get install -y tesseract-ocr", "Installing Tesseract OCR")
    else:
        print(f"❌ Unsupported operating system: {system}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = [
        "static/receipts",
        "static/uploads",
        "logs"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def setup_database():
    """Initialize the database"""
    try:
        from database import DatabaseManager
        db = DatabaseManager()
        print("✅ Database initialized successfully!")
        return True
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Personal Expense Tracker...")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install Python dependencies
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        print("❌ Failed to install Python dependencies!")
        sys.exit(1)
    
    # Install Tesseract OCR
    if not install_tesseract():
        print("⚠️  Tesseract OCR installation failed, but continuing...")
        print("   You can install it manually later for receipt scanning.")
    
    # Create directories
    create_directories()
    
    # Setup database
    if not setup_database():
        print("❌ Database setup failed!")
        sys.exit(1)
    
    print("=" * 50)
    print("🎉 Setup completed successfully!")
    print("")
    print("To run the application:")
    print("  python app.py")
    print("")
    print("Then open your browser and go to:")
    print("  http://localhost:5000")
    print("")
    print("Happy expense tracking! 💰✨")

if __name__ == "__main__":
    main()
