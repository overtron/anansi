# Netflix Theme Extraction and Question-Answering System with Web Interface

This project provides a complete system for extracting business themes from Netflix's investor relations documents and SEC filings, and a web interface for exploring these themes and asking questions about them.

## System Components

The system consists of three main components:

1. **Theme Extraction Scripts**: Python scripts for extracting business themes from source documents
2. **Backend API**: FastAPI server that provides endpoints for accessing themes, asking questions, and managing documents
3. **Frontend Web Interface**: React application for exploring themes and asking questions

## Features

- **Theme Extraction**: Extract business growth/contraction themes from Netflix documents
- **Theme Exploration**: Browse through extracted themes organized by category
- **Question Answering**: Ask questions about themes and get AI-powered answers
- **Document Management**: View the source documents used for theme extraction
- **Manual Theme Addition**: Add custom themes that will be preserved during updates
- **Document Caching**: Efficiently cache extracted text and embeddings to speed up repeated operations

## Prerequisites

- Python 3.8+ (for backend and theme extraction)
- Node.js and npm (for frontend)
- OpenAI API key
- Source documents (investor relations PDFs and SEC filings)

## Quick Start

### 1. Set Up the Backend

```bash
# Navigate to the backend directory
cd filingsdata/backend

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY=your-api-key  # On Windows: set OPENAI_API_KEY=your-api-key

# Run the backend server
python run.py
```

The backend API will be available at [http://localhost:8000](http://localhost:8000).

### 2. Set Up the Frontend

```bash
# Navigate to the frontend directory
cd filingsdata/frontend

# Install dependencies
npm install

# Run the development server
npm start
```

The frontend will be available at [http://localhost:3000](http://localhost:3000).

## Directory Structure

```
filingsdata/
├── backend/                # Backend API
│   ├── app/                # FastAPI application
│   │   ├── api/            # API routers
│   │   ├── models/         # Data models
│   │   └── services/       # Business logic
│   ├── requirements.txt    # Backend dependencies
│   └── README.md           # Backend documentation
├── frontend/               # Frontend web interface
│   ├── public/             # Static files
│   ├── src/                # Source code
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   └── services/       # API services
│   ├── package.json        # Frontend dependencies
│   └── README.md           # Frontend documentation
├── output/                 # Output files from theme extraction
│   ├── themes.json         # Extracted themes in JSON format
│   └── netflix_themes.md   # Formatted markdown of themes
├── trackedcompanies/       # Source documents
│   └── Netflix/            # Netflix documents
│       ├── investorrelations/  # Investor relations PDFs
│       └── sec-submissions/    # SEC filings
├── theme_extractor.py      # Theme extraction script
├── theme_qa.py             # Question-answering script
├── add_manual_theme.py     # Script for adding manual themes
├── run_theme_extractor.sh  # Script to run theme extraction
├── run_theme_qa.sh         # Script to run question answering
└── README.md               # This file
```

## Detailed Documentation

- [Backend API Documentation](./backend/README.md)
- [Frontend Documentation](./frontend/README.md)
- [Theme Extraction Documentation](./README_ORIGINAL.md)

## Using the System

### Extracting Themes

Before using the web interface, you need to extract themes from the source documents. You can do this using the theme_extractor.py script:

```bash
# Run the theme extraction script
python theme_extractor.py --api-key YOUR_OPENAI_API_KEY
```

Or use the provided shell script:

```bash
# Make the script executable (if not already)
chmod +x run_theme_extractor.sh

# Run the script
./run_theme_extractor.sh YOUR_OPENAI_API_KEY
```

### Using the Web Interface

Once the backend and frontend are running, you can access the web interface at [http://localhost:3000](http://localhost:3000).

The web interface provides the following pages:

- **Home**: Overview of the system
- **Themes**: Browse and search extracted themes
- **Ask Questions**: Ask questions about themes and get AI-powered answers
- **Documents**: View the source documents used for theme extraction
- **Add Theme**: Add a manual theme

### Using the Question-Answering Script with Caching

The question-answering script now supports caching to improve performance for repeated operations. When you run the script, it will:

1. Cache extracted text from documents
2. Cache document embeddings in a vector database
3. Only reprocess documents that have changed since the last run

You can use the following options with the `run_theme_qa.sh` script:

```bash
# Basic usage
./run_theme_qa.sh -k YOUR_OPENAI_API_KEY -q "Your question here"

# Specify a custom cache directory
./run_theme_qa.sh -k YOUR_OPENAI_API_KEY -q "Your question here" -c "custom/cache/dir"

# Force reprocessing of all documents (invalidate cache)
./run_theme_qa.sh -k YOUR_OPENAI_API_KEY -q "Your question here" -r

# Get help with all options
./run_theme_qa.sh -h
```

For Windows users, the `run_theme_qa.bat` script provides the same functionality:

```batch
run_theme_qa.bat -k YOUR_OPENAI_API_KEY -q "Your question here"
```

The caching system significantly improves performance for repeated questions and when processing the same documents multiple times.

## Development

For development instructions, see the README files in the backend and frontend directories.

## Deployment

For production deployment, consider:

1. Building the frontend for production:

```bash
cd filingsdata/frontend
npm run build
```

2. Serving the frontend build directory with a static file server or CDN

3. Deploying the backend API to a production environment with proper authentication and HTTPS

## License

This project is licensed under the MIT License - see the LICENSE file for details.
