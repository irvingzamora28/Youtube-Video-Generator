"""
API endpoint for background removal preview (returns base64, does not save file).
"""
from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from typing import Optional
from backend.api.bg_removal import remove_background_from_image
from PIL import Image
import requests
import io
import base64
import tempfile
import os

router = APIRouter(prefix="/api/bg_removal", tags=["Background Removal"])

class BgRemovalPreviewRequest(BaseModel):
    image_url: str
    background_url: Optional[str] = None
    project_id: Optional[int] = None
    method: Optional[str] = 'color'  # 'color' or 'rembg'
    removeBackgroundMethod: Optional[str] = None  # camelCase for frontend compatibility
    tolerance: Optional[int] = None

@router.post("/preview")
def preview_bg_removal(payload: BgRemovalPreviewRequest):
    """
    Accepts image_url and optional background_url, returns base64 PNG of composited image.
    """
    try:
        # Download images
        def resolve_image(image_url):
            # Handle local static files
            if image_url.startswith("/static/") or image_url.startswith("static/"):
                # Remove leading slash if present
                rel_path = image_url.lstrip("/")
                # Find absolute path relative to backend dir
                backend_dir = os.path.dirname(os.path.dirname(__file__))
                abs_path = os.path.join(backend_dir, rel_path)
                if not os.path.exists(abs_path):
                    raise FileNotFoundError(f"File not found: {abs_path}")
                return Image.open(abs_path).convert("RGBA")
            elif image_url.startswith("http://") or image_url.startswith("https://"):
                resp = requests.get(image_url)
                resp.raise_for_status()
                return Image.open(io.BytesIO(resp.content)).convert("RGBA")
            else:
                raise ValueError(f"Invalid image_url: {image_url}")

        img = resolve_image(payload.image_url)
        bg = None
        if payload.background_url:
            bg = resolve_image(payload.background_url)
            bg = bg.resize(img.size)
        elif payload.project_id is not None:
            # Try to get project background image
            from backend.models.project import Project
            project = Project.get_by_id(payload.project_id)
            if project and project.background_image and os.path.exists(project.background_image):
                bg = Image.open(project.background_image).convert("RGBA").resize(img.size)
        if bg is None:
            bg = Image.new("RGBA", img.size, (255,255,255,0))
        # Save img and bg to temp files because remove_background_from_image expects file paths
        with tempfile.NamedTemporaryFile(suffix='.png') as img_tmp, tempfile.NamedTemporaryFile(suffix='.png') as bg_tmp:
            img.save(img_tmp.name)
            bg.save(bg_tmp.name)
            method = payload.removeBackgroundMethod or payload.method or 'color'
            composite = remove_background_from_image(
                img_tmp.name,
                bg_tmp.name,
                output_path=None,
                method=method,
                tolerance=payload.tolerance if payload.tolerance is not None else 20
            )
        # Encode to base64
        buf = io.BytesIO()
        composite.save(buf, format="PNG")
        base64_img = base64.b64encode(buf.getvalue()).decode("utf-8")
        return {"base64_png": base64_img}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
