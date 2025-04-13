"""
Main FastAPI application.
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api import llm

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
