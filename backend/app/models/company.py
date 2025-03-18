from pydantic import BaseModel, Field
from typing import List, Optional

class CompanyBase(BaseModel):
    """Base model for company data"""
    id: str = Field(..., description="Company ID (e.g., 'netflix', 'roku')")
    name: str = Field(..., description="Company name (e.g., 'Netflix', 'Roku')")
    description: Optional[str] = Field(None, description="Company description")
    logo_url: Optional[str] = Field(None, description="URL to company logo")

class Company(CompanyBase):
    """Model for a company with all fields"""
    
    class Config:
        from_attributes = True

class CompanyList(BaseModel):
    """Model for a list of companies"""
    companies: List[Company] = Field(..., description="List of companies")
