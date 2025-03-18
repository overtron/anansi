#!/bin/bash

# Netflix Theme Question-Answering Script Runner
# This script runs the theme_qa.py script with the necessary arguments

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
API_KEY=""
QUESTION=""
INPUT_DIR="trackedcompanies/Netflix"
OUTPUT_DIR="output"
CACHE_DIR=""
INVALIDATE_CACHE=false

# Function to display usage
usage() {
    echo "Usage: ./run_theme_qa.sh [OPTIONS]"
    echo ""
    echo "Required options:"
    echo "  -k, --api-key KEY       OpenAI API key"
    echo "  -q, --question TEXT     Question to answer"
    echo ""
    echo "Optional options:"
    echo "  -i, --input-dir DIR     Input directory containing documents (default: trackedcompanies/Netflix)"
    echo "  -o, --output-dir DIR    Output directory for themes and cache (default: output)"
    echo "  -c, --cache-dir DIR     Directory to store cache files (default: output/cache)"
    echo "  -r, --refresh           Invalidate cache and reprocess all documents"
    echo "  -h, --help              Display this help message"
    exit 1
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        -k|--api-key)
            API_KEY="$2"
            shift 2
            ;;
        -q|--question)
            QUESTION="$2"
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
        -c|--cache-dir)
            CACHE_DIR="$2"
            shift 2
            ;;
        -r|--refresh)
            INVALIDATE_CACHE=true
            shift
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

# Check required arguments
if [ -z "$API_KEY" ]; then
    echo "Error: OpenAI API key is required"
    usage
fi

if [ -z "$QUESTION" ]; then
    echo "Error: Question is required"
    usage
fi

# Build command
CMD="python theme_qa.py --api-key \"$API_KEY\" --question \"$QUESTION\" --input-dir \"$INPUT_DIR\" --output-dir \"$OUTPUT_DIR\""

# Add optional arguments
if [ -n "$CACHE_DIR" ]; then
    CMD="$CMD --cache-dir \"$CACHE_DIR\""
fi

if [ "$INVALIDATE_CACHE" = true ]; then
    CMD="$CMD --invalidate-cache"
fi

# Print information
echo "Running Netflix Theme Question-Answering Script"
echo "Question: $QUESTION"
echo "Input directory: $INPUT_DIR"
echo "Output directory: $OUTPUT_DIR"
if [ -n "$CACHE_DIR" ]; then
    echo "Cache directory: $CACHE_DIR"
fi
if [ "$INVALIDATE_CACHE" = true ]; then
    echo "Cache will be invalidated"
fi
echo ""
echo "Loading documents and generating answer... (this may take a few minutes)"
echo ""

# Run the script
eval $CMD

# Check if the script ran successfully
if [ $? -eq 0 ]; then
    echo ""
    echo "Question answered successfully!"
else
    echo ""
    echo "Error: Failed to answer question"
    exit 1
fi
