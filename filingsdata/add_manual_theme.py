#!/usr/bin/env python3
"""
Add Manual Theme Script

This script adds a manual theme to the themes.json file.
Manual themes are preserved during updates by the theme_extractor.py script.
"""

import os
import json
import argparse
from datetime import datetime

# Constants
DEFAULT_THEMES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output", "themes.json")

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

def add_manual_theme(name, description, category, themes_file):
    """Add a manual theme to the themes.json file."""
    # Load existing themes
    themes = load_themes(themes_file)
    
    # Check if theme with same name already exists
    for theme in themes:
        if theme["name"].lower() == name.lower():
            print(f"Warning: A theme with the name '{name}' already exists.")
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
        "category": category
    }
    
    # Add theme
    themes.append(new_theme)
    
    # Save themes
    save_themes(themes, themes_file)
    print(f"Added manual theme: {name}")

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Add a manual theme to the themes.json file")
    parser.add_argument("--name", required=True, help="Theme name (1-5 words)")
    parser.add_argument("--description", required=True, help="Theme description")
    parser.add_argument("--category", default="General", help="Theme category (default: General)")
    parser.add_argument("--themes-file", default=DEFAULT_THEMES_FILE, help="Path to themes.json file")
    
    args = parser.parse_args()
    
    # Add manual theme
    add_manual_theme(args.name, args.description, args.category, args.themes_file)

if __name__ == "__main__":
    main()
