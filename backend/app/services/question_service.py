import os
import sys
import json
from typing import List, Dict, Any, Optional
import re

# Add the parent directory to sys.path to allow importing the theme_qa module
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Add the scripts directory to sys.path
scripts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "scripts")
sys.path.append(scripts_dir)

# Import models
from app.models.question import QuestionRequest, QuestionResponse

# Import the theme_qa module
import theme_qa

class QuestionService:
    """Service for handling questions about themes"""
    
    def __init__(self, api_key: str, input_dir: Optional[str] = None, output_dir: Optional[str] = None, cache_dir: Optional[str] = None):
        self.api_key = api_key
        self.input_dir = input_dir or os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "filingsdata", "trackedcompanies", "Netflix")
        self.output_dir = output_dir or os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "filingsdata", "output")
        self.cache_dir = cache_dir or os.path.join(self.output_dir, "cache")
        
        # Initialize ThemeQA
        self.theme_qa = theme_qa.ThemeQA(
            api_key=self.api_key,
            input_dir=self.input_dir,
            output_dir=self.output_dir,
            cache_dir=self.cache_dir
        )
        
        # Load documents
        self.theme_qa.load_documents()
    
    def answer_question(self, question_request: QuestionRequest) -> QuestionResponse:
        """Answer a question about themes"""
        # Get answer from ThemeQA
        answer = self.theme_qa.answer_question(question_request.question)
        
        # Extract sources from answer
        sources = self._extract_sources(answer)
        
        # Create response
        response = QuestionResponse(
            question=question_request.question,
            answer=answer,
            sources=sources
        )
        
        return response
    
    def _extract_sources(self, answer: str) -> List[str]:
        """Extract sources from answer text"""
        sources = []
        
        # Look for source patterns like "Source: filename.pdf"
        source_matches = re.findall(r"Source: ([^\n]+)", answer)
        for match in source_matches:
            if match not in sources:
                sources.append(match)
        
        # Look for document references like "Document X: filename.pdf"
        doc_matches = re.findall(r"Document \d+: ([^\n]+)", answer)
        for match in doc_matches:
            if match not in sources:
                sources.append(match)
        
        return sources
