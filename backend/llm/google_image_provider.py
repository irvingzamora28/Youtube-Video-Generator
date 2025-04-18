"""
Google Gemini image generation provider.
"""
import base64
from io import BytesIO
from typing import Dict, Any, Optional, List

from google import genai
from google.genai import types
from PIL import Image

from .image_generation import ImageGenerationProvider


class GoogleImageProvider(ImageGenerationProvider):
    """Provider for Google Gemini image generation API."""

    def __init__(self, api_key: str = None, default_model: str = "gemini-1.5-flash", client=None):
        """
        Initialize the Google Gemini image provider.

        Args:
            api_key: API key for authentication
            default_model: Default model to use
            client: Optional pre-configured client (for testing)
        """
        self.default_model = default_model

        # Use provided client or create a new one
        if client:
            self.client = client
        else:
            # Use API key from parameters or environment variable
            print("DEBUG - Using API key from parameters or environment variable")
            self.client = genai.Client(api_key=api_key)

    async def generate_image(self,
                           prompt: str,
                           model: Optional[str] = None,
                           aspect_ratio: Optional[str] = None,
                           **kwargs) -> Dict[str, Any]:
        """
        Generate an image based on a prompt using Gemini.

        Args:
            prompt: Text description of the desired image
            model: Optional model override (defaults to configured model)
            size: Optional size specification (not directly supported by Gemini)
            **kwargs: Additional Gemini-specific parameters

        Returns:
            Dictionary containing the response with image data
        """
        model_name = model or self.default_model

        # If using an Imagen model, delegate to generate_images
        if "imagen" in model_name.lower():
            imgs = await self._generate_with_imagen(prompt, count=1, model=model_name, aspect_ratio=aspect_ratio, **kwargs)
            if not imgs or not imgs[0].get("success", False):
                return imgs[0] if imgs else {"success": False, "error": "No images returned from Imagen"}
            return imgs[0]

        # Configure response modalities: flash-exp needs both Text and Image, others only Image
        if "flash-exp" in model_name.lower():
            modalities = ["Text", "Image"]
        else:
            modalities = ["Image"]
        config = types.GenerateContentConfig(
            response_modalities=modalities,
            **kwargs
        )

        # Generate content using generate_content
        try:
            print("DEBUG - Generating image content")
            try:
                response = await self.client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=config
                )
            except TypeError:
                response = self.client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=config
                )
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to generate image: {str(e)}",
                "model": model_name,
                "prompt": prompt
            }

        # Extract image data from response
        try:
            image_data = None
            text_response = ""

            # Check if response has candidates
            if not hasattr(response, 'candidates') or not response.candidates:
                return {
                    "success": False,
                    "error": "No candidates in response",
                    "raw_response": str(response)
                }

            # Check if the first candidate has content
            if not hasattr(response.candidates[0], 'content'):
                return {
                    "success": False,
                    "error": "No content in first candidate",
                    "raw_response": str(response)
                }

            # Check if content has parts
            if not hasattr(response.candidates[0].content, 'parts'):
                return {
                    "success": False,
                    "error": "No parts in content",
                    "raw_response": str(response)
                }

            # Extract text and image data from parts
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'text') and part.text is not None:
                    text_response += part.text
                elif hasattr(part, 'inline_data') and part.inline_data is not None:
                    image_data = part.inline_data.data

            # If no image was generated, return an error
            if not image_data:
                return {
                    "success": False,
                    "error": "No image was generated",
                    "text_response": text_response,
                    "raw_response": str(response)
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error processing response: {str(e)}",
                "raw_response": str(response)
            }

        # Check if image_data is already a base64 string
        if isinstance(image_data, str):
            # If it's already a string, assume it's base64
            image_base64 = image_data
            print("DEBUG - Image data is already a base64 string")
        else:
            # Otherwise, encode it
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            print("DEBUG - Encoded image data to base64")

        return {
            "success": True,
            "image_data": image_base64,
            "mime_type": "image/png",  # Assuming PNG format
            "text_response": text_response,
            "model": model_name
        }

    async def edit_image(self,
                       image_data: bytes,
                       prompt: str,
                       model: Optional[str] = None,
                       **kwargs) -> Dict[str, Any]:
        """
        Edit an existing image based on a prompt using Gemini.

        Args:
            image_data: Binary data of the image to edit
            prompt: Text description of the desired edits
            model: Optional model override (defaults to configured model)
            **kwargs: Additional Gemini-specific parameters

        Returns:
            Dictionary containing the response with the edited image data
        """
        model_name = model or self.default_model

        # Create a PIL Image from the binary data
        try:
            image = Image.open(BytesIO(image_data))
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to process image: {str(e)}"
            }

        # Configure response modalities to include image
        config = types.GenerateContentConfig(
            response_modalities=['Text', 'Image'],
            **kwargs
        )

        # Create content with text and image
        contents = [
            prompt,
            {
                "inline_data": {
                    "mime_type": f"image/{image.format.lower()}" if image.format else "image/png",
                    "data": image_data
                }
            }
        ]

        # Generate content
        # The new Gemini API might not be fully async, so we need to handle it properly
        try:
            # Try to use it as an awaitable
            response = await self.client.models.generate_content(
                model=model_name,
                contents=contents,
                config=config
            )
        except TypeError:
            # If it's not awaitable, use it directly
            response = self.client.models.generate_content(
                model=model_name,
                contents=contents,
                config=config
            )

        # Extract image data from response
        edited_image_data = None
        text_response = ""

        for part in response.candidates[0].content.parts:
            if part.text is not None:
                text_response += part.text
            elif part.inline_data is not None:
                edited_image_data = part.inline_data.data

        # If no image was generated, return an error
        if not edited_image_data:
            return {
                "success": False,
                "error": "No edited image was generated",
                "text_response": text_response
            }

        # Convert image data to base64 for easy transmission
        image_base64 = base64.b64encode(edited_image_data).decode('utf-8')

        return {
            "success": True,
            "image_data": image_base64,
            "mime_type": "image/png",  # Assuming PNG format
            "text_response": text_response,
            "model": model_name
        }

    async def generate_multiple_images(self,
                                    prompt: str,
                                    count: int = 1,
                                    model: Optional[str] = None,
                                    aspect_ratio: Optional[str] = None,
                                    **kwargs) -> List[Dict[str, Any]]:
        """
        Generate multiple images based on a prompt using Imagen.

        Args:
            prompt: Text description of the desired images
            count: Number of images to generate (1-4)
            model: Optional model override (defaults to configured model)
            aspect_ratio: Optional aspect ratio specification (not directly supported by Gemini)
            **kwargs: Additional Gemini-specific parameters

        Returns:
            List of dictionaries containing the responses with image data
        """
        # For Imagen model, use a different approach
        if model and "imagen" in model:
            return await self._generate_with_imagen(prompt, count, model, **kwargs)

        # For Gemini model, generate images one by one
        results = []
        for _ in range(count):
            result = await self.generate_image(prompt, model, size, **kwargs)
            if result["success"]:
                results.append(result)

        return results

    async def _generate_with_imagen(self,
                                  prompt: str,
                                  count: int = 1,
                                  model: str = "imagen-3.0-generate-002",
                                  aspect_ratio: Optional[str] = None,
                                  **kwargs) -> List[Dict[str, Any]]:
        """
        Generate images using Imagen model.

        Args:
            prompt: Text description of the desired images
            count: Number of images to generate (1-4)
            model: Imagen model to use
            **kwargs: Additional Imagen-specific parameters

        Returns:
            List of dictionaries containing the responses with image data
        """
        # Ensure count is within valid range (1-4)
        count = max(1, min(4, count))

        # Generate images
        # The new Gemini API might not be fully async, so we need to handle it properly
        try:
            # Try to use it as an awaitable
            response = await self.client.models.generate_images(
                model=model,
                prompt=prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=count,
                    aspect_ratio=aspect_ratio,
                    **kwargs
                )
            )
        except TypeError:
            # If it's not awaitable, use it directly
            response = self.client.models.generate_images(
                model=model,
                prompt=prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=count,
                    aspect_ratio=aspect_ratio,
                    **kwargs
                )
            )

        results = []

        # Process each generated image
        for generated_image in response.generated_images:
            image_bytes = generated_image.image.image_bytes
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')

            results.append({
                "success": True,
                "image_data": image_base64,
                "mime_type": "image/png",  # Imagen generates PNG images
                "model": model
            })

        return results
