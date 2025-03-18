import os
import json
import sys
from typing import List, Dict, Any, Optional
import hashlib
from datetime import datetime

# Add the parent directory to sys.path to allow importing the theme_extractor module
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Add the scripts directory to sys.path
scripts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "scripts")
sys.path.append(scripts_dir)

# Import models
from app.models.theme import Theme, ThemeCreate

# Constants
DEFAULT_OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "filingsdata", "output")

class ThemeService:
    """Service for managing themes"""
    
    def __init__(self, output_dir: str = DEFAULT_OUTPUT_DIR, company_id: Optional[str] = None):
        self.output_dir = output_dir
        self.company_id = company_id
        os.makedirs(self.output_dir, exist_ok=True)
    
    def get_themes_file(self, company_id: Optional[str] = None) -> str:
        """Get the path to the themes file for a specific company"""
        company_id = company_id or self.company_id or "netflix"  # Default to netflix if not specified
        return os.path.join(self.output_dir, f"{company_id}_themes.json")
    
    def get_all_themes(self, company_id: Optional[str] = None) -> List[Theme]:
        """Get all themes, optionally filtered by company_id"""
        company_id = company_id or self.company_id
        
        if company_id:
            # If company_id is provided, only return themes for that company
            return self._load_themes(company_id)
        else:
            # Otherwise, return themes for all companies
            all_themes = []
            
            # Look for theme files for all companies
            for file in os.listdir(self.output_dir):
                if file.endswith("_themes.json"):
                    company_id = file.replace("_themes.json", "")
                    all_themes.extend(self._load_themes(company_id))
            
            return all_themes
    
    def get_themes_by_company(self, company_id: str) -> List[Theme]:
        """Get all themes for a specific company"""
        return self._load_themes(company_id)
    
    def get_theme_by_name(self, name: str, company_id: Optional[str] = None) -> Optional[Theme]:
        """Get a theme by name, optionally filtered by company_id"""
        themes = self.get_all_themes(company_id)
        for theme in themes:
            if theme.name.lower() == name.lower():
                return theme
        return None
    
    def create_theme(self, theme: ThemeCreate) -> Theme:
        """Create a new theme"""
        company_id = theme.company_id
        themes = self._load_themes(company_id)
        
        # Check if theme with same name already exists for this company
        for existing_theme in themes:
            if existing_theme.name.lower() == theme.name.lower() and existing_theme.company_id == company_id:
                raise ValueError(f"Theme with name '{theme.name}' already exists for company '{company_id}'")
        
        # Create new theme
        new_theme = Theme(
            name=theme.name,
            description=theme.description,
            category=theme.category,
            company_id=company_id
        )
        
        # Add theme to list
        themes.append(new_theme)
        
        # Save themes
        self._save_themes(themes, company_id)
        
        return new_theme
    
    def update_theme(self, name: str, theme: ThemeCreate) -> Optional[Theme]:
        """Update an existing theme"""
        company_id = theme.company_id
        themes = self._load_themes(company_id)
        
        # Find theme with matching name and company_id
        for i, existing_theme in enumerate(themes):
            if existing_theme.name.lower() == name.lower() and existing_theme.company_id == company_id:
                # Update theme
                updated_theme = Theme(
                    name=theme.name,
                    description=theme.description,
                    category=theme.category,
                    company_id=company_id,
                    evidence=existing_theme.evidence,
                    source=existing_theme.source
                )
                
                # Replace theme in list
                themes[i] = updated_theme
                
                # Save themes
                self._save_themes(themes, company_id)
                
                return updated_theme
        
        return None
    
    def delete_theme(self, name: str, company_id: Optional[str] = None) -> bool:
        """Delete a theme"""
        company_id = company_id or self.company_id
        if not company_id:
            return False
            
        themes = self._load_themes(company_id)
        
        # Find theme with matching name and company_id
        for i, existing_theme in enumerate(themes):
            if existing_theme.name.lower() == name.lower() and existing_theme.company_id == company_id:
                # Remove theme from list
                themes.pop(i)
                
                # Save themes
                self._save_themes(themes, company_id)
                
                return True
        
        return False
    
    def _load_themes(self, company_id: str) -> List[Theme]:
        """Load themes from file for a specific company"""
        themes_file = self.get_themes_file(company_id)
        if os.path.exists(themes_file):
            try:
                with open(themes_file, 'r', encoding='utf-8') as file:
                    theme_data = json.load(file)
                    return [Theme.model_validate(theme) for theme in theme_data]
            except Exception as e:
                print(f"Error loading themes for company {company_id}: {str(e)}")
                return []
        return []
    
    def _save_themes(self, themes: List[Theme], company_id: str) -> None:
        """Save themes to file for a specific company"""
        themes_file = self.get_themes_file(company_id)
        try:
            with open(themes_file, 'w', encoding='utf-8') as file:
                theme_data = [theme.model_dump() for theme in themes]
                json.dump(theme_data, file, indent=2)
        except Exception as e:
            print(f"Error saving themes for company {company_id}: {str(e)}")
