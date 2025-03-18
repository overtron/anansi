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
from app.services.company_service import CompanyService

# Import the theme_qa module
import theme_qa

class QuestionService:
    """Service for handling questions about themes"""
    
    def __init__(self, api_key: str, company_id: Optional[str] = None, input_dir: Optional[str] = None, output_dir: Optional[str] = None, cache_dir: Optional[str] = None):
        self.api_key = api_key
        self.company_id = company_id
        self.trackedcompanies_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "filingsdata", "trackedcompanies")
        self.output_dir = output_dir or os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "filingsdata", "output")
        self.cache_dir = cache_dir or os.path.join(self.output_dir, "cache")
        self.company_service = CompanyService()
        
        # Set input directory based on company_id
        if company_id:
            self.input_dir = input_dir or os.path.join(self.trackedcompanies_dir, company_id.capitalize())
        else:
            self.input_dir = input_dir or os.path.join(self.trackedcompanies_dir, "Netflix")
        
        # Initialize ThemeQA
        self.theme_qa = theme_qa.ThemeQA(
            api_key=self.api_key,
            input_dir=self.input_dir,
            output_dir=self.output_dir,
            cache_dir=self.cache_dir
        )
        
        # Load documents
        self.theme_qa.load_documents()
    
    def answer_question(self, question_request: QuestionRequest, company_id: Optional[str] = None) -> QuestionResponse:
        """Answer a question about themes for a specific company"""
        # Use provided company_id or the one set in the constructor
        company_id = company_id or self.company_id
        
        # If company_id has changed, reinitialize ThemeQA with the new input directory
        if company_id and (not self.company_id or company_id != self.company_id):
            self.company_id = company_id
            self.input_dir = os.path.join(self.trackedcompanies_dir, company_id.capitalize())
            
            # Reinitialize ThemeQA
            self.theme_qa = theme_qa.ThemeQA(
                api_key=self.api_key,
                input_dir=self.input_dir,
                output_dir=self.output_dir,
                cache_dir=self.cache_dir
            )
            
            # Load documents
            self.theme_qa.load_documents()
        
        # Get company name for context
        company_name = company_id.capitalize() if company_id else "Netflix"
        if company_id:
            company = self.company_service.get_company_by_id(company_id)
            if company:
                company_name = company.name
        
        # Add company context to the question
        contextualized_question = f"Question about {company_name}: {question_request.question}"
        
        # Get answer from ThemeQA
        answer = self.theme_qa.answer_question(contextualized_question)
        
        # Extract sources from answer
        sources = self._extract_sources(answer)
        
        # Create response
        response = QuestionResponse(
            question=question_request.question,
            answer=answer,
            sources=sources,
            company_id=company_id
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
