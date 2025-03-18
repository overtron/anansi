from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class QuestionRequest(BaseModel):
    """Model for a question request"""
    question: str = Field(..., description="Question to answer")
    
class QuestionResponse(BaseModel):
    """Model for a question response"""
    question: str = Field(..., description="Original question")
    answer: str = Field(..., description="Answer to the question")
    sources: List[str] = Field(default_factory=list, description="Sources used to answer the question")
    
class QuestionHistory(BaseModel):
    """Model for question history"""
    questions: List[QuestionResponse] = Field(default_factory=list, description="List of previous questions and answers")
