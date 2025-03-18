from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
import os

from app.models.question import QuestionRequest, QuestionResponse
from app.services.question_service import QuestionService

router = APIRouter()

# Get OpenAI API key from environment variable or use a dummy key for development
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "dummy-key")

# Default paths
DEFAULT_INPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "filingsdata", "trackedcompanies", "Netflix")
DEFAULT_OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "filingsdata", "output")
DEFAULT_CACHE_DIR = os.path.join(DEFAULT_OUTPUT_DIR, "cache")

def get_question_service():
    return QuestionService(
        api_key=OPENAI_API_KEY,
        input_dir=DEFAULT_INPUT_DIR,
        output_dir=DEFAULT_OUTPUT_DIR,
        cache_dir=DEFAULT_CACHE_DIR
    )

@router.post("/ask", response_model=QuestionResponse)
async def ask_question(question_request: QuestionRequest, question_service: QuestionService = Depends(get_question_service)):
    """Ask a question about themes"""
    try:
        return question_service.answer_question(question_request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error answering question: {str(e)}")
