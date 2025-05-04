from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid
from backend.models.asset import Asset
from backend.models.project import Project
from backend.llm.factory import create_llm_provider_from_env
from backend.llm.image_factory import create_image_provider

from fastapi import Query
router = APIRouter(prefix="/api/image", tags=["Image"])


class GenerateVisualsForSegmentRequest(BaseModel):
    project_id: int
    segment_id: str
    narration_text: str

async def _generate_visuals_for_segment_core(project, segment, narration_text, image_provider, aspect_ratio="16:9"):
    """
    Core logic to generate visuals for a segment. Used by both single and bulk endpoints.
    """
    llm_provider = create_llm_provider_from_env()
    prompt = (
        "You are an expert at video narration analysis. Given the following narration, break it down into the minimal set of concise, descriptive parts, each representing a distinct visual or important moment that should be illustrated. "
        "VERY IMPORTANT: Generate at least 2 parts, even if the narration is short."
        "For each part, return an object with two fields: "
        "- 'referenceText': the exact substring from the narration text that this visual should be synced to (do NOT paraphrase, use the exact text). "
        "- 'description': a concise, self-contained description or phrase suitable for image generation. "
        "Return ONLY a JSON array of objects in this format, no explanations.\n\n"
        f"Narration:\n{narration_text}\n"
        "Parts:"
    )
    try:
        response = await llm_provider.generate_completion(
            messages=[{"role": "user", "content": prompt}],
            model=None, temperature=0.5, max_tokens=400
        )
        import json, re
        raw_content = response["content"] if isinstance(response, dict) else str(response)
        cleaned_content = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw_content.strip(), flags=re.IGNORECASE)
        parts = json.loads(cleaned_content)
        if not isinstance(parts, list):
            raise ValueError("LLM did not return a list")
        if parts and isinstance(parts[0], str):
            parts = [
                {"referenceText": p, "description": p} for p in parts
            ]
        for p in parts:
            if not (isinstance(p, dict) and "referenceText" in p and "description" in p):
                raise ValueError("Each part must be an object with 'referenceText' and 'description'")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to break narration into parts: {str(e)}")

    visuals = []
    assets = []
    from backend.api.image import generate_image_description_text

    existing_visuals = segment.get("visuals", [])
    num_existing = len(existing_visuals)
    num_parts = len(parts)
    visuals_to_keep = min(num_existing, num_parts)
    script_text = project.get_full_script()

    # Update visuals for as many as we can reuse
    for idx in range(visuals_to_keep):
        part = parts[idx]
        prev_visual = existing_visuals[idx]
        prev_visual_id = prev_visual.get("id", str(uuid.uuid4()))
        try:
            image_description = part['description']
            reference_text = part['referenceText']
        except Exception as e:
            image_description = part['description']
            reference_text = part['referenceText']
        try:
            prompt = f"Generate an image of: {image_description}. Style: {getattr(project, 'visual_style', 'educational')}."
            img_result = await image_provider.generate_image(prompt, None, aspect_ratio)
            if not img_result.get('success', False):
                raise Exception(img_result.get('error', 'Unknown image generation error'))
            image_data = img_result['image_data']
            mime_type = img_result.get('mime_type', 'image/png')
        except Exception as e:
            image_data = None
            mime_type = None
        asset_id = None
        image_url = None
        if image_data:
            from backend.api.image_save import SaveImagePayload, save_image_asset
            payload = SaveImagePayload(
                project_id=project.id,
                segment_id=segment['id'],
                visual_id=prev_visual_id,
                timestamp=idx * 2.0,
                duration=2.0,
                image_data=image_data,
                description=image_description
            )
            asset_result = await save_image_asset(payload)
            if asset_result.get("success"):
                asset = asset_result["asset"]
                asset_id = asset["id"]
                image_url = f"/static/{asset['path']}"
                assets.append(asset)
        visual = {
            "id": prev_visual_id,
            "description": image_description,
            "timestamp": idx * 2.0,
            "duration": 2.0,
            "imageUrl": image_url,
            "altText": image_description,
            "visualType": "image",
            "visualStyle": project.visual_style or 'stick-man black-white',
            "position": "center",
            "zoomLevel": 1,
            "transition": "fade",
            "removeBackground": True,
            "removeBackgroundMethod": "color",
            "assetId": asset_id,
            "referenceText": reference_text,
        }
        visuals.append(visual)

    # Add new visuals if more parts than existing
    for idx in range(visuals_to_keep, num_parts):
        part = parts[idx]
        visual_id = f"visual-{str(uuid.uuid4())[:10]}"
        try:
            image_description = part['description']
            reference_text = part['referenceText']
        except Exception as e:
            image_description = part if isinstance(part, str) else str(part)
            reference_text = part if isinstance(part, str) else str(part)
        try:
            prompt = f"Generate an image of: {image_description}. Style: {project.visual_style or 'educational'}."
            img_result = await image_provider.generate_image(prompt, None, aspect_ratio)
            if not img_result.get('success', False):
                raise Exception(img_result.get('error', 'Unknown image generation error'))
            image_data = img_result['image_data']
            mime_type = img_result.get('mime_type', 'image/png')
        except Exception as e:
            image_data = None
            mime_type = None
        asset_id = None
        image_url = None
        if image_data:
            from backend.api.image_save import SaveImagePayload, save_image_asset
            payload = SaveImagePayload(
                project_id=project.id,
                segment_id=segment['id'],
                visual_id=visual_id,
                timestamp=idx * 2.0,
                duration=2.0,
                image_data=image_data,
                description=image_description
            )
            asset_result = await save_image_asset(payload)
            if asset_result.get("success"):
                asset = asset_result["asset"]
                asset_id = asset["id"]
                image_url = f"/static/{asset['path']}"
                assets.append(asset)
        visual = {
            "id": visual_id,
            "description": image_description,
            "timestamp": idx * 2.0,
            "duration": 2.0,
            "imageUrl": image_url,
            "altText": image_description,
            "visualType": "image",
            "visualStyle": project.visual_style or 'stick-man black-white',
            "position": "center",
            "zoomLevel": 1,
            "transition": "fade",
            "removeBackground": True,
            "removeBackgroundMethod": "color",
            "assetId": asset_id,
            "referenceText": reference_text,
        }
        visuals.append(visual)

    # Delete extra visuals (and assets) if there are more visuals than parts
    for idx in range(num_parts, num_existing):
        extra_visual = existing_visuals[idx]
        asset_id = extra_visual.get("assetId")
        if asset_id:
            try:
                asset = Asset.get_by_id(asset_id)
                if asset:
                    asset.delete()
            except Exception:
                pass
    segment["visuals"] = visuals
    return {"visuals": visuals, "assets": assets}

@router.post("/generate_visuals_for_segment")
async def generate_visuals_for_segment(request: dict):
    """
    Generate all visuals for a segment based on its narration text.
    - Breaks narration into visual parts (using LLM)
    - Generates image descriptions and images for each part
    - Creates/updates visuals and assets in the DB
    - Replaces visuals in the segment
    - Returns updated visuals
    
    Accepts request body:
      - project_id: int
      - segment_id: str
      - narration_text: str
      - field: Optional[str] = 'content'
      - aspect_ratio: Optional[str] = '16:9'
    """
    # Maintain backward compatibility: accept both pydantic and dict
    if isinstance(request, GenerateVisualsForSegmentRequest):
        req_dict = request.dict()
    else:
        req_dict = request
    project_id = req_dict.get("project_id")
    segment_id = req_dict.get("segment_id")
    narration_text = req_dict.get("narration_text")
    field = req_dict.get("field", "content")
    aspect_ratio = req_dict.get("aspect_ratio", "16:9")
    print(f"[generate_visuals_for_segment] Loading project {project_id} and segment {segment_id} (field={field}, aspect_ratio={aspect_ratio})")
    project = Project.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if field not in ("content", "short_content"):
        raise HTTPException(status_code=400, detail="Invalid field. Must be 'content' or 'short_content'.")
    script_data = getattr(project, field, None)
    if not script_data or not isinstance(script_data, dict):
        raise HTTPException(status_code=400, detail=f"Project has no valid '{field}' field.")
    segment = None
    for section in script_data.get('sections', []):
        for seg in section.get('segments', []):
            if str(seg.get('id')) == str(segment_id):
                segment = seg
                break
        if segment:
            break
    if not segment:
        raise HTTPException(status_code=404, detail="Segment not found")
    image_provider = create_image_provider()
    result = await _generate_visuals_for_segment_core(project, segment, narration_text, image_provider, aspect_ratio)
    setattr(project, field, script_data)
    project.save()
    return {"visuals": result["visuals"], "assets": result["assets"]}

async def _generate_all_project_visuals_core(project, field, image_provider, aspect_ratio="16:9"):
    """
    Bulk generate visuals for all segments in all sections for the specified field.
    """
    if field not in ("content", "short_content"):
        raise HTTPException(status_code=400, detail="Invalid field. Must be 'content' or 'short_content'.")
    script_data = getattr(project, field, None)
    if not script_data or not isinstance(script_data, dict):
        raise HTTPException(status_code=400, detail=f"Project has no valid '{field}' field.")
    total_segments = 0
    errors = []
    visuals_summary = []
    assets_summary = []
    for section in script_data.get('sections', []):
        for segment in section.get('segments', []):
            narration_text = segment.get('narrationText', '')
            if not narration_text:
                continue
            try:
                result = await _generate_visuals_for_segment_core(project, segment, narration_text, image_provider, aspect_ratio)
                visuals_summary.append(result["visuals"])
                assets_summary.extend(result["assets"])
                total_segments += 1
            except Exception as e:
                errors.append(f"Segment {segment.get('id')}: {str(e)}")
    setattr(project, field, script_data)
    project.save()
    return {"visuals": visuals_summary, "assets": assets_summary, "errors": errors}

@router.get("/generate_all_project_visuals/{project_id}")
async def generate_all_project_visuals(project_id: int, field: str = "content", aspect_ratio: str = "16:9"):
    """
    Generate all visuals for a project based on its narration text.
    - Breaks narration into visual parts (using LLM)
    - Generates image descriptions and images for each part
    - Creates/updates visuals and assets in the DB
    - Replaces visuals in the project
    - Returns updated visuals
    """
    print(f"[generate_all_project_visuals] Loading project {project_id}")
    project = Project.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    image_provider = create_image_provider()
    result = await _generate_all_project_visuals_core(project, field, image_provider, aspect_ratio)
    return {"visuals": result["visuals"], "assets": result["assets"], "errors": result["errors"]}
