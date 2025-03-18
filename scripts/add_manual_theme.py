#!/usr/bin/env python3
"""
Add Manual Theme Script

This script adds a manual theme to the company-specific themes.json file.
Manual themes are preserved during updates by the theme_extractor.py script.
"""

import os
import json
import argparse
from datetime import datetime

# Constants
DEFAULT_OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "filingsdata", "output")

def get_themes_file(company_id, output_dir):
    """Get the path to the themes file for a specific company"""
    return os.path.join(output_dir, f"{company_id}_themes.json")

def load_themes(themes_file):
    """Load existing themes from JSON file."""
    if os.path.exists(themes_file):
        try:
            with open(themes_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading themes: {str(e)}")
            return []
    return []

def save_themes(themes, themes_file):
    """Save themes to JSON file."""
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(themes_file), exist_ok=True)
        
        with open(themes_file, 'w', encoding='utf-8') as file:
            json.dump(themes, file, indent=2)
        print(f"Saved {len(themes)} themes to {themes_file}")
    except Exception as e:
        print(f"Error saving themes: {str(e)}")

def add_manual_theme(name, description, category, company_id, themes_file):
    """Add a manual theme to the themes.json file."""
    # Load existing themes
    themes = load_themes(themes_file)
    
    # Check if theme with same name already exists
    for theme in themes:
        if theme["name"].lower() == name.lower():
            print(f"Warning: A theme with the name '{name}' already exists for company '{company_id}'.")
            replace = input("Do you want to replace it? (y/n): ").lower()
            if replace != 'y':
                print("Theme not added.")
                return
            # Remove existing theme
            themes = [t for t in themes if t["name"].lower() != name.lower()]
            break
    
    # Create new theme
    new_theme = {
        "name": name,
        "description": description,
        "category": category,
        "company_id": company_id
    }
    
    # Add theme
    themes.append(new_theme)
    
    # Save themes
    save_themes(themes, themes_file)
    print(f"Added manual theme '{name}' for company '{company_id}'")

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Add a manual theme to the company-specific themes.json file")
    parser.add_argument("--name", required=True, help="Theme name (1-5 words)")
    parser.add_argument("--description", required=True, help="Theme description")
    parser.add_argument("--category", default="General", help="Theme category (default: General)")
    parser.add_argument("--company-id", default="netflix", help="Company ID (e.g., 'netflix', 'roku')")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR, help="Output directory containing themes files")
    
    args = parser.parse_args()
    
    # Get themes file path
    themes_file = get_themes_file(args.company_id, args.output_dir)
    
    print(f"Adding theme for company: {args.company_id}")
    print(f"Themes file: {themes_file}")
    
    # Add manual theme
    add_manual_theme(args.name, args.description, args.category, args.company_id, themes_file)

if __name__ == "__main__":
    main()
