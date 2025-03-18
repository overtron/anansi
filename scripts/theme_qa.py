#!/usr/bin/env python3
"""
Netflix Theme Question-Answering Script

This script allows users to ask questions about Netflix business themes using
the source documents as reference. It can explain why certain themes might be
missing, provide additional context for existing themes, or explore potential
new themes based on the source material.
"""

import os
import json
import argparse
import logging
from typing import List, Dict, Any, Tuple
import re
import numpy as np
from datetime import datetime
import pickle  # For serializing/deserializing the vector database
import hashlib  # For generating file hashes

# Third-party imports (will need to be installed)
import openai
import PyPDF2
import tiktoken
import faiss  # For vector search

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
DEFAULT_INPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "filingsdata", "trackedcompanies", "Netflix")
DEFAULT_OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "filingsdata", "output")
THEMES_JSON_FILE = "themes.json"
OPENAI_MODEL = "gpt-4o"
EMBEDDING_MODEL = "text-embedding-3-large"
MAX_TOKENS = 8192  # Maximum tokens for GPT-4o context
CHUNK_OVERLAP = 200  # Token overlap between chunks
TOP_K_RESULTS = 5  # Number of top document chunks to retrieve
MAX_PROMPT_TOKENS = 20000  # Limit total prompt tokens to stay under the 30k TPM limit

# Cache constants
CACHE_DIR = "cache"  # Directory to store cache files
TEXT_CACHE_FILE = "document_text_cache.json"  # Cache for extracted text
VECTOR_DB_CACHE_FILE = "vector_db_cache.pkl"  # Cache for vector database
FILE_HASH_CACHE_FILE = "file_hashes.json"  # Cache for file hashes

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

class VectorDatabase:
    """Manages the vector database for document chunks."""
    
    def __init__(self, dimension: int = 3072):  # text-embedding-3-large has 3072 dimensions
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)  # L2 distance (Euclidean)
        self.documents = []  # List to store document chunks and metadata
        self.last_updated = datetime.now().isoformat()  # Track when the database was last updated
    
    def add_document(self, document: Dict[str, Any], embedding: List[float]) -> None:
        """Add a document and its embedding to the database."""
        if not embedding:
            logger.warning("Attempted to add document with empty embedding")
            return
        
        # Convert embedding to numpy array
        embedding_np = np.array([embedding], dtype=np.float32)
        
        # Add to FAISS index
        self.index.add(embedding_np)
        
        # Store document with metadata
        self.documents.append(document)
        
        # Update last_updated timestamp
        self.last_updated = datetime.now().isoformat()
    
    def search(self, query_embedding: List[float], top_k: int = TOP_K_RESULTS) -> List[Dict[str, Any]]:
        """Search for the most similar documents to the query embedding."""
        if not query_embedding or self.index.ntotal == 0:
            return []
        
        # Convert query embedding to numpy array
        query_np = np.array([query_embedding], dtype=np.float32)
        
        # Search the index
        distances, indices = self.index.search(query_np, min(top_k, self.index.ntotal))
        
        # Return the top results
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1:  # FAISS returns -1 for not found
                doc = self.documents[idx].copy()
                doc["score"] = float(distances[0][i])
                results.append(doc)
        
        return results
    
    def __getstate__(self):
        """Custom state for pickling."""
        # Convert FAISS index to bytes for serialization
        index_bytes = faiss.serialize_index(self.index)
        
        # Return a state without the actual index object
        state = self.__dict__.copy()
        state['index'] = index_bytes
        return state
    
    def __setstate__(self, state):
        """Custom state loading for unpickling."""
        # Restore the index from bytes
        index_bytes = state.pop('index')
        self.__dict__.update(state)
        self.index = faiss.deserialize_index(index_bytes)

class ThemeQA:
    """Handles question answering about themes using source documents."""
    
    def __init__(self, api_key: str, input_dir: str, output_dir: str, cache_dir: str = None):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.themes_file = os.path.join(output_dir, THEMES_JSON_FILE)
        
        # Set up cache directory
        self.cache_dir = cache_dir or os.path.join(output_dir, CACHE_DIR)
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Cache file paths
        self.text_cache_file = os.path.join(self.cache_dir, TEXT_CACHE_FILE)
        self.vector_db_cache_file = os.path.join(self.cache_dir, VECTOR_DB_CACHE_FILE)
        self.file_hash_cache_file = os.path.join(self.cache_dir, FILE_HASH_CACHE_FILE)
        
        # Initialize OpenAI client
        self.openai_client = openai.OpenAI(api_key=api_key)
        
        # Initialize components
        self.doc_processor = DocumentProcessor()
        self.text_processor = TextProcessor(self.openai_client)
        self.vector_db = VectorDatabase()
        
        # Load themes
        self.themes = self._load_themes()
        
        # Load cached data
        self.text_cache = self._load_text_cache()
        self.file_hashes = self._load_file_hashes()
    
    def _load_themes(self) -> List[Dict]:
        """Load existing themes from JSON file."""
        if os.path.exists(self.themes_file):
            try:
                with open(self.themes_file, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except Exception as e:
                logger.error(f"Error loading themes: {str(e)}")
                return []
        return []
    
    def _load_text_cache(self) -> Dict[str, str]:
        """Load cached document text from file."""
        if os.path.exists(self.text_cache_file):
            try:
                with open(self.text_cache_file, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except Exception as e:
                logger.error(f"Error loading text cache: {str(e)}")
                return {}
        return {}

    def _save_text_cache(self) -> None:
        """Save document text cache to file."""
        try:
            with open(self.text_cache_file, 'w', encoding='utf-8') as file:
                json.dump(self.text_cache, file, indent=2)
        except Exception as e:
            logger.error(f"Error saving text cache: {str(e)}")

    def _load_file_hashes(self) -> Dict[str, str]:
        """Load cached file hashes from file."""
        if os.path.exists(self.file_hash_cache_file):
            try:
                with open(self.file_hash_cache_file, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except Exception as e:
                logger.error(f"Error loading file hashes: {str(e)}")
                return {}
        return {}

    def _save_file_hashes(self) -> None:
        """Save file hashes to cache file."""
        try:
            with open(self.file_hash_cache_file, 'w', encoding='utf-8') as file:
                json.dump(self.file_hashes, file, indent=2)
        except Exception as e:
            logger.error(f"Error saving file hashes: {str(e)}")

    def _calculate_file_hash(self, file_path: str) -> str:
        """Calculate MD5 hash of a file to detect changes."""
        try:
            with open(file_path, 'rb') as file:
                return hashlib.md5(file.read()).hexdigest()
        except Exception as e:
            logger.error(f"Error calculating file hash: {str(e)}")
            return ""

    def _load_vector_db(self) -> bool:
        """Load vector database from cache file."""
        if os.path.exists(self.vector_db_cache_file):
            try:
                with open(self.vector_db_cache_file, 'rb') as file:
                    self.vector_db = pickle.load(file)
                logger.info(f"Loaded vector database from cache with {self.vector_db.index.ntotal} chunks")
                return True
            except Exception as e:
                logger.error(f"Error loading vector database: {str(e)}")
                return False
        return False

    def _save_vector_db(self) -> None:
        """Save vector database to cache file."""
        try:
            with open(self.vector_db_cache_file, 'wb') as file:
                pickle.dump(self.vector_db, file)
            logger.info(f"Saved vector database to cache with {self.vector_db.index.ntotal} chunks")
        except Exception as e:
            logger.error(f"Error saving vector database: {str(e)}")
    
    def invalidate_cache(self) -> None:
        """Invalidate all caches to force reprocessing of documents."""
        logger.info("Invalidating all caches")
        
        # Remove cache files
        if os.path.exists(self.text_cache_file):
            os.remove(self.text_cache_file)
        
        if os.path.exists(self.vector_db_cache_file):
            os.remove(self.vector_db_cache_file)
        
        if os.path.exists(self.file_hash_cache_file):
            os.remove(self.file_hash_cache_file)
        
        # Reset in-memory caches
        self.text_cache = {}
        self.file_hashes = {}
        self.vector_db = VectorDatabase()
        
        logger.info("All caches invalidated")
    
    def load_documents(self) -> None:
        """Load and process documents, adding them to the vector database."""
        logger.info("Loading and processing documents...")
        
        # Try to load vector database from cache first
        if self._load_vector_db():
            logger.info("Using cached vector database")
            return
        
        logger.info(f"Input directory: {self.input_dir}")
        
        # Check if input directory exists
        if not os.path.exists(self.input_dir):
            logger.error(f"Input directory does not exist: {self.input_dir}")
            logger.info(f"Current working directory: {os.getcwd()}")
            logger.info(f"Directory contents: {os.listdir('.')}")
            return
        
        # Find all PDF and JSON files
        pdf_files = []
        json_files = []
        
        for root, dirs, files in os.walk(self.input_dir):
            logger.info(f"Scanning directory: {root}")
            
            for file in files:
                file_path = os.path.join(root, file)
                
                if file.lower().endswith('.pdf'):
                    pdf_files.append(file_path)
                    logger.info(f"Found PDF: {file_path}")
                elif file.lower().endswith('.json'):
                    json_files.append(file_path)
                    logger.info(f"Found JSON: {file_path}")
        
        # Process PDF files
        for pdf_file in pdf_files:
            # Check if file has changed since last processing
            current_hash = self._calculate_file_hash(pdf_file)
            cached_hash = self.file_hashes.get(pdf_file)
            
            if pdf_file in self.text_cache and cached_hash == current_hash:
                logger.info(f"Using cached text for PDF: {pdf_file}")
                text = self.text_cache[pdf_file]
            else:
                # Extract text from PDF
                logger.info(f"Extracting text from PDF: {pdf_file}")
                text = self.doc_processor.extract_text_from_pdf(pdf_file)
                if not text:
                    logger.warning(f"No text extracted from PDF: {pdf_file}")
                    continue
                
                # Update cache
                self.text_cache[pdf_file] = text
                self.file_hashes[pdf_file] = current_hash
            
            # Split text into chunks
            chunks = self.text_processor.chunk_text(text)
            
            # Add chunks to vector database
            for i, chunk in enumerate(chunks):
                # Generate embedding
                embedding = self.text_processor.generate_embedding(chunk)
                
                # Add to vector database
                self.vector_db.add_document({
                    "content": chunk,
                    "source": os.path.basename(pdf_file),
                    "chunk_id": i,
                    "total_chunks": len(chunks),
                    "type": "pdf"
                }, embedding)
        
        # Process JSON files
        for json_file in json_files:
            # Check if file has changed since last processing
            current_hash = self._calculate_file_hash(json_file)
            cached_hash = self.file_hashes.get(json_file)
            
            if json_file in self.text_cache and cached_hash == current_hash:
                logger.info(f"Using cached text for JSON: {json_file}")
                text = self.text_cache[json_file]
            else:
                # Parse JSON file
                logger.info(f"Parsing JSON file: {json_file}")
                json_data = self.doc_processor.parse_json_file(json_file)
                if not json_data:
                    logger.warning(f"No data parsed from JSON: {json_file}")
                    continue
                
                # Extract text from JSON
                text = self.doc_processor.extract_text_from_sec_json(json_data)
                if not text:
                    logger.warning(f"No text extracted from JSON: {json_file}")
                    continue
                
                # Update cache
                self.text_cache[json_file] = text
                self.file_hashes[json_file] = current_hash
            
            # Split text into chunks
            chunks = self.text_processor.chunk_text(text)
            
            # Add chunks to vector database
            for i, chunk in enumerate(chunks):
                # Generate embedding
                embedding = self.text_processor.generate_embedding(chunk)
                
                # Add to vector database
                self.vector_db.add_document({
                    "content": chunk,
                    "source": os.path.basename(json_file),
                    "chunk_id": i,
                    "total_chunks": len(chunks),
                    "type": "json"
                }, embedding)
        
        # Save caches
        self._save_text_cache()
        self._save_file_hashes()
        self._save_vector_db()
        
        logger.info(f"Loaded {self.vector_db.index.ntotal} document chunks into vector database")
    
    def answer_question(self, question: str) -> str:
        """Answer a question about themes using the source documents."""
        logger.info(f"Answering question: {question}")
        
        # Generate embedding for the question
        question_embedding = self.text_processor.generate_embedding(question)
        
        # Search for relevant document chunks
        relevant_chunks = self.vector_db.search(question_embedding)
        
        if not relevant_chunks:
            return "I couldn't find any relevant information in the source documents to answer your question."
        
        # Prepare context for the LLM
        context = ""
        total_context_tokens = 0
        
        # Sort chunks by relevance score (lower is better for L2 distance)
        relevant_chunks.sort(key=lambda x: x["score"])
        
        # Add chunks to context until we reach the token limit
        for i, chunk in enumerate(relevant_chunks):
            chunk_text = f"\n--- Document {i+1}: {chunk['source']} (part {chunk['chunk_id']+1}/{chunk['total_chunks']}) ---\n"
            chunk_text += chunk["content"] + "\n"
            
            # Count tokens in this chunk
            chunk_tokens = self.text_processor.count_tokens(chunk_text)
            
            # Check if adding this chunk would exceed our token limit
            if total_context_tokens + chunk_tokens > MAX_PROMPT_TOKENS - 2000:  # Leave 2000 tokens for the rest of the prompt
                logger.info(f"Stopping at {i} chunks to stay under token limit")
                break
            
            context += chunk_text
            total_context_tokens += chunk_tokens
        
        # Prepare theme information (limit to 10 themes to save tokens)
        theme_info = ""
        for i, theme in enumerate(self.themes[:10]):
            theme_name = theme.get("name", "")
            theme_desc = theme.get("description", "")
            theme_source = theme.get("source", "Manually added")
            theme_info += f"- {theme_name}: {theme_desc} (Source: {theme_source})\n"
            
            # If we have more than 10 themes, add a note
            if i == 9 and len(self.themes) > 10:
                theme_info += f"- ... and {len(self.themes) - 10} more themes\n"
        
        # Determine if this is a "missing theme" question
        is_missing_theme_question = any(phrase in question.lower() for phrase in [
            "missing", "not included", "isn't listed", "not listed", "absent", "omitted", "excluded"
        ])
        
        # Create prompt based on question type
        if is_missing_theme_question:
            # Extract the potential theme name from the question
            potential_theme = re.search(r"(?:why isn't|why is not|why isn't the theme|why is the theme) ['\"](.*?)['\"]", question.lower())
            if potential_theme:
                potential_theme = potential_theme.group(1)
            else:
                potential_theme = "the mentioned theme"
            
            prompt = f"""
            You are analyzing Netflix's investor relations and SEC filings to determine why a specific theme might not be included in the extracted themes.
            
            Question: {question}
            
            Current extracted themes:
            {theme_info}
            
            Based on the following relevant document excerpts, explain why "{potential_theme}" might not be included as a theme. Consider:
            1. Is there sufficient evidence in the documents to support this as a significant business growth/contraction theme?
            2. Is it possibly included under a different theme name or category?
            3. Is it mentioned but not emphasized enough to be considered a key theme?
            
            Provide specific evidence from the documents to support your explanation.
            
            Relevant document excerpts:
            {context}
            """
        else:
            prompt = f"""
            You are analyzing Netflix's investor relations and SEC filings to answer questions about business themes.
            
            Question: {question}
            
            Current extracted themes:
            {theme_info}
            
            Based on the following relevant document excerpts, provide a comprehensive answer to the question.
            Include specific evidence and citations from the documents to support your answer.
            
            Relevant document excerpts:
            {context}
            """
        
        # Check total prompt tokens
        prompt_tokens = self.text_processor.count_tokens(prompt)
        logger.info(f"Total prompt tokens: {prompt_tokens}")
        
        if prompt_tokens > MAX_PROMPT_TOKENS:
            logger.warning(f"Prompt exceeds token limit ({prompt_tokens} > {MAX_PROMPT_TOKENS})")
            # Truncate context to fit within token limit
            context_tokens = self.text_processor.count_tokens(context)
            excess_tokens = prompt_tokens - MAX_PROMPT_TOKENS + 500  # Add 500 token buffer
            
            if excess_tokens >= context_tokens:
                # If we need to remove more tokens than we have in context, use a simplified prompt
                prompt = f"""
                You are analyzing Netflix's investor relations and SEC filings to answer questions about business themes.
                
                Question: {question}
                
                Current extracted themes:
                {theme_info}
                
                I don't have enough context from the documents to provide a detailed answer.
                Please provide the best answer you can based on the themes listed above.
                """
            else:
                # Otherwise, truncate the context
                context_tokens_to_keep = context_tokens - excess_tokens
                context_parts = context.split("--- Document ")
                
                new_context = ""
                current_tokens = 0
                
                for i, part in enumerate(context_parts):
                    if i == 0:  # First part doesn't have the "--- Document" prefix
                        new_context = part
                        current_tokens = self.text_processor.count_tokens(part)
                    else:
                        part_with_prefix = "--- Document " + part
                        part_tokens = self.text_processor.count_tokens(part_with_prefix)
                        
                        if current_tokens + part_tokens <= context_tokens_to_keep:
                            new_context += part_with_prefix
                            current_tokens += part_tokens
                        else:
                            break
                
                # Recreate the prompt with truncated context
                if is_missing_theme_question:
                    prompt = f"""
                    You are analyzing Netflix's investor relations and SEC filings to determine why a specific theme might not be included in the extracted themes.
                    
                    Question: {question}
                    
                    Current extracted themes:
                    {theme_info}
                    
                    Based on the following relevant document excerpts, explain why "{potential_theme}" might not be included as a theme. Consider:
                    1. Is there sufficient evidence in the documents to support this as a significant business growth/contraction theme?
                    2. Is it possibly included under a different theme name or category?
                    3. Is it mentioned but not emphasized enough to be considered a key theme?
                    
                    Provide specific evidence from the documents to support your explanation.
                    
                    Relevant document excerpts (truncated due to length):
                    {new_context}
                    """
                else:
                    prompt = f"""
                    You are analyzing Netflix's investor relations and SEC filings to answer questions about business themes.
                    
                    Question: {question}
                    
                    Current extracted themes:
                    {theme_info}
                    
                    Based on the following relevant document excerpts, provide a comprehensive answer to the question.
                    Include specific evidence and citations from the documents to support your answer.
                    
                    Relevant document excerpts (truncated due to length):
                    {new_context}
                    """
        
        # Generate answer using OpenAI
        try:
            response = self.openai_client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a financial analyst specializing in identifying business growth and contraction themes from corporate documents."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            logger.error(f"Error generating answer: {str(e)}")
            return f"An error occurred while generating the answer: {str(e)}"

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Answer questions about company business themes")
    parser.add_argument("--api-key", required=True, help="OpenAI API key")
    parser.add_argument("--question", required=True, help="Question to answer")
    parser.add_argument("--company-id", default="netflix", help="Company ID (e.g., 'netflix', 'roku')")
    parser.add_argument("--input-dir", help="Input directory containing documents (defaults to trackedcompanies/{Company})")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR, help="Output directory containing themes.json")
    parser.add_argument("--cache-dir", help="Directory to store cache files")
    parser.add_argument("--invalidate-cache", action="store_true", help="Invalidate all caches")
    
    args = parser.parse_args()
    
    # Set default input directory based on company_id if not provided
    if not args.input_dir:
        args.input_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                     "filingsdata", "trackedcompanies", args.company_id.capitalize())
    
    # Set themes file name based on company_id
    global THEMES_JSON_FILE
    THEMES_JSON_FILE = f"{args.company_id}_themes.json"
    
    print(f"Answering question for company: {args.company_id}")
    print(f"Input directory: {args.input_dir}")
    print(f"Output directory: {args.output_dir}")
    print(f"Themes file: {THEMES_JSON_FILE}")
    
    # Initialize ThemeQA
    theme_qa = ThemeQA(
        api_key=args.api_key,
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        cache_dir=args.cache_dir
    )
    
    # Invalidate cache if requested
    if args.invalidate_cache:
        theme_qa.invalidate_cache()
    
    # Load documents
    theme_qa.load_documents()
    
    # Get company name for context
    company_name = args.company_id.capitalize()
    
    # Add company context to the question
    contextualized_question = f"Question about {company_name}: {args.question}"
    
    # Answer question
    answer = theme_qa.answer_question(contextualized_question)
    
    # Print answer
    print("\n" + "="*80)
    print(f"Question about {company_name}: {args.question}")
    print("="*80)
    print(answer)
    print("="*80)

if __name__ == "__main__":
    main()
