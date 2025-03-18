#!/bin/bash

# Netflix Theme Extraction Script Runner
# This script runs the theme_extractor.py script with the necessary arguments

# Get the project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Load environment variables from .env file
if [ -f "$PROJECT_ROOT/.env" ]; then
    echo "Loading environment variables from .env file..."
    export $(grep -v '^#' "$PROJECT_ROOT/.env" | xargs)
else
    echo "Error: .env file not found in project root"
    echo "Please create a .env file with your OPENAI_API_KEY"
    echo "Example: OPENAI_API_KEY=your_api_key_here"
    exit 1
fi

# Check if OPENAI_API_KEY is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "Error: OPENAI_API_KEY not found in .env file"
    echo "Please add your OpenAI API key to the .env file"
    echo "Example: OPENAI_API_KEY=your_api_key_here"
    exit 1
fi

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

# Set default values
API_KEY="$OPENAI_API_KEY"
INPUT_DIR="${1:-$PROJECT_ROOT/filingsdata/trackedcompanies/Netflix}"
OUTPUT_DIR="${2:-$PROJECT_ROOT/filingsdata/output}"

# Print information
echo "Running Netflix Theme Extraction Script"
echo "Input directory: $INPUT_DIR"
echo "Output directory: $OUTPUT_DIR"
echo ""

# Run the script
python "$PROJECT_ROOT/scripts/theme_extractor.py" --api-key "$API_KEY" --input-dir "$INPUT_DIR" --output-dir "$OUTPUT_DIR"

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
