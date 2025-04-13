"""
Script to run the FastAPI server.
"""
import os
import sys
import uvicorn

# Add the parent directory to the path so we can import the backend package
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Import settings after path is set up
from backend.config.settings import API_HOST, API_PORT, API_DEBUG

if __name__ == "__main__":
    uvicorn.run(
        "backend.app.main:app",
        host=API_HOST,
        port=API_PORT,
        reload=API_DEBUG
    )
