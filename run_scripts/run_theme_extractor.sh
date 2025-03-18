#!/bin/bash

# Company Theme Extraction Script Runner
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

# Parse command line arguments
COMPANY_ID="netflix"
INPUT_DIR=""
OUTPUT_DIR="$PROJECT_ROOT/filingsdata/output"

# Function to display usage
usage() {
    echo "Usage: ./run_theme_extractor.sh [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -c, --company COMPANY_ID   Company ID (e.g., 'netflix', 'roku') (default: netflix)"
    echo "  -i, --input-dir DIR        Input directory containing documents"
    echo "  -o, --output-dir DIR       Output directory for results (default: filingsdata/output)"
    echo "  -h, --help                 Display this help message"
    exit 1
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        -c|--company)
            COMPANY_ID="$2"
            shift 2
            ;;
        -i|--input-dir)
            INPUT_DIR="$2"
            shift 2
            ;;
        -o|--output-dir)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo "Unknown option: $1"
            usage
            ;;
    esac
done

# Set default input directory based on company_id if not provided
if [ -z "$INPUT_DIR" ]; then
    INPUT_DIR="$PROJECT_ROOT/filingsdata/trackedcompanies/${COMPANY_ID^}"
fi

# Print information
echo "Running Theme Extraction Script for company: $COMPANY_ID"
echo "Input directory: $INPUT_DIR"
echo "Output directory: $OUTPUT_DIR"
echo ""

# Build command
CMD="python \"$PROJECT_ROOT/scripts/theme_extractor.py\" --api-key \"$OPENAI_API_KEY\" --company-id \"$COMPANY_ID\""

# Add optional arguments
if [ -n "$INPUT_DIR" ]; then
    CMD="$CMD --input-dir \"$INPUT_DIR\""
fi

if [ -n "$OUTPUT_DIR" ]; then
    CMD="$CMD --output-dir \"$OUTPUT_DIR\""
fi

# Run the script
eval $CMD

# Check if the script ran successfully
if [ $? -eq 0 ]; then
    echo ""
    echo "Theme extraction completed successfully!"
    echo "Results are available in: $OUTPUT_DIR/${COMPANY_ID}_themes.md"
else
    echo ""
    echo "Error: Theme extraction failed"
    exit 1
fi
