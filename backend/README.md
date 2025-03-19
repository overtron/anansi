# Company Theme Analysis Backend API

This is the backend API for the Company Theme Extraction and Question-Answering System. It provides endpoints for accessing themes, asking questions, and managing documents extracted from company investor relations materials.

## Features

- **RESTful API**: Clean, well-structured API endpoints following REST principles
- **Theme Management**: CRUD operations for business themes
- **Question Answering**: AI-powered answers to questions about business themes
- **Document Management**: Access to source documents used for theme extraction
- **Multi-Company Support**: API endpoints support multiple companies
- **FastAPI Framework**: Built with FastAPI for high performance and automatic OpenAPI documentation

## Prerequisites

- Python 3.8+
- OpenAI API key
- Source documents organized by company

## Installation

1. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set your OpenAI API key:

```bash
export OPENAI_API_KEY=your-api-key  # On Windows: set OPENAI_API_KEY=your-api-key
```

## Running the Server

To run the development server:

```bash
python run.py
```

The API will be available at [http://localhost:8000](http://localhost:8000).

## API Documentation

Once the server is running, you can access the auto-generated API documentation at:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## API Endpoints

### Themes

- `GET /api/themes`: Get all themes for a company
- `GET /api/themes/{theme_id}`: Get a specific theme
- `POST /api/themes`: Create a new theme
- `PUT /api/themes/{theme_id}`: Update a theme
- `DELETE /api/themes/{theme_id}`: Delete a theme

### Questions

- `POST /api/questions/ask`: Ask a question about themes

### Documents

- `GET /api/documents`: Get all documents for a company
- `GET /api/documents/{document_id}`: Get a specific document

### Companies

- `GET /api/companies`: Get all companies
- `GET /api/companies/{company_id}`: Get a specific company

## Project Structure

```
backend/
├── app/                # FastAPI application
│   ├── api/            # API routers
│   │   ├── __init__.py
│   │   ├── companies.py
│   │   ├── documents.py
│   │   ├── questions.py
│   │   └── themes.py
│   ├── models/         # Data models
│   │   ├── __init__.py
│   │   ├── company.py
│   │   ├── document.py
│   │   ├── question.py
│   │   └── theme.py
│   ├── services/       # Business logic
│   │   ├── __init__.py
│   │   ├── company_service.py
│   │   ├── document_service.py
│   │   ├── question_service.py
│   │   └── theme_service.py
│   ├── __init__.py
│   └── main.py         # FastAPI app initialization
├── requirements.txt    # Dependencies
└── run.py              # Server startup script
```

## Development

### Adding a New Endpoint

1. Define the route in the appropriate router file in `app/api/`
2. Implement the business logic in the corresponding service file in `app/services/`
3. Define any necessary data models in `app/models/`

### Code Style

This project follows PEP 8 style guidelines. You can use tools like `flake8` and `black` to ensure your code adheres to these standards.

## Deployment

For production deployment, consider:

1. Using a production ASGI server like Uvicorn or Hypercorn behind a reverse proxy like Nginx
2. Setting up proper authentication and HTTPS
3. Using environment variables for configuration
4. Implementing proper logging and monitoring

Example deployment with Uvicorn:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
