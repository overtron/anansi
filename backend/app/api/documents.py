from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional

from app.models.document import Document, DocumentList
from app.services.document_service import DocumentService

router = APIRouter()

def get_document_service():
    return DocumentService()

@router.get("/", response_model=List[Document])
async def get_all_documents(
    company_id: Optional[str] = Query(None, description="Filter documents by company ID"),
    document_service: DocumentService = Depends(get_document_service)
):
    """Get all documents, optionally filtered by company_id"""
    if company_id:
        return document_service.get_documents_by_company(company_id)
    return document_service.get_all_documents()

@router.get("/company/{company_id}", response_model=List[Document])
async def get_documents_by_company(
    company_id: str,
    document_service: DocumentService = Depends(get_document_service)
):
    """Get all documents for a specific company"""
    return document_service.get_documents_by_company(company_id)

@router.get("/{path:path}", response_model=Document)
async def get_document_by_path(path: str, document_service: DocumentService = Depends(get_document_service)):
    """Get a document by path"""
    document = document_service.get_document_by_path(path)
    if document is None:
        raise HTTPException(status_code=404, detail=f"Document with path '{path}' not found")
    return document
