"""
Factory for creating image generation providers.
"""

import os
from typing import Optional
from dotenv import load_dotenv
from .image_generation import ImageGenerationProvider
from .google_image_provider import GoogleImageProvider
from backend.config.settings import Settings


def create_image_provider_from_env() -> ImageGenerationProvider:
    """
    Create an image generation provider based on environment variables.

    Returns:
        An instance of ImageGenerationProvider

    Raises:
        ValueError: If no valid provider configuration is found
    """
    env_loaded = load_dotenv()
    # Check for Image Generation API Provider
    provider = os.getenv("IMAGE_API_PROVIDER")
    model = os.getenv("IMAGE_API_MODEL")
    api_key = os.getenv("IMAGE_API_KEY")

    if provider == "google-genai":
        return GoogleImageProvider(api_key=api_key, default_model=model)

    # If no API keys are found, try to create a provider without explicit keys
    # This will rely on environment variables recognized by the provider's client
    try:
        return GoogleImageProvider()
    except Exception as e:
        raise ValueError(f"Failed to create image provider: {str(e)}")


def create_image_provider() -> ImageGenerationProvider:
    """
    Create an image generation provider of the specified type.

    Args:
        provider_type: Type of provider to create ("google", "openai", etc.)
        api_key: Optional API key for the provider

    Returns:
        An instance of ImageGenerationProvider

    Raises:
        ValueError: If the provider type is not supported
    """

    settings = Settings()
    print(f"Attempting to create image provider from settings: {settings}")
    image_provider = settings.image_api_provider
    print(f"Attempting to create image provider: {image_provider}")
    image_model = settings.image_api_model
    print(f"Attempting to create image model: {image_model}")
    image_api_key = settings.image_api_key
    print(f"Attempting to create image api key: {image_api_key}")

    if "google" in image_provider.lower():
        return GoogleImageProvider(api_key=image_api_key, default_model=image_model)

    else:
        raise ValueError(f"Unsupported image provider type: {image_provider}")
