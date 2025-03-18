#!/usr/bin/env python3
"""
Netflix Theme Extraction Script

This script extracts business growth/contraction themes from Netflix's investor relations
PDFs and SEC filings using OpenAI's API. It outputs themes to a markdown file and
supports updates as new documents become available.
"""

import os
import sys
import json
import argparse
import logging
from datetime import datetime
import hashlib
from typing import List, Dict, Any, Set, Optional
import re

# Third-party imports (will need to be installed)
import openai
import PyPDF2
import tiktoken

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
DEFAULT_OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "filingsdata", "output")
THEMES_JSON_FILE = "themes.json"
THEMES_MD_FILE = "netflix_themes.md"
PROCESSED_FILES_JSON = "processed_files.json"
OPENAI_MODEL = "gpt-4o"
EMBEDDING_MODEL = "text-embedding-3-large"
MAX_TOKENS = 8192  # Maximum tokens for GPT-4o context
CHUNK_OVERLAP = 200  # Token overlap between chunks

class DocumentProcessor:
    """Handles the processing of different document types."""
    
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        """Extract text from a PDF file."""
        logger.info(f"Extracting text from PDF: {file_path}")
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            logger.error(f"Error extracting text from PDF {file_path}: {str(e)}")
            return ""
    
    @staticmethod
    def parse_json_file(file_path: str) -> Dict:
        """Parse a JSON file."""
        logger.info(f"Parsing JSON file: {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            logger.error(f"Error parsing JSON file {file_path}: {str(e)}")
            return {}
    
    @staticmethod
    def extract_text_from_sec_json(json_data: Dict) -> str:
        """Extract relevant text from SEC JSON data."""
        # This is a placeholder. The actual implementation would depend on the
        # structure of the SEC JSON files, which we couldn't examine directly.
        text = ""
        try:
            # Example extraction logic - adjust based on actual JSON structure
            if "filings" in json_data:
                for filing in json_data.get("filings", {}).get("recent", []):
                    text += f"Filing Type: {filing.get('form', '')}\n"
                    text += f"Filing Date: {filing.get('filingDate', '')}\n"
                    text += f"Description: {filing.get('description', '')}\n\n"
            
            # Add more extraction logic based on the actual structure
            return text
        except Exception as e:
            logger.error(f"Error extracting text from SEC JSON: {str(e)}")
            return ""

class TextProcessor:
    """Handles text processing, chunking, and embedding generation."""
    
    def __init__(self, openai_client):
        self.openai_client = openai_client
        self.tokenizer = tiktoken.get_encoding("cl100k_base")  # For token counting
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters that don't add meaning
        text = re.sub(r'[^\w\s.,;:!?()[\]{}"\'-]', '', text)
        return text.strip()
    
    def count_tokens(self, text: str) -> int:
        """Count the number of tokens in a text."""
        return len(self.tokenizer.encode(text))
    
    def chunk_text(self, text: str, max_tokens: int = MAX_TOKENS, overlap: int = CHUNK_OVERLAP) -> List[str]:
        """Split text into chunks of specified token size with overlap."""
        chunks = []
        
        # Clean the text first
        text = self.clean_text(text)
        
        # If text is short enough, return it as a single chunk
        if self.count_tokens(text) <= max_tokens:
            return [text]
        
        # Split text into sentences to avoid breaking in the middle of a sentence
        sentences = re.split(r'(?<=[.!?])\s+', text)
        current_chunk = ""
        
        for sentence in sentences:
            # Check if adding this sentence would exceed the max tokens
            potential_chunk = current_chunk + " " + sentence if current_chunk else sentence
            if self.count_tokens(potential_chunk) <= max_tokens:
                current_chunk = potential_chunk
            else:
                # Save the current chunk and start a new one
                if current_chunk:
                    chunks.append(current_chunk)
                
                # If the sentence itself is too long, we need to split it
                if self.count_tokens(sentence) > max_tokens:
                    # Split by words
                    words = sentence.split()
                    current_chunk = ""
                    for word in words:
                        potential_chunk = current_chunk + " " + word if current_chunk else word
                        if self.count_tokens(potential_chunk) <= max_tokens:
                            current_chunk = potential_chunk
                        else:
                            chunks.append(current_chunk)
                            current_chunk = word
                else:
                    current_chunk = sentence
        
        # Add the last chunk if it's not empty
        if current_chunk:
            chunks.append(current_chunk)
        
        # Create overlapping chunks
        overlapping_chunks = []
        for i in range(len(chunks)):
            if i > 0:
                # Get the end of the previous chunk for overlap
                prev_chunk = chunks[i-1]
                prev_tokens = self.tokenizer.encode(prev_chunk)
                overlap_tokens = prev_tokens[-overlap:] if len(prev_tokens) > overlap else prev_tokens
                overlap_text = self.tokenizer.decode(overlap_tokens)
                
                # Add the overlap to the beginning of the current chunk
                current_chunk = chunks[i]
                overlapping_chunks.append(overlap_text + " " + current_chunk)
            else:
                overlapping_chunks.append(chunks[i])
        
        return overlapping_chunks
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate an embedding for the given text using OpenAI's API."""
        try:
            response = self.openai_client.embeddings.create(
                model=EMBEDDING_MODEL,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            return []

class ThemeExtractor:
    """Extracts themes from document text using OpenAI's API."""
    
    def __init__(self, openai_client):
        self.openai_client = openai_client
    
    def extract_themes(self, text: str, document_source: str) -> List[Dict]:
        """
        Extract business growth/contraction themes from text using OpenAI's API.
        
        Args:
            text: The document text to analyze
            document_source: Source information for the document
            
        Returns:
            List of theme dictionaries with name, description, and source
        """
        logger.info(f"Extracting themes from document: {document_source}")
        
        # Get company name from THEMES_MD_FILE (e.g., "netflix_themes.md" -> "Netflix")
        company_name = THEMES_MD_FILE.split('_')[0].capitalize()
        
        prompt = f"""
        You are analyzing a document from {company_name}'s investor relations or SEC filings.
        
        Document source: {document_source}
        
        Please identify key themes related to {company_name}'s business growth or contraction factors.
        Focus on strategic initiatives, market trends, competitive factors, financial indicators,
        content strategy, technology developments, and regulatory impacts.
        
        For each theme:
        1. Provide a concise name (1-5 words)
        2. Write a brief description explaining how this theme relates to {company_name}'s business growth or contraction
        3. Include specific evidence from the document that supports this theme
        
        Format your response as a JSON array of theme objects with the following structure:
        [
            {{
                "name": "Theme Name",
                "description": "Description of how this theme impacts {company_name}'s business",
                "evidence": "Specific evidence from the document"
            }}
        ]
        
        Only include themes that are clearly supported by evidence in the document.
        
        Document text:
        {text}
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a financial analyst specializing in identifying business growth and contraction themes from corporate documents."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            # Extract the JSON response
            content = response.choices[0].message.content
            themes_data = json.loads(content)
            
            # Add source information to each theme
            themes = []
            for theme in themes_data.get("themes", []):
                theme["source"] = document_source
                themes.append(theme)
            
            return themes
        
        except Exception as e:
            logger.error(f"Error extracting themes: {str(e)}")
            return []

class ThemeManager:
    """Manages theme storage, deduplication, and updates."""
    
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.themes_file = os.path.join(output_dir, THEMES_JSON_FILE)
        self.processed_files_json = os.path.join(output_dir, PROCESSED_FILES_JSON)
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
    
    def load_themes(self) -> List[Dict]:
        """Load existing themes from JSON file."""
        if os.path.exists(self.themes_file):
            try:
                with open(self.themes_file, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except Exception as e:
                logger.error(f"Error loading themes: {str(e)}")
                return []
        return []
    
    def save_themes(self, themes: List[Dict]) -> None:
        """Save themes to JSON file."""
        try:
            with open(self.themes_file, 'w', encoding='utf-8') as file:
                json.dump(themes, file, indent=2)
            logger.info(f"Saved {len(themes)} themes to {self.themes_file}")
        except Exception as e:
            logger.error(f"Error saving themes: {str(e)}")
    
    def load_processed_files(self) -> Dict[str, str]:
        """Load information about processed files."""
        if os.path.exists(self.processed_files_json):
            try:
                with open(self.processed_files_json, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except Exception as e:
                logger.error(f"Error loading processed files info: {str(e)}")
                return {}
        return {}
    
    def save_processed_files(self, processed_files: Dict[str, str]) -> None:
        """Save information about processed files."""
        try:
            with open(self.processed_files_json, 'w', encoding='utf-8') as file:
                json.dump(processed_files, file, indent=2)
        except Exception as e:
            logger.error(f"Error saving processed files info: {str(e)}")
    
    def get_file_hash(self, file_path: str) -> str:
        """Calculate MD5 hash of a file to detect changes."""
        try:
            with open(file_path, 'rb') as file:
                return hashlib.md5(file.read()).hexdigest()
        except Exception as e:
            logger.error(f"Error calculating file hash: {str(e)}")
            return ""
    
    def merge_themes(self, existing_themes: List[Dict], new_themes: List[Dict]) -> List[Dict]:
        """
        Merge new themes with existing themes, avoiding duplicates.
        Preserves manually added themes (those without a source).
        """
        # Create a set of existing theme names for quick lookup
        existing_theme_names = {theme["name"].lower() for theme in existing_themes}
        
        # Identify manually added themes (those without a source)
        manual_themes = [theme for theme in existing_themes if "source" not in theme]
        
        # Start with all manually added themes
        merged_themes = manual_themes.copy()
        
        # Add non-manual existing themes that aren't duplicated in new themes
        for theme in existing_themes:
            if "source" in theme:  # Not a manual theme
                # Check if this theme is duplicated in new themes
                is_duplicate = False
                for new_theme in new_themes:
                    if self._are_themes_similar(theme, new_theme):
                        is_duplicate = True
                        break
                
                if not is_duplicate:
                    merged_themes.append(theme)
        
        # Add new themes that aren't too similar to existing ones
        for new_theme in new_themes:
            is_duplicate = False
            for theme in merged_themes:
                if self._are_themes_similar(theme, new_theme):
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                merged_themes.append(new_theme)
        
        return merged_themes
    
    def _are_themes_similar(self, theme1: Dict, theme2: Dict) -> bool:
        """
        Check if two themes are similar enough to be considered duplicates.
        Currently using a simple name comparison, but could be enhanced with embeddings.
        """
        # Simple comparison based on theme name
        return theme1["name"].lower() == theme2["name"].lower()
    
    def generate_markdown(self, themes: List[Dict]) -> None:
        """Generate a markdown file from the themes."""
        md_file_path = os.path.join(self.output_dir, THEMES_MD_FILE)
        
        try:
            with open(md_file_path, 'w', encoding='utf-8') as file:
                file.write(f"# {THEMES_MD_FILE.split('_')[0].capitalize()} Business Themes\n\n")
                file.write(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
                
                # Group themes by category if they have one, otherwise use "General"
                categorized_themes = {}
                for theme in themes:
                    category = theme.get("category", "General")
                    if category not in categorized_themes:
                        categorized_themes[category] = []
                    categorized_themes[category].append(theme)
                
                # Write themes by category
                for category, category_themes in categorized_themes.items():
                    file.write(f"## {category}\n\n")
                    
                    for theme in category_themes:
                        file.write(f"### {theme['name']}\n\n")
                        file.write(f"{theme['description']}\n\n")
                        
                        if "evidence" in theme:
                            file.write("**Evidence:**\n\n")
                            file.write(f"{theme['evidence']}\n\n")
                        
                        if "source" in theme:
                            file.write(f"*Source: {theme['source']}*\n\n")
                        else:
                            file.write("*Manually added theme*\n\n")
                
                file.write("---\n")
                file.write(f"This document was generated automatically by the {THEMES_MD_FILE.split('_')[0].capitalize()} Theme Extraction Script.\n")
            
            logger.info(f"Generated markdown file: {md_file_path}")
        
        except Exception as e:
            logger.error(f"Error generating markdown: {str(e)}")

class ThemeExtractionPipeline:
    """Main pipeline for extracting themes from documents."""
    
    def __init__(self, api_key: str, input_dir: str, output_dir: str):
        self.input_dir = input_dir
        self.output_dir = output_dir
        
        # Initialize OpenAI client
        self.openai_client = openai.OpenAI(api_key=api_key)
        
        # Initialize components
        self.doc_processor = DocumentProcessor()
        self.text_processor = TextProcessor(self.openai_client)
        self.theme_extractor = ThemeExtractor(self.openai_client)
        self.theme_manager = ThemeManager(output_dir)
    
    def run(self) -> None:
        """Run the theme extraction pipeline."""
        logger.info("Starting theme extraction pipeline")
        
        # Load existing themes and processed files info
        existing_themes = self.theme_manager.load_themes()
        processed_files = self.theme_manager.load_processed_files()
        
        # Find all PDF and JSON files
        pdf_files = []
        json_files = []
        
        for root, _, files in os.walk(self.input_dir):
            for file in files:
                file_path = os.path.join(root, file)
                
                if file.lower().endswith('.pdf'):
                    pdf_files.append(file_path)
                elif file.lower().endswith('.json'):
                    json_files.append(file_path)
        
        # Process files and extract themes
        all_new_themes = []
        updated_processed_files = processed_files.copy()
        
        # Process PDF files
        for pdf_file in pdf_files:
            file_hash = self.theme_manager.get_file_hash(pdf_file)
            
            # Skip if file hasn't changed
            if pdf_file in processed_files and processed_files[pdf_file] == file_hash:
                logger.info(f"Skipping unchanged PDF: {pdf_file}")
                continue
            
            # Extract text from PDF
            text = self.doc_processor.extract_text_from_pdf(pdf_file)
            if not text:
                logger.warning(f"No text extracted from PDF: {pdf_file}")
                continue
            
            # Split text into chunks
            chunks = self.text_processor.chunk_text(text)
            
            # Extract themes from each chunk
            file_themes = []
            for i, chunk in enumerate(chunks):
                chunk_source = f"{os.path.basename(pdf_file)} (part {i+1}/{len(chunks)})"
                themes = self.theme_extractor.extract_themes(chunk, chunk_source)
                file_themes.extend(themes)
            
            all_new_themes.extend(file_themes)
            updated_processed_files[pdf_file] = file_hash
        
        # Process JSON files
        for json_file in json_files:
            file_hash = self.theme_manager.get_file_hash(json_file)
            
            # Skip if file hasn't changed
            if json_file in processed_files and processed_files[json_file] == file_hash:
                logger.info(f"Skipping unchanged JSON: {json_file}")
                continue
            
            # Parse JSON file
            json_data = self.doc_processor.parse_json_file(json_file)
            if not json_data:
                logger.warning(f"No data parsed from JSON: {json_file}")
                continue
            
            # Extract text from JSON
            text = self.doc_processor.extract_text_from_sec_json(json_data)
            if not text:
                logger.warning(f"No text extracted from JSON: {json_file}")
                continue
            
            # Split text into chunks
            chunks = self.text_processor.chunk_text(text)
            
            # Extract themes from each chunk
            file_themes = []
            for i, chunk in enumerate(chunks):
                chunk_source = f"{os.path.basename(json_file)} (part {i+1}/{len(chunks)})"
                themes = self.theme_extractor.extract_themes(chunk, chunk_source)
                file_themes.extend(themes)
            
            all_new_themes.extend(file_themes)
            updated_processed_files[json_file] = file_hash
        
        # Merge new themes with existing themes
        merged_themes = self.theme_manager.merge_themes(existing_themes, all_new_themes)
        
        # Save updated themes and processed files info
        self.theme_manager.save_themes(merged_themes)
        self.theme_manager.save_processed_files(updated_processed_files)
        
        # Generate markdown file
        self.theme_manager.generate_markdown(merged_themes)
        
        logger.info("Theme extraction pipeline completed")

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Extract business themes from company documents")
    parser.add_argument("--api-key", help="OpenAI API key (can also use OPENAI_API_KEY environment variable)")
    parser.add_argument("--company-id", default="netflix", help="Company ID (e.g., 'netflix', 'roku')")
    parser.add_argument("--input-dir", help="Input directory containing documents (defaults to trackedcompanies/{Company})")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR, help="Output directory for results")
    
    args = parser.parse_args()
    
    # Get API key from command line or environment variable
    api_key = args.api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OpenAI API key is required. Provide it with --api-key or set OPENAI_API_KEY environment variable.")
        sys.exit(1)
    
    # Set default input directory based on company_id if not provided
    if not args.input_dir:
        args.input_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                     "filingsdata", "trackedcompanies", args.company_id.capitalize())
    
    # Set output file name based on company_id
    global THEMES_JSON_FILE, THEMES_MD_FILE
    THEMES_JSON_FILE = f"{args.company_id}_themes.json"
    THEMES_MD_FILE = f"{args.company_id}_themes.md"
    
    print(f"Extracting themes for company: {args.company_id}")
    print(f"Input directory: {args.input_dir}")
    print(f"Output directory: {args.output_dir}")
    print(f"Output files: {THEMES_JSON_FILE}, {THEMES_MD_FILE}")
    
    # Run the pipeline
    pipeline = ThemeExtractionPipeline(
        api_key=api_key,
        input_dir=args.input_dir,
        output_dir=args.output_dir
    )
    pipeline.run()

if __name__ == "__main__":
    main()
