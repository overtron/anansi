#!/bin/bash

# Netflix Theme Extraction Script Runner
# This script runs the theme_extractor.py script with the necessary arguments

# Check if running in a virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Warning: It is recommended to run this script in a Python virtual environment."
    echo "See the README.md file for instructions on setting up a virtual environment."
    read -p "Continue without a virtual environment? (y/n): " continue_without_venv
    if [ "$continue_without_venv" != "y" ]; then
        echo "Exiting. Please set up a virtual environment before running this script."
        exit 1
    fi
    echo ""
fi

# Check if OpenAI API key is provided
if [ -z "$1" ]; then
    echo "Error: OpenAI API key is required"
    echo "Usage: ./run_theme_extractor.sh YOUR_OPENAI_API_KEY [input_dir] [output_dir]"
    exit 1
fi

# Set default values
API_KEY="$1"
INPUT_DIR="${2:-trackedcompanies/Netflix}"
OUTPUT_DIR="${3:-output}"

# Print information
echo "Running Netflix Theme Extraction Script"
echo "Input directory: $INPUT_DIR"
echo "Output directory: $OUTPUT_DIR"
echo ""

# Run the script
python theme_extractor.py --api-key "$API_KEY" --input-dir "$INPUT_DIR" --output-dir "$OUTPUT_DIR"

# Check if the script ran successfully
if [ $? -eq 0 ]; then
    echo ""
    echo "Theme extraction completed successfully!"
    echo "Results are available in: $OUTPUT_DIR/netflix_themes.md"
else
    echo ""
    echo "Error: Theme extraction failed"
    exit 1
fi
