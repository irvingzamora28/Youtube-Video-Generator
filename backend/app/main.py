"""
Main FastAPI application.
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Import API routers
from backend.api import llm, script, image, project_api, audio # Add audio router import
from backend.api.image_save import router as image_save_router

# Create FastAPI app
app = FastAPI(
    title="AI Video Content Generator API",
    description="API for generating video content using AI",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(llm.router)
app.include_router(script.router)
app.include_router(image.router)
app.include_router(project_api.router)
app.include_router(image_save_router)
app.include_router(audio.router) # Include the audio router

# Serve static files (images, audio etc.)
# Use settings for consistency
from backend.config.settings import settings
static_dir_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), settings.static_dir)
app.mount(f"/{settings.static_dir}", StaticFiles(directory=static_dir_path), name=settings.static_dir)

# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint.
    """
    return {"message": "Welcome to the AI Video Content Generator API"}

# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy"}
