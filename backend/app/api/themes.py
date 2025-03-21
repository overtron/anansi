from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional

from app.models.theme import Theme, ThemeCreate, ThemeList
from app.services.theme_service import ThemeService

router = APIRouter()

def get_theme_service():
    return ThemeService()

@router.get("/", response_model=List[Theme])
async def get_all_themes(
    company_id: Optional[str] = Query(None, description="Filter themes by company ID"),
    theme_service: ThemeService = Depends(get_theme_service)
):
    """Get all themes, optionally filtered by company_id"""
    if company_id:
        return theme_service.get_themes_by_company(company_id)
    return theme_service.get_all_themes()

@router.get("/company/{company_id}", response_model=List[Theme])
async def get_themes_by_company(
    company_id: str,
    theme_service: ThemeService = Depends(get_theme_service)
):
    """Get all themes for a specific company"""
    return theme_service.get_themes_by_company(company_id)

@router.get("/{name}", response_model=Theme)
async def get_theme_by_name(
    name: str, 
    company_id: Optional[str] = Query(None, description="Filter by company ID"),
    theme_service: ThemeService = Depends(get_theme_service)
):
    """Get a theme by name, optionally filtered by company_id"""
    theme = theme_service.get_theme_by_name(name, company_id)
    if theme is None:
        raise HTTPException(status_code=404, detail=f"Theme with name '{name}' not found")
    return theme

@router.post("/", response_model=Theme)
async def create_theme(theme: ThemeCreate, theme_service: ThemeService = Depends(get_theme_service)):
    """Create a new theme"""
    try:
        return theme_service.create_theme(theme)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{name}", response_model=Theme)
async def update_theme(name: str, theme: ThemeCreate, theme_service: ThemeService = Depends(get_theme_service)):
    """Update an existing theme"""
    updated_theme = theme_service.update_theme(name, theme)
    if updated_theme is None:
        raise HTTPException(status_code=404, detail=f"Theme with name '{name}' not found for company '{theme.company_id}'")
    return updated_theme

@router.delete("/{name}")
async def delete_theme(
    name: str, 
    company_id: str = Query(..., description="Company ID of the theme to delete"),
    theme_service: ThemeService = Depends(get_theme_service)
):
    """Delete a theme"""
    success = theme_service.delete_theme(name, company_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Theme with name '{name}' not found for company '{company_id}'")
    return {"message": f"Theme '{name}' for company '{company_id}' deleted successfully"}
