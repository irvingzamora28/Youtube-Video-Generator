"""
Script to run the FastAPI server.
"""
import os
import sys
import uvicorn
from config.settings import Settings


# Add the parent directory to the path so we can import the backend package
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Import settings after path is set up
settings = Settings()


if __name__ == "__main__":
    uvicorn.run(
        "backend.app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_debug,
    )
