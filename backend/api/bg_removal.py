"""
Background removal utility for visuals in video generation.
"""
from PIL import Image
from rembg import remove
import os

def remove_background_from_image(image_path: str, background_path: str, output_path: str = None):
    """
    Removes the background from the given image using rembg and composites it over the project background image.
    Args:
        image_path: Path to the input image.
        background_path: Path to the project background image.
        output_path: Optional path to save the composited output image.
    Returns:
        If output_path is provided: Path to the composited output image.
        If output_path is None: The composited PIL Image object.
    """
    img = Image.open(image_path).convert("RGBA")
    bg = Image.open(background_path).convert("RGBA")
    bg = bg.resize(img.size)

    img_no_bg = remove(img)
    if not isinstance(img_no_bg, Image.Image):
        img_no_bg = Image.open(img_no_bg).convert("RGBA")

    composite = Image.alpha_composite(bg, img_no_bg)
    if output_path:
        composite.save(output_path)
        return output_path
    else:
        return composite
