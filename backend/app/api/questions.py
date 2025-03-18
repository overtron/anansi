from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
import os

from app.models.question import QuestionRequest, QuestionResponse
from app.services.question_service import QuestionService

router = APIRouter()

# Get OpenAI API key from environment variable or use a dummy key for development
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "dummy-key")

# Default paths
DEFAULT_TRACKEDCOMPANIES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "filingsdata", "trackedcompanies")
DEFAULT_OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "filingsdata", "output")
DEFAULT_CACHE_DIR = os.path.join(DEFAULT_OUTPUT_DIR, "cache")

def get_question_service(company_id: Optional[str] = None):
    """Get a question service instance, optionally for a specific company"""
    return QuestionService(
        api_key=OPENAI_API_KEY,
        company_id=company_id,
        output_dir=DEFAULT_OUTPUT_DIR,
        cache_dir=DEFAULT_CACHE_DIR
    )

@router.post("/ask", response_model=QuestionResponse)
async def ask_question(
    question_request: QuestionRequest,
    company_id: Optional[str] = Query(None, description="ID of the company to ask about"),
    question_service: QuestionService = Depends(get_question_service)
):
    """Ask a question about themes, optionally for a specific company"""
    try:
        # Use company_id from query parameter or from request body
        company_id = company_id or question_request.company_id
        return question_service.answer_question(question_request, company_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error answering question: {str(e)}")

@router.post("/company/{company_id}/ask", response_model=QuestionResponse)
async def ask_question_for_company(
    company_id: str,
    question_request: QuestionRequest
):
    """Ask a question about themes for a specific company"""
    try:
        # Create a question service for this company
        question_service = get_question_service(company_id)
        return question_service.answer_question(question_request, company_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error answering question for company {company_id}: {str(e)}")
