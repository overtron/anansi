from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class Document(BaseModel):
    """Model for a document"""
    filename: str = Field(..., description="Document filename")
    path: str = Field(..., description="Document path")
    type: str = Field(..., description="Document type (PDF, JSON, etc.)")
    processed: bool = Field(False, description="Whether the document has been processed")
    processed_date: Optional[datetime] = Field(None, description="Date when the document was processed")
    hash: Optional[str] = Field(None, description="Document hash for change detection")
    
class DocumentList(BaseModel):
    """Model for a list of documents"""
    documents: List[Document] = Field(..., description="List of documents")
