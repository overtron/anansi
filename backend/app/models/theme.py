from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ThemeBase(BaseModel):
    """Base model for theme data"""
    name: str = Field(..., description="Theme name (1-5 words)")
    description: str = Field(..., description="Theme description")
    category: str = Field("General", description="Theme category")
    company_id: str = Field(..., description="ID of the company this theme belongs to")

class ThemeCreate(ThemeBase):
    """Model for creating a new theme"""
    pass

class Theme(ThemeBase):
    """Model for a theme with all fields"""
    evidence: Optional[str] = Field(None, description="Evidence supporting the theme")
    source: Optional[str] = Field(None, description="Source document for the theme")
    
    class Config:
        from_attributes = True

class ThemeList(BaseModel):
    """Model for a list of themes"""
    themes: List[Theme] = Field(..., description="List of themes")
