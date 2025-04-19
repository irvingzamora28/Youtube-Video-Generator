"""
Application settings using Pydantic BaseSettings.
Reads environment variables and provides typed settings.
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from typing import List, Optional

# Load environment variables from .env file relative to this file's location
env_path = Path(__file__).parent.parent.parent / '.env'
if env_path.is_file():
    print(f"Loading environment variables from: {env_path}")
    load_dotenv(dotenv_path=env_path, override=True)
else:
    print(f".env file not found at {env_path}, using system environment variables or defaults.")

class Settings(BaseSettings):
    """Application settings class."""

    # LLM settings
    llm_api_provider: str = "google" # Default to google now
    llm_api_key: Optional[str] = None
    llm_model: str = "gemini-1.5-flash" # Default model
    llm_api_url: Optional[str] = None

    # Image Generation settings (Optional, add if needed)
    default_image_provider: str = "google" # Assuming google for images too
    # Add image provider specific keys if necessary, e.g., GOOGLE_IMAGE_API_KEY
    image_api_provider: str
    image_api_key: str
    image_api_model: str

    # Audio Generation settings
    default_audio_provider: str = "google" # Default audio provider
    # Add audio provider specific keys if necessary, e.g., GOOGLE_AUDIO_API_KEY

    # API settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_debug: bool = False

    # CORS settings
    cors_origins: List[str] = ["*"] # Default to allow all for development

    # Media settings
    media_dir: str = "media"
    upload_dir: str = "uploads"
    static_dir: str = "static" # Added for consistency

    class Config:
        # Pydantic V2 uses model_config
        # For Pydantic V1 use: env_file = str(env_path), env_file_encoding = 'utf-8'
        # If using Pydantic V2 and want to load from .env automatically:
        env_file = str(env_path)
        env_file_encoding = 'utf-8'
        extra = 'ignore' # Ignore extra env vars not defined in the model

# Instantiate settings
settings = Settings()

# Ensure directories exist after settings are loaded
# Use absolute paths for clarity if needed, otherwise relative to project root assumed
base_dir = Path(__file__).parent.parent # backend directory
static_path = base_dir / settings.static_dir
media_path = base_dir / settings.media_dir
upload_path = base_dir / settings.upload_dir

print(f"Ensuring directory exists: {static_path}")
os.makedirs(static_path, exist_ok=True)
print(f"Ensuring directory exists: {media_path}")
os.makedirs(media_path, exist_ok=True)
print(f"Ensuring directory exists: {upload_path}")
os.makedirs(upload_path, exist_ok=True)

# You can optionally print loaded settings for verification (be careful with keys)
# print("Loaded Settings:")
# print(f"  LLM Provider: {settings.llm_api_provider}")
# print(f"  LLM Model: {settings.llm_model}")
# print(f"  Audio Provider: {settings.default_audio_provider}")
# print(f"  API Debug: {settings.api_debug}")
# print(f"  Static Dir: {settings.static_dir}")
