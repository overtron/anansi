from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional

from app.models.document import Document, DocumentList
from app.services.document_service import DocumentService

router = APIRouter()

def get_document_service():
    return DocumentService()

@router.get("/", response_model=List[Document])
async def get_all_documents(document_service: DocumentService = Depends(get_document_service)):
    """Get all documents"""
    return document_service.get_all_documents()

@router.get("/{path:path}", response_model=Document)
async def get_document_by_path(path: str, document_service: DocumentService = Depends(get_document_service)):
    """Get a document by path"""
    document = document_service.get_document_by_path(path)
    if document is None:
        raise HTTPException(status_code=404, detail=f"Document with path '{path}' not found")
    return document
