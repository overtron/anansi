#!/usr/bin/env python3
"""
Run the FastAPI backend for the Netflix Theme Extraction API
"""

import uvicorn
import os
import sys

if __name__ == "__main__":
    # Add the current directory to sys.path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    # Run the FastAPI application
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
