import os
import sys
import json
import hashlib
from typing import List, Dict, Any, Optional
from datetime import datetime

# Add the parent directory to sys.path to allow importing the theme_extractor module
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Add the scripts directory to sys.path
scripts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "scripts")
sys.path.append(scripts_dir)

# Import models
from app.models.document import Document, DocumentList
from app.services.company_service import CompanyService

# Constants
DEFAULT_PROCESSED_FILES_JSON = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "filingsdata", "output", "processed_files.json")
DEFAULT_TRACKEDCOMPANIES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "filingsdata", "trackedcompanies")

class DocumentService:
    """Service for managing documents"""
    
    def __init__(self, 
                 trackedcompanies_dir: str = DEFAULT_TRACKEDCOMPANIES_DIR, 
                 processed_files_json: str = DEFAULT_PROCESSED_FILES_JSON,
                 company_id: Optional[str] = None):
        self.trackedcompanies_dir = trackedcompanies_dir
        self.processed_files_json = processed_files_json
        self.company_id = company_id
        self.company_service = CompanyService()
        os.makedirs(os.path.dirname(self.processed_files_json), exist_ok=True)
    
    def get_all_documents(self, company_id: Optional[str] = None) -> List[Document]:
        """Get all documents, optionally filtered by company_id"""
        # Use provided company_id or the one set in the constructor
        company_id = company_id or self.company_id
        
        # Get processed files info
        processed_files = self._load_processed_files()
        
        # Find all PDF and JSON files
        documents = []
        
        # If company_id is provided, only look in that company's directory
        if company_id:
            company_dir = os.path.join(self.trackedcompanies_dir, company_id.capitalize())
            if not os.path.exists(company_dir):
                return []
            self._process_company_directory(company_dir, company_id, processed_files, documents)
        else:
            # Otherwise, look in all company directories
            for company in self.company_service.get_all_companies():
                company_dir = os.path.join(self.trackedcompanies_dir, company.name)
                if os.path.exists(company_dir):
                    self._process_company_directory(company_dir, company.id, processed_files, documents)
        
        return documents
    
    def _process_company_directory(self, company_dir: str, company_id: str, processed_files: Dict, documents: List[Document]) -> None:
        """Process a company directory and add documents to the list"""
        for root, _, files in os.walk(company_dir):
            for file in files:
                file_path = os.path.join(root, file)
                
                if file.lower().endswith('.pdf') or file.lower().endswith('.json'):
                    # Get file hash
                    file_hash = self._get_file_hash(file_path)
                    
                    # Check if file has been processed
                    processed = file_path in processed_files
                    processed_date = None
                    
                    if processed:
                        # Convert timestamp to datetime if available
                        if isinstance(processed_files[file_path], dict) and "timestamp" in processed_files[file_path]:
                            try:
                                processed_date = datetime.fromisoformat(processed_files[file_path]["timestamp"])
                            except:
                                pass
                    
                    # Create document
                    document = Document(
                        company_id=company_id,
                        filename=file,
                        path=file_path,
                        type=file.split('.')[-1].upper(),
                        processed=processed,
                        processed_date=processed_date,
                        hash=file_hash
                    )
                    
                    documents.append(document)
    
    def get_document_by_path(self, path: str) -> Optional[Document]:
        """Get a document by path"""
        documents = self.get_all_documents()
        for document in documents:
            if document.path == path:
                return document
        return None
    
    def get_documents_by_company(self, company_id: str) -> List[Document]:
        """Get all documents for a specific company"""
        return self.get_all_documents(company_id)
    
    def _load_processed_files(self) -> Dict[str, Any]:
        """Load information about processed files"""
        if os.path.exists(self.processed_files_json):
            try:
                with open(self.processed_files_json, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except Exception as e:
                print(f"Error loading processed files info: {str(e)}")
                return {}
        return {}
    
    def _get_file_hash(self, file_path: str) -> str:
        """Calculate MD5 hash of a file to detect changes"""
        try:
            with open(file_path, 'rb') as file:
                return hashlib.md5(file.read()).hexdigest()
        except Exception as e:
            print(f"Error calculating file hash: {str(e)}")
            return ""
