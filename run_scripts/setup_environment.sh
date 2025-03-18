#!/bin/bash

# Netflix Theme Extraction Environment Setup Script
# This script sets up a Python virtual environment and installs the required dependencies

echo "Setting up Netflix Theme Extraction environment..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in your PATH"
    echo "Please install Python 3 and try again"
    exit 1
fi

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv netflix-themes-env

# Check if virtual environment was created successfully
if [ ! -d "netflix-themes-env" ]; then
    echo "Error: Failed to create virtual environment"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source netflix-themes-env/bin/activate

# Check if activation was successful
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Error: Failed to activate virtual environment"
    exit 1
fi

# Install dependencies
echo "Installing required dependencies..."
pip install -r requirements.txt

# Check if installation was successful
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

echo ""
echo "Environment setup completed successfully!"
echo ""
echo "To activate the virtual environment in the future, run:"
echo "  source netflix-themes-env/bin/activate"
echo ""
echo "To run the theme extraction script, use:"
echo "  ./run_theme_extractor.sh YOUR_OPENAI_API_KEY"
echo ""
echo "To deactivate the virtual environment when you're done, run:"
echo "  deactivate"
