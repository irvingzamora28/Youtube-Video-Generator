"""
Interface for image generation providers.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List


class ImageGenerationProvider(ABC):
    """Base class for image generation providers."""

    @abstractmethod
    async def generate_image(self, 
                           prompt: str,
                           model: Optional[str] = None,
                           size: Optional[str] = None,
                           **kwargs) -> Dict[str, Any]:
        """
        Generate an image based on a prompt.

        Args:
            prompt: Text description of the desired image
            model: Optional model override (defaults to configured model)
            size: Optional size specification (e.g., "1024x1024")
            **kwargs: Additional provider-specific parameters

        Returns:
            Dictionary containing the response with image data
        """
        pass

    @abstractmethod
    async def edit_image(self,
                       image_data: bytes,
                       prompt: str,
                       model: Optional[str] = None,
                       **kwargs) -> Dict[str, Any]:
        """
        Edit an existing image based on a prompt.

        Args:
            image_data: Binary data of the image to edit
            prompt: Text description of the desired edits
            model: Optional model override (defaults to configured model)
            **kwargs: Additional provider-specific parameters

        Returns:
            Dictionary containing the response with the edited image data
        """
        pass

    @abstractmethod
    async def generate_multiple_images(self,
                                    prompt: str,
                                    count: int = 1,
                                    model: Optional[str] = None,
                                    size: Optional[str] = None,
                                    **kwargs) -> List[Dict[str, Any]]:
        """
        Generate multiple images based on a prompt.

        Args:
            prompt: Text description of the desired images
            count: Number of images to generate
            model: Optional model override (defaults to configured model)
            size: Optional size specification (e.g., "1024x1024")
            **kwargs: Additional provider-specific parameters

        Returns:
            List of dictionaries containing the responses with image data
        """
        pass
