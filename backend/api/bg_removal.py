"""
Background removal utility for visuals in video generation.
"""
from PIL import Image
from rembg import remove
import os

def remove_background_from_image(image_path: str, background_path: str, output_path: str = None, method: str = 'color', tolerance: int = 20):
    """
    Removes the background from the given image and composites it over the project background image.

    Args:
        image_path: Path to the input image.
        background_path: Path to the project background image.
        output_path: Optional path to save the composited output image.
        method: 'color' (remove background similar to top-left pixel), or 'rembg' (remove white background). Default 'color'.
        tolerance: Color distance threshold for background removal (default 20).
    Returns:
        If output_path is provided: Path to the composited output image.
        If output_path is None: The composited PIL Image object.
    """
    img = Image.open(image_path).convert("RGBA")
    bg = Image.open(background_path).convert("RGBA")
    bg = bg.resize(img.size)

    import numpy as np
    arr = np.array(img)

    if method == 'color':
        # Remove all pixels close to the average color of the top-left 5x5 patch
        print(f"Removing background with method {method} and tolerance {tolerance}")
        corner_patch = arr[:5, :5, :3].reshape(-1, 3)
        target_color = corner_patch.mean(axis=0)
        print(f"Target color (mean of top-left 5x5): {target_color}")
        color_diff = np.linalg.norm(arr[:, :, :3] - target_color, axis=2)
        mask = color_diff < tolerance
        print(f"Number of pixels removed: {mask.sum()} out of {mask.size}")
        # Show unique colors being removed (sample up to 20 for brevity)
        removed_colors = arr[:, :, :3][mask]
        unique_removed = np.unique(removed_colors, axis=0)
        print(f"Number of unique colors removed: {len(unique_removed)}")
        print(f"Sample of unique colors removed (up to 20): {unique_removed[:20]}")
        arr[mask, 3] = 0  # Set alpha to 0 for background pixels
        img_no_bg = Image.fromarray(arr, mode="RGBA")
    elif method == 'rembg':
        # Use rembg to remove background
        img_no_bg = remove(img)
        if not isinstance(img_no_bg, Image.Image):
            img_no_bg = Image.open(img_no_bg).convert("RGBA")
    else:
        raise ValueError(f"Unknown background removal method: {method}")

    composite = Image.alpha_composite(bg, img_no_bg)
    if output_path:
        composite.save(output_path)
        return output_path
    else:
        return composite
