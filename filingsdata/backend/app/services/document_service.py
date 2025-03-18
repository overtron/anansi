import os
import sys
import json
import hashlib
from typing import List, Dict, Any, Optional
from datetime import datetime

# Add the parent directory to sys.path to allow importing the theme_extractor module
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Add the backend directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import models
from app.models.document import Document, DocumentList

# Constants
DEFAULT_PROCESSED_FILES_JSON = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "output", "processed_files.json")
DEFAULT_DOCUMENTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "trackedcompanies", "Netflix")

class DocumentService:
    """Service for managing documents"""
    
    def __init__(self, documents_dir: str = DEFAULT_DOCUMENTS_DIR, processed_files_json: str = DEFAULT_PROCESSED_FILES_JSON):
        self.documents_dir = documents_dir
        self.processed_files_json = processed_files_json
        os.makedirs(os.path.dirname(self.processed_files_json), exist_ok=True)
    
    def get_all_documents(self) -> List[Document]:
        """Get all documents"""
        # Get processed files info
        processed_files = self._load_processed_files()
        
        # Find all PDF and JSON files
        documents = []
        
        for root, _, files in os.walk(self.documents_dir):
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
                        filename=file,
                        path=file_path,
                        type=file.split('.')[-1].upper(),
                        processed=processed,
                        processed_date=processed_date,
                        hash=file_hash
                    )
                    
                    documents.append(document)
        
        return documents
    
    def get_document_by_path(self, path: str) -> Optional[Document]:
        """Get a document by path"""
        documents = self.get_all_documents()
        for document in documents:
            if document.path == path:
                return document
        return None
    
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
