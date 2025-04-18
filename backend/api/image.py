"""
Image generation API endpoints.
"""
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from typing import Dict, Any, Optional, List
import base64
from pydantic import BaseModel

from backend.llm.image_generation import ImageGenerationProvider
from backend.llm.image_factory import create_image_provider_from_env

# Create router
router = APIRouter(prefix="/api/image", tags=["Image"])

# Dependencies
def get_image_provider() -> ImageGenerationProvider:
    """
    Get the image provider from environment variables.
    """
    try:
        print("DEBUG - Creating image provider from environment variables")
        return create_image_provider_from_env()
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Request models
class ImageGenerationRequest(BaseModel):
    prompt: str
    model: Optional[str] = None
    size: Optional[str] = None
    aspect_ratio: Optional[str] = None

class ImageEditRequest(BaseModel):
    prompt: str
    model: Optional[str] = None
    aspect_ratio: Optional[str] = None

class MultipleImagesRequest(BaseModel):
    prompt: str
    count: int = 1
    model: Optional[str] = None
    aspect_ratio: Optional[str] = None

# Routes
@router.post("/generate")
async def generate_image(
    request: ImageGenerationRequest,
    image_provider: ImageGenerationProvider = Depends(get_image_provider)
):
    """
    Generate an image based on a prompt.
    """
    try:
        print("DEBUG - Calling image_provider.generate_image")
        print(f"DEBUG - Request: prompt={request.prompt}, model={request.model}, aspect_ratio={request.aspect_ratio}")
        result = await image_provider.generate_image(request.prompt, request.model, request.aspect_ratio)
        print(f"DEBUG - Result: success={result.get('success', False)}")

        if not result.get('success', False):
            print(f"DEBUG - Error in result: {result.get('error', 'Unknown error')}")
            return result

        # Simplify the response to just include the necessary fields
        return {
            "success": True,
            "image_data": result.get('image_data'),
            "mime_type": result.get('mime_type', 'image/png')
        }
    except Exception as e:
        # Log the error for debugging
        import traceback
        error_details = {
            "error": str(e),
            "traceback": traceback.format_exc(),
            "request": {
                "prompt": request.prompt,
                "model": request.model,
                "aspect_ratio": request.aspect_ratio
            }
        }
        print("Error generating image:", error_details)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/edit")
async def edit_image(
    prompt: str = Form(...),
    image: UploadFile = File(...),
    model: Optional[str] = Form(None),
    image_provider: ImageGenerationProvider = Depends(get_image_provider)
):
    """
    Edit an image based on a prompt.
    """
    try:
        # Read the image data
        image_data = await image.read()

        # Edit the image
        result = await image_provider.edit_image(image_data, prompt, model)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-multiple")
async def generate_multiple_images(
    request: MultipleImagesRequest,
    image_provider: ImageGenerationProvider = Depends(get_image_provider)
):
    """
    Generate multiple images based on a prompt.
    """
    try:
        # Ensure count is within a reasonable range
        count = max(1, min(4, request.count))

        results = await image_provider.generate_multiple_images(request.prompt, count, request.model, request.aspect_ratio)
        return {"images": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
