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
DEFAULT_THEMES_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "filingsdata", "output", "themes.json")

class ThemeService:
    """Service for managing themes"""
    
    def __init__(self, themes_file: str = DEFAULT_THEMES_FILE):
        self.themes_file = themes_file
        os.makedirs(os.path.dirname(self.themes_file), exist_ok=True)
    
    def get_all_themes(self) -> List[Theme]:
        """Get all themes"""
        themes = self._load_themes()
        return themes
    
    def get_theme_by_name(self, name: str) -> Optional[Theme]:
        """Get a theme by name"""
        themes = self._load_themes()
        for theme in themes:
            if theme.name.lower() == name.lower():
                return theme
        return None
    
    def create_theme(self, theme: ThemeCreate) -> Theme:
        """Create a new theme"""
        themes = self._load_themes()
        
        # Check if theme with same name already exists
        for existing_theme in themes:
            if existing_theme.name.lower() == theme.name.lower():
                raise ValueError(f"Theme with name '{theme.name}' already exists")
        
        # Create new theme
        new_theme = Theme(
            name=theme.name,
            description=theme.description,
            category=theme.category
        )
        
        # Add theme to list
        themes.append(new_theme)
        
        # Save themes
        self._save_themes(themes)
        
        return new_theme
    
    def update_theme(self, name: str, theme: ThemeCreate) -> Optional[Theme]:
        """Update an existing theme"""
        themes = self._load_themes()
        
        # Find theme with matching name
        for i, existing_theme in enumerate(themes):
            if existing_theme.name.lower() == name.lower():
                # Update theme
                updated_theme = Theme(
                    name=theme.name,
                    description=theme.description,
                    category=theme.category,
                    evidence=existing_theme.evidence,
                    source=existing_theme.source
                )
                
                # Replace theme in list
                themes[i] = updated_theme
                
                # Save themes
                self._save_themes(themes)
                
                return updated_theme
        
        return None
    
    def delete_theme(self, name: str) -> bool:
        """Delete a theme"""
        themes = self._load_themes()
        
        # Find theme with matching name
        for i, existing_theme in enumerate(themes):
            if existing_theme.name.lower() == name.lower():
                # Remove theme from list
                themes.pop(i)
                
                # Save themes
                self._save_themes(themes)
                
                return True
        
        return False
    
    def _load_themes(self) -> List[Theme]:
        """Load themes from file"""
        if os.path.exists(self.themes_file):
            try:
                with open(self.themes_file, 'r', encoding='utf-8') as file:
                    theme_data = json.load(file)
                    return [Theme.model_validate(theme) for theme in theme_data]
            except Exception as e:
                print(f"Error loading themes: {str(e)}")
                return []
        return []
    
    def _save_themes(self, themes: List[Theme]) -> None:
        """Save themes to file"""
        try:
            with open(self.themes_file, 'w', encoding='utf-8') as file:
                theme_data = [theme.model_dump() for theme in themes]
                json.dump(theme_data, file, indent=2)
        except Exception as e:
            print(f"Error saving themes: {str(e)}")
