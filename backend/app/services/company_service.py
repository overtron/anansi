import os
import json
from typing import List, Dict, Any, Optional

from app.models.company import Company

# Constants
DEFAULT_COMPANIES_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "filingsdata", "companies.json")

class CompanyService:
    """Service for managing companies"""
    
    def __init__(self, companies_file: str = DEFAULT_COMPANIES_FILE):
        self.companies_file = companies_file
        os.makedirs(os.path.dirname(self.companies_file), exist_ok=True)
        
        # Initialize with default companies if file doesn't exist
        if not os.path.exists(self.companies_file):
            self._initialize_default_companies()
    
    def get_all_companies(self) -> List[Company]:
        """Get all companies"""
        companies = self._load_companies()
        return companies
    
    def get_company_by_id(self, company_id: str) -> Optional[Company]:
        """Get a company by ID"""
        companies = self._load_companies()
        for company in companies:
            if company.id.lower() == company_id.lower():
                return company
        return None
    
    def create_company(self, company: Company) -> Company:
        """Create a new company"""
        companies = self._load_companies()
        
        # Check if company with same ID already exists
        for existing_company in companies:
            if existing_company.id.lower() == company.id.lower():
                raise ValueError(f"Company with ID '{company.id}' already exists")
        
        # Add company to list
        companies.append(company)
        
        # Save companies
        self._save_companies(companies)
        
        return company
    
    def update_company(self, company_id: str, company: Company) -> Optional[Company]:
        """Update an existing company"""
        companies = self._load_companies()
        
        # Find company with matching ID
        for i, existing_company in enumerate(companies):
            if existing_company.id.lower() == company_id.lower():
                # Replace company in list
                companies[i] = company
                
                # Save companies
                self._save_companies(companies)
                
                return company
        
        return None
    
    def delete_company(self, company_id: str) -> bool:
        """Delete a company"""
        companies = self._load_companies()
        
        # Find company with matching ID
        for i, existing_company in enumerate(companies):
            if existing_company.id.lower() == company_id.lower():
                # Remove company from list
                companies.pop(i)
                
                # Save companies
                self._save_companies(companies)
                
                return True
        
        return False
    
    def _load_companies(self) -> List[Company]:
        """Load companies from file"""
        if os.path.exists(self.companies_file):
            try:
                with open(self.companies_file, 'r', encoding='utf-8') as file:
                    company_data = json.load(file)
                    return [Company.model_validate(company) for company in company_data]
            except Exception as e:
                print(f"Error loading companies: {str(e)}")
                return self._get_default_companies()
        return self._get_default_companies()
    
    def _save_companies(self, companies: List[Company]) -> None:
        """Save companies to file"""
        try:
            with open(self.companies_file, 'w', encoding='utf-8') as file:
                company_data = [company.model_dump() for company in companies]
                json.dump(company_data, file, indent=2)
        except Exception as e:
            print(f"Error saving companies: {str(e)}")
    
    def _initialize_default_companies(self) -> None:
        """Initialize the companies file with default companies"""
        self._save_companies(self._get_default_companies())
    
    def _get_default_companies(self) -> List[Company]:
        """Get a list of default companies"""
        return [
            Company(
                id="netflix",
                name="Netflix",
                description="American subscription streaming service and production company",
                logo_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Netflix_2015_logo.svg/1920px-Netflix_2015_logo.svg.png"
            ),
            Company(
                id="roku",
                name="Roku",
                description="American manufacturer of digital media players for streaming",
                logo_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Roku_logo.svg/1920px-Roku_logo.svg.png"
            )
        ]
