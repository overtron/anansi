from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional

from app.models.company import Company
from app.services.company_service import CompanyService

router = APIRouter()

def get_company_service():
    return CompanyService()

@router.get("/", response_model=List[Company])
async def get_all_companies(company_service: CompanyService = Depends(get_company_service)):
    """Get all companies"""
    return company_service.get_all_companies()

@router.get("/{company_id}", response_model=Company)
async def get_company_by_id(company_id: str, company_service: CompanyService = Depends(get_company_service)):
    """Get a company by ID"""
    company = company_service.get_company_by_id(company_id)
    if company is None:
        raise HTTPException(status_code=404, detail=f"Company with ID '{company_id}' not found")
    return company

@router.post("/", response_model=Company)
async def create_company(company: Company, company_service: CompanyService = Depends(get_company_service)):
    """Create a new company"""
    try:
        return company_service.create_company(company)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{company_id}", response_model=Company)
async def update_company(company_id: str, company: Company, company_service: CompanyService = Depends(get_company_service)):
    """Update an existing company"""
    updated_company = company_service.update_company(company_id, company)
    if updated_company is None:
        raise HTTPException(status_code=404, detail=f"Company with ID '{company_id}' not found")
    return updated_company

@router.delete("/{company_id}")
async def delete_company(company_id: str, company_service: CompanyService = Depends(get_company_service)):
    """Delete a company"""
    success = company_service.delete_company(company_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Company with ID '{company_id}' not found")
    return {"message": f"Company '{company_id}' deleted successfully"}
