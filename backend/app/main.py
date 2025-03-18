from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import sys

# Add the parent directory to sys.path to allow importing from sibling directories
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import API routers
from app.api.themes import router as themes_router
from app.api.questions import router as questions_router
from app.api.documents import router as documents_router

# Create FastAPI app
app = FastAPI(
    title="Netflix Theme Extraction API",
    description="API for extracting and querying themes from Netflix documents",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(themes_router, prefix="/api/themes", tags=["themes"])
app.include_router(questions_router, prefix="/api/questions", tags=["questions"])
app.include_router(documents_router, prefix="/api/documents", tags=["documents"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Netflix Theme Extraction API"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
