"""
File storage utilities for the video generation project.
"""
import os
import base64
import uuid
from pathlib import Path
from typing import Optional, Tuple
import logging
from io import BytesIO
from PIL import Image

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Storage directory
STORAGE_DIR = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "storage")))

def ensure_storage_dirs():
    """
    Ensure that the storage directories exist.
    """
    # Create main storage directory
    os.makedirs(STORAGE_DIR, exist_ok=True)

    # Create projects directory
    projects_dir = STORAGE_DIR / "projects"
    os.makedirs(projects_dir, exist_ok=True)

    logger.info(f"Storage directories initialized at {STORAGE_DIR}")

def get_project_dir(project_id: int) -> Path:
    """
    Get the directory for a project.

    Args:
        project_id: The ID of the project

    Returns:
        Path to the project directory
    """
    project_dir = STORAGE_DIR / "projects" / str(project_id)
    os.makedirs(project_dir, exist_ok=True)

    # Create subdirectories
    images_dir = project_dir / "images"
    audio_dir = project_dir / "audio"
    video_dir = project_dir / "video"
    video_segments_dir = video_dir / "segments"

    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(audio_dir, exist_ok=True)
    os.makedirs(video_dir, exist_ok=True)
    os.makedirs(video_segments_dir, exist_ok=True)

    return project_dir

def save_asset(data: bytes, project_id: int, asset_type: str, asset_id: str = None, extension: str = None) -> Tuple[bool, Optional[str]]:
    """
    Save an asset to the file system.

    Args:
        data: Binary data of the asset
        project_id: The ID of the project
        asset_type: Type of asset ('image', 'audio', 'video')
        asset_id: The ID of the asset (optional)
        extension: File extension (optional, defaults based on asset_type)

    Returns:
        Tuple of (success, file_path)
    """
    try:
        # Get the project directory
        project_dir = get_project_dir(project_id)

        # Determine the subdirectory based on asset type
        if asset_type == 'image':
            subdir = project_dir / "images"
            default_ext = ".png"
        elif asset_type == 'audio':
            subdir = project_dir / "audio"
            default_ext = ".mp3"
        elif asset_type == 'video':
            if asset_id and asset_id.startswith('segment_'):
                subdir = project_dir / "video" / "segments"
            else:
                subdir = project_dir / "video"
            default_ext = ".mp4"
        else:
            subdir = project_dir / asset_type
            default_ext = ".bin"
            os.makedirs(subdir, exist_ok=True)

        # Use provided extension or default
        ext = extension or default_ext

        # Generate a unique filename if asset_id is not provided
        if asset_id is None:
            filename = f"{uuid.uuid4()}{ext}"
        else:
            filename = f"{asset_id}{ext}"

        # Save the asset
        file_path = subdir / filename

        with open(file_path, 'wb') as f:
            f.write(data)

        # Return the relative path from the storage directory
        relative_path = os.path.relpath(file_path, STORAGE_DIR)

        logger.info(f"Saved {asset_type} to {file_path}")
        return True, relative_path

    except Exception as e:
        logger.error(f"Error saving {asset_type}: {str(e)}")
        return False, None

def save_base64_image(base64_data: str, project_id: int, visual_id: str = None) -> Tuple[bool, Optional[str]]:
    """
    Save a base64-encoded image to the file system.

    Args:
        base64_data: Base64-encoded image data
        project_id: The ID of the project
        visual_id: The ID of the visual (optional)

    Returns:
        Tuple of (success, file_path)
    """
    try:
        # Remove data URL prefix if present
        if "," in base64_data:
            base64_data = base64_data.split(",", 1)[1]

        # Decode the base64 data
        image_data = base64.b64decode(base64_data)

        # Validate the image using PIL
        img = Image.open(BytesIO(image_data))

        # Convert to PNG format
        output = BytesIO()
        img.save(output, format='PNG')
        png_data = output.getvalue()

        # Save the image as an asset
        return save_asset(png_data, project_id, 'image', visual_id)

    except Exception as e:
        logger.error(f"Error processing base64 image: {str(e)}")
        return False, None

def load_image_as_base64(file_path: str) -> Tuple[bool, Optional[str]]:
    """
    Load an image from the file system and convert it to base64.

    Args:
        file_path: Path to the image file (relative to storage directory)

    Returns:
        Tuple of (success, base64_data)
    """
    try:
        # Get the absolute path
        abs_path = STORAGE_DIR / file_path

        # Read the image file
        with open(abs_path, "rb") as f:
            image_data = f.read()

        # Convert to base64
        base64_data = base64.b64encode(image_data).decode("utf-8")

        return True, base64_data

    except Exception as e:
        logger.error(f"Error loading image: {str(e)}")
        return False, None

def delete_file(file_path: str) -> bool:
    """
    Delete a file from the file system.

    Args:
        file_path: Path to the file (relative to storage directory)

    Returns:
        True if successful, False otherwise
    """
    try:
        # Get the absolute path
        abs_path = STORAGE_DIR / file_path

        # Delete the file
        os.remove(abs_path)

        logger.info(f"Deleted file {abs_path}")
        return True

    except Exception as e:
        logger.error(f"Error deleting file: {str(e)}")
        return False

# Initialize storage directories if this module is run directly
if __name__ == "__main__":
    ensure_storage_dirs()
