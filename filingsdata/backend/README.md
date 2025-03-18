# Netflix Themes Backend API

This is the backend API for the Netflix Theme Extraction and Question-Answering System. It provides endpoints for accessing themes, asking questions, and managing documents.

## Features

- **Theme Management**: Get, create, update, and delete themes
- **Question Answering**: Ask questions about themes and get AI-powered answers
- **Document Management**: Get information about source documents
- **OpenAI Integration**: Uses OpenAI's GPT-4o model for theme extraction and question answering

## Prerequisites

- Python 3.8+
- OpenAI API key
- Source documents (investor relations PDFs and SEC filings)

## Installation

1. Create a virtual environment (recommended):

```bash
cd filingsdata/backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

The API requires an OpenAI API key for theme extraction and question answering. You can provide it in one of two ways:

1. Set it as an environment variable:

```bash
# On Unix/macOS
export OPENAI_API_KEY=your-api-key

# On Windows
set OPENAI_API_KEY=your-api-key
```

2. Pass it directly when running the API (see below)

## Running the API

To run the API in development mode:

```bash
cd filingsdata/backend
python run.py
```

This will start the FastAPI server at [http://localhost:8000](http://localhost:8000).

You can also run the API with uvicorn directly:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once the API is running, you can access the auto-generated documentation at:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## API Endpoints

### Themes

- `GET /api/themes`: Get all themes
- `GET /api/themes/{name}`: Get a theme by name
- `POST /api/themes`: Create a new theme
- `PUT /api/themes/{name}`: Update a theme
- `DELETE /api/themes/{name}`: Delete a theme

### Questions

- `POST /api/questions/ask`: Ask a question about themes

### Documents

- `GET /api/documents`: Get all documents
- `GET /api/documents/{path}`: Get a document by path

## Project Structure

- `app/`: Main application package
  - `main.py`: FastAPI application entry point
  - `api/`: API routers
  - `models/`: Pydantic models for request/response validation
  - `services/`: Business logic services
- `run.py`: Script to run the API

## Integration with Theme Extraction

The backend integrates with the existing theme extraction and question-answering scripts:

- `theme_extractor.py`: Extracts themes from source documents
- `theme_qa.py`: Answers questions about themes using source documents

## Deployment

The API can be deployed to any platform that supports Python applications. Some options include:

- Docker container on any cloud platform
- Heroku
- AWS Lambda with API Gateway
- Google Cloud Run
- Azure App Service

For production deployment, consider:

1. Using a production ASGI server like Gunicorn with Uvicorn workers
2. Setting up proper authentication and HTTPS
3. Restricting CORS to only allow requests from your frontend domain
