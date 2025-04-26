from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid
from backend.models.asset import Asset
from backend.models.project import Project
from backend.llm.factory import create_llm_provider_from_env
from backend.llm.image_factory import create_image_provider

router = APIRouter(prefix="/api/image", tags=["Image"])


class GenerateVisualsForSegmentRequest(BaseModel):
    project_id: int
    segment_id: str
    narration_text: str

@router.post("/generate_visuals_for_segment")
async def generate_visuals_for_segment(request: GenerateVisualsForSegmentRequest):
    """
    Generate all visuals for a segment based on its narration text.
    - Breaks narration into visual parts (using LLM)
    - Generates image descriptions and images for each part
    - Creates/updates visuals and assets in the DB
    - Replaces visuals in the segment
    - Returns updated visuals
    """
    # Load project by project_id
    print(f"[generate_visuals_for_segment] Loading project {request.project_id} and segment {request.segment_id}")
    project = Project.get_by_id(request.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    content = project.content
    # Find the segment by traversing sections/segments
    segment = None
    for section in content.get('sections', []):
        for seg in section.get('segments', []):
            if str(seg.get('id')) == str(request.segment_id):
                segment = seg
                break
        if segment:
            break
    if not segment:
        raise HTTPException(status_code=404, detail="Segment not found")
    print(f"[generate_visuals_for_segment] Found segment: {segment}")
    narration_text = request.narration_text
    llm_provider = create_llm_provider_from_env()
    image_provider = create_image_provider()

    prompt = (
        "You are an expert at video narration analysis. Given the following narration, break it down into the minimal set of concise, descriptive parts, each representing a distinct visual or important moment that should be illustrated. "
        "Each part should be a short, self-contained description or phrase suitable for image generation. "
        "Return ONLY a JSON array of strings, no explanations.\n\n"
        f"Narration:\n{narration_text}\n"
        "Parts:"
    )
    try:
        print(f"[generate_visuals_for_segment] Prompt: {prompt}")
        response = await llm_provider.generate_completion(
            messages=[{"role": "user", "content": prompt}],
            model=None, temperature=0.5, max_tokens=400
        )
        import json, re
        raw_content = response["content"] if isinstance(response, dict) else str(response)
        # Remove Markdown code block if present
        cleaned_content = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw_content.strip(), flags=re.IGNORECASE)
        parts = json.loads(cleaned_content)
        if not isinstance(parts, list):
            raise ValueError("LLM did not return a list")
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
    print(f"[generate_visuals_for_segment] Parts: {parts}")
    print(f"[generate_visuals_for_segment] Segment ID: {segment['id']}")

    # Update visuals for as many as we can reuse
    for idx in range(visuals_to_keep):
        part = parts[idx]
        prev_visual = existing_visuals[idx]
        
        prev_visual_id = prev_visual.get("id", str(uuid.uuid4()))
        
        try:
            # For now use part as image description as it turned out to be better for generating images using Google Imagen 3
            image_description = part
            # image_description = await generate_image_description_text(
            #     script=script_text,
            #     narration=narration_text,
            #     selected_text=part
            # )
        except Exception as e:
            image_description = part
        try:
            prompt = f"Generate an image of: {image_description}. Style: {getattr(project, 'visual_style', 'educational')}."
            img_result = await image_provider.generate_image(prompt, None, "16:9")
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
            if asset_result and asset_result.get("success"):
                asset = asset_result["asset"]
                asset_id = asset["id"]
                image_url = f"/static/{asset['path']}"
                assets.append(asset)
        # Update the existing visual, preserve its id
        visual = {
            "id": prev_visual_id,
            "description": image_description,
            "timestamp": idx * 2.0,
            "duration": 2.0,
            "imageUrl": image_url,
            "altText": image_description,
            "visualType": "image",
            "visualStyle": prev_visual.get("visualStyle", ""),
            "position": prev_visual.get("position", "center"),
            "zoomLevel": prev_visual.get("zoomLevel", 1),
            "transition": prev_visual.get("transition", "fade"),
            "removeBackground": prev_visual.get("removeBackground", True),
            "removeBackgroundMethod": prev_visual.get("removeBackgroundMethod", "color"),
            "assetId": asset_id,
        }
        visuals.append(visual)

    # For extra parts, create new visuals
    for idx in range(visuals_to_keep, num_parts):
        part = parts[idx]
        visual_id = f"visual-{str(uuid.uuid4())[:10]}"
        print(f"[generate_visuals_for_segment] Generating image for part {idx}: {part}")
        try:
            # For now use part as image description as it turned out to be better for generating images using Google Imagen 3
            image_description = part
            # image_description = await generate_image_description_text(
            #     script=script_text,
            #     narration=narration_text,
            #     selected_text=part
            # )
            print(f"[generate_visuals_for_segment] Image description: {image_description}")
        except Exception as e:
            print(f"[generate_visuals_for_segment] Failed to generate image description: {e}")
            image_description = part
        try:
            prompt = f"Generate an image of: {image_description}. Style: {project.visual_style or 'educational'}."
            print(f"[generate_visuals_for_segment] Image generation prompt: {prompt}")
            img_result = await image_provider.generate_image(prompt, None, "16:9")
            print(f"[generate_visuals_for_segment] Image provider result: {img_result[:50]}")
            if not img_result.get('success', False):
                print(f"[generate_visuals_for_segment] Image generation failed: {img_result.get('error', 'Unknown image generation error')}")
                raise Exception(img_result.get('error', 'Unknown image generation error'))
            image_data = img_result['image_data']
            mime_type = img_result.get('mime_type', 'image/png')
        except Exception as e:
            print(f"[generate_visuals_for_segment] Exception during image generation: {e}")
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
            print(f"[generate_visuals_for_segment] Saving image asset with payload: {payload}")
            asset_result = await save_image_asset(payload)
            # print(f"[generate_visuals_for_segment] Asset save result: {asset_result}")
            if asset_result.get("success"):
                asset = asset_result["asset"]
                asset_id = asset["id"]
                image_url = f"/static/{asset['path']}"
                assets.append(asset)
                print(f"[generate_visuals_for_segment] Created asset: {asset}")
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
        }
        print(f"[generate_visuals_for_segment] Visual created: {visual}")
        visuals.append(visual)

    # Delete extra visuals (and assets) if there are more visuals than parts
    for idx in range(num_parts, num_existing):
        extra_visual = existing_visuals[idx]
        # Optionally delete associated asset
        asset_id = extra_visual.get("assetId")
        if asset_id:
            try:
                asset = Asset.get_by_id(asset_id)
                if asset:
                    asset.delete()
            except Exception:
                pass
    # 4. Replace visuals in segment (truncate or add)
    segment["visuals"] = visuals
    # 5. Save the project to persist the updated visuals
    project.save()
    # 6. Return visuals and assets
    return {"visuals": segment["visuals"], "assets": assets}
