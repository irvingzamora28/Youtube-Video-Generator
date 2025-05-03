"""
Image generation API endpoints.
"""
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form, BackgroundTasks
from typing import Dict, Any, Optional, List
import base64
from pydantic import BaseModel

import os
import uuid
import base64
from backend.llm.image_generation import ImageGenerationProvider
from backend.llm.image_factory import create_image_provider
from backend.models.asset import Asset
from backend.models.project import Project
from backend.config.settings import settings

# Create router
router = APIRouter(prefix="/api/image", tags=["Image"])

# Dependencies
def get_image_provider() -> ImageGenerationProvider:
    """
    Get the image provider from environment variables.
    """
    try:
        print("DEBUG - Creating image provider from environment variables")
        return create_image_provider()
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

# Request model for image description generation
class ImageDescriptionRequest(BaseModel):
    script: str
    narration: str
    selected_text: str

# Request model for generating visuals for a segment
class GenerateVisualsForSegmentRequest(BaseModel):
    segment_id: str
    narration_text: str

# Routes
async def generate_image_description_text(script: str, narration: str, selected_text: str) -> str:
    """
    Generate an image description for the selected text, using the full script and narration as context.
    Returns only the description string.
    """
    from backend.llm.factory import create_llm_provider_from_env
    llm_provider = create_llm_provider_from_env()
    prompt = (
        "You are an expert at writing vivid, concise image descriptions for video generation. "
        "Given the full script, the current segment narration, and a specific text selection, "
        "generate an improved, detailed image description that best represents the selected text. "
        "The description should be visual, specific, MINIMALISTIC and suitable for an image generation model.\n"
        f"Full Script:\n{script}\n"
        f"Current Segment Narration:\n{narration}\n"
        f"Selected Text (to represent):\n{selected_text}\n"
        "Image Description:"
    )
    response = await llm_provider.generate_completion(
        messages=[{"role": "user", "content": prompt}],
        model=None, temperature=0.7, max_tokens=400
    )
    description = response["content"] if isinstance(response, dict) else str(response)
    return description.strip()

@router.post("/generate-description")
async def generate_image_description(request: ImageDescriptionRequest):
    """
    Generate an image description for the selected text, using the full script and narration as context.
    """
    try:
        description = await generate_image_description_text(request.script, request.narration, request.selected_text)
        return {"description": description}
    except Exception as e:
        import traceback
        print("[generate_image_description] Error:", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate")
async def generate_image(
    request: ImageGenerationRequest,
    image_provider: ImageGenerationProvider = Depends(get_image_provider)
):
    """
    Generate an image based on a prompt.
    """
    try:
        print(f"[generate_image] Request: prompt='{request.prompt[:50]}...', model={request.model}, aspect_ratio={request.aspect_ratio}")
        print(f"[generate_image] Prompt: {request.prompt}")
        # prompt = f"Generate a {visual.get('visualType', 'image')} of: {description}. Style: {visual_style or 'simple, clear, educational'}."
        result = await image_provider.generate_image(request.prompt, request.model, request.aspect_ratio)

        if not result.get('success', False):
            error_msg = result.get('error', 'Unknown image generation error')
            print(f"[ERROR][generate_image] Image generation failed: {error_msg}")
            raise HTTPException(status_code=500, detail=error_msg)

        # Return success and image data
        return {
            "success": True,
            "image_data": result.get('image_data'), # Base64 encoded
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


# --- Helper Function for Generating/Saving/Linking ---
async def _generate_and_link_image_for_visual(
    project_id: int,
    segment_id: str,
    visual: dict, # Pass the whole visual dict
    image_provider: ImageGenerationProvider
) -> tuple[dict | None, dict | None]:
    """
    Internal helper: Generates image, deletes old asset, saves new asset, returns update data.
    Does NOT save the project itself.

    Args:
        project_id: ID of the project.
        segment_id: ID of the segment containing the visual.
        visual: The dictionary representing the visual from project content.
        image_provider: Instance of the image generation provider.

    Returns:
        tuple[dict | None, dict | None]: (new_asset_dict, visual_update_data) or (None, None) on failure.
    """
    visual_id = visual.get('id')
    description = visual.get('description')
    visual_style = visual.get('visualStyle')
    existing_asset_id = visual.get('assetId')

    if not description:
        print(f"[_generate_and_link_image] Skipping visual {visual_id}: No description.")
        return None, None

    print(f"[_generate_and_link_image] Processing visual {visual_id} for segment {segment_id}. Description: '{description[:50]}...'")

    # --- Delete existing asset if regenerating ---
    if existing_asset_id:
        print(f"[_generate_and_link_image] Regenerating image for visual {visual_id}. Deleting old asset ID: {existing_asset_id}")
        try:
            old_asset = Asset.get_by_id(existing_asset_id)
            if old_asset and old_asset.asset_type == 'image':
                old_file_path = os.path.join(settings.static_dir, old_asset.path)
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)
                    print(f"[_generate_and_link_image] Deleted old image file: {old_file_path}")
                deleted_db = old_asset.delete()
                if deleted_db: print(f"[_generate_and_link_image] Deleted old image asset record ID: {existing_asset_id}")
                else: print(f"[WARNING] Failed to delete old image asset record ID: {existing_asset_id}")
            elif old_asset: print(f"[WARNING] Asset ID {existing_asset_id} is not 'image' type.")
            else: print(f"[WARNING] Old asset ID {existing_asset_id} not found.")
        except Exception as e:
            print(f"[ERROR] Failed during deletion of old image asset {existing_asset_id}: {e}")
            # Continue even if deletion fails

    # --- Generate New Image ---
    try:
        # Construct prompt (similar to frontend logic)
        prompt = f"Generate a {visual.get('visualType', 'image')} of: {description}. Style: {visual_style or 'simple, clear, educational'}."
        print(f"[_generate_and_link_image] Generating image with prompt: '{prompt[:100]}...'")
        # Assuming generate_image returns base64 data directly now
        gen_result = await image_provider.generate_image(prompt=prompt, aspect_ratio="16:9") # Add aspect ratio if needed

        if not gen_result or not gen_result.get('success') or not gen_result.get('image_data'):
             error_msg = gen_result.get('error', 'Unknown image generation error')
             print(f"[ERROR][_generate_and_link_image] Image generation failed for visual {visual_id}: {error_msg}")
             return None, None

        image_data_b64 = gen_result['image_data']

    except Exception as e:
        print(f"[ERROR][_generate_and_link_image] Exception during image generation for visual {visual_id}: {e}")
        return None, None

    # --- Save New Image File ---
    try:
        header, _, data = image_data_b64.partition(",")
        image_bytes = base64.b64decode(data if data else image_data_b64)

        img_dir = os.path.join(settings.static_dir, "projects", str(project_id), "segments", str(segment_id)) # Image saved in segment dir, not sub-dir like audio
        os.makedirs(img_dir, exist_ok=True)
        filename = f"{uuid.uuid4().hex}.png" # Assume PNG
        output_path = os.path.join(img_dir, filename)
        rel_path = os.path.relpath(output_path, start=settings.static_dir).replace("\\", "/")

        print(f"[_generate_and_link_image] Writing image to {output_path}")
        with open(output_path, "wb") as f:
            f.write(image_bytes)
        print(f"[_generate_and_link_image] Image written successfully.")

    except Exception as e:
        print(f"[ERROR][_generate_and_link_image] Failed to decode/save image file for visual {visual_id}: {e}")
        return None, None

    # --- Create New Asset Record ---
    metadata = {
        "segment_id": segment_id,
        "visual_id": visual_id,
        "description": description,
        "visual_style": visual_style,
        "timestamp": visual.get("timestamp"),
        "duration": visual.get("duration")
    }
    asset = Asset(project_id=project_id, asset_type="image", path=rel_path, metadata=metadata)
    asset_saved = asset.save()
    if not asset_saved or asset.id is None:
        print(f"[ERROR] Failed to save image asset to DB for visual {visual_id}")
        if os.path.exists(output_path): os.remove(output_path) # Cleanup attempt
        return None, None

    print(f"[_generate_and_link_image] Asset saved for visual {visual_id}: ID {asset.id}")

    # --- Prepare Visual Update Data ---
    visual_update_data = {
        'imageUrl': asset.path,
        'assetId': asset.id
    }

    return asset.to_dict(), visual_update_data


# --- Bulk Generation Endpoint ---

@router.post("/generate_highlight_images/{project_id}")
async def generate_highlight_images_for_project(
    project_id: int,
    aspect_ratio: str = "16:9",
    image_provider: ImageGenerationProvider = Depends(get_image_provider)
):
    """
    Generate images for all infocard highlights of a project, store them, and update highlights with image URLs.
    """
    project = Project.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project {project_id} not found.")
    highlights = project.infocard_highlights or []
    if not highlights:
        raise HTTPException(status_code=400, detail="No infocard highlights found for this project.")

    static_dir = os.path.join(settings.static_dir, str(project_id), "highlights")
    os.makedirs(static_dir, exist_ok=True)
    updated_highlights = []
    for idx, highlight in enumerate(highlights):
        prompt = highlight.get("visual_description") or highlight.get("text")
        if not prompt:
            updated_highlights.append(highlight)
            continue
        try:
            result = await image_provider.generate_image(prompt=prompt, aspect_ratio=aspect_ratio)
            if not result.get("success") or not result.get("image_data"):
                highlight["image_url"] = None
                updated_highlights.append(highlight)
                continue
            image_data_b64 = result["image_data"]
            header, _, data = image_data_b64.partition(",")
            image_bytes = base64.b64decode(data if data else image_data_b64)
            filename = f"highlight_{idx+1}.png"
            output_path = os.path.join(static_dir, filename)
            with open(output_path, "wb") as f:
                f.write(image_bytes)
            rel_path = os.path.relpath(output_path, start=settings.static_dir).replace("\\", "/")
            highlight["image_url"] = f"/static/{project_id}/highlights/{filename}"
        except Exception as e:
            print(f"[generate_highlight_images_for_project] Error for highlight {idx}: {e}")
            highlight["image_url"] = None
        updated_highlights.append(highlight)
    project.infocard_highlights = updated_highlights
    project.save()
    return {"success": True, "highlights": updated_highlights}

async def _bulk_generate_images_task(project_id: int, image_provider: ImageGenerationProvider):
    """Background task to generate images for all visuals in a project."""
    print(f"[_bulk_generate_images_task] Starting bulk image generation for project {project_id}")
    project = Project.get_by_id(project_id)
    if not project:
        print(f"[ERROR][_bulk_generate_images_task] Project {project_id} not found.")
        return

    visuals_processed = 0
    visuals_failed = 0
    project_updated = False

    # Iterate through all visuals in all segments
    for section in project.content.get('sections', []):
        for segment in section.get('segments', []):
            segment_id = segment.get('id')
            for i, visual in enumerate(segment.get('visuals', [])):
                visual_id = visual.get('id')
                description = visual.get('description')

                if not visual_id or not description:
                    print(f"[_bulk_generate_images_task] Skipping visual {i} in segment {segment_id}: Missing ID or description.")
                    continue

                # Skip if image already exists (optional)
                # if visual.get('imageUrl'):
                #      print(f"[_bulk_generate_images_task] Skipping visual {visual_id}: Image already exists.")
                #      continue

                print(f"[_bulk_generate_images_task] Processing visual {visual_id}...")
                asset_dict, visual_update_data = await _generate_and_link_image_for_visual(
                    project_id=project_id,
                    segment_id=segment_id,
                    visual=visual, # Pass the whole visual dict
                    image_provider=image_provider
                )

                if asset_dict and visual_update_data:
                    # Update the visual data *within the project.content dictionary*
                    visual.update(visual_update_data)
                    project_updated = True
                    visuals_processed += 1
                    print(f"[_bulk_generate_images_task] Successfully processed visual {visual_id}")
                else:
                    visuals_failed += 1
                    print(f"[ERROR][_bulk_generate_images_task] Failed to process visual {visual_id}")

                import time # Add delay between image generations
                time.sleep(2) # Adjust delay as needed

    # Save the project *once* after processing all visuals if any updates were made
    if project_updated:
        print(f"[_bulk_generate_images_task] Saving updated project {project_id} with new image data...")
        save_success = project.save()
        if save_success:
            print(f"[_bulk_generate_images_task] Project {project_id} saved successfully.")
        else:
            print(f"[ERROR][_bulk_generate_images_task] Failed to save project {project_id} after bulk image generation.")
    else:
         print(f"[_bulk_generate_images_task] No visuals required image generation for project {project_id}.")

    print(f"[_bulk_generate_images_task] Finished bulk image generation for project {project_id}. Processed: {visuals_processed}, Failed: {visuals_failed}")


@router.post("/generate_all_project_images/{project_id}")
async def generate_all_project_images(
    project_id: int,
    background_tasks: BackgroundTasks,
    image_provider: ImageGenerationProvider = Depends(get_image_provider)
):
    """
    Triggers background generation of images for all visuals in a project.
    """
    project = Project.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project {project_id} not found.")

    print(f"[generate_all_project_images] Adding bulk image generation task for project {project_id} to background.")
    background_tasks.add_task(_bulk_generate_images_task, project_id, image_provider)

    return {"message": f"Image generation for all visuals of project {project_id} started in the background."}


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
