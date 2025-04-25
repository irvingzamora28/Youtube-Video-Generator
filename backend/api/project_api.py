"""
Project API endpoints.
"""
from fastapi import APIRouter, HTTPException, Depends, Body, File, UploadFile, Form
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
import base64
import json
import shutil
import os
from io import BytesIO
from backend.models.visual import Visual
from backend.models.segment import Segment
from backend.models.section import Section
from backend.models.project import Project
from backend.models.asset import Asset
from backend.database.db import init_db
from backend.utils.file_storage import ensure_storage_dirs, save_asset, save_base64_image, load_image_as_base64

# Initialize database and storage
init_db()
ensure_storage_dirs()

# Create router
router = APIRouter(prefix="/api/project", tags=["Project"])

# Request models
class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    target_audience: Optional[str] = ""
    style: Optional[str] = None
    visual_style: Optional[str] = None

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    target_audience: Optional[str] = None
    total_duration: Optional[float] = None
    status: Optional[str] = None
    style: Optional[str] = None
    visual_style: Optional[str] = None

class ScriptUpdate(BaseModel):
    content: Dict[str, Any]

class AssetCreate(BaseModel):
    asset_type: str
    metadata: Optional[Dict[str, Any]] = None
    base64_data: Optional[str] = None

class AssetUpdate(BaseModel):
    metadata: Optional[Dict[str, Any]] = None

@router.post("/{project_id}/background-image")
async def upload_background_image(project_id: int, file: UploadFile = File(...)):
    """
    Upload a background image for a project. Stores the image locally and updates the project.
    """
    project = Project.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    # Create directory if needed
    bg_dir = f"static/projects/{project_id}/background"
    os.makedirs(bg_dir, exist_ok=True)
    # Save file
    file_ext = os.path.splitext(file.filename)[1]
    filename = f"background{file_ext}"
    file_path = os.path.join(bg_dir, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # Store relative path
    rel_path = os.path.relpath(file_path, start=".")
    project.background_image = rel_path
    if project.save():
        return {"success": True, "background_image": rel_path, "project": project.to_dict()}
    else:
        raise HTTPException(status_code=500, detail="Failed to update project with background image")

@router.get("/")
async def get_all_projects():
    """
    Get all projects.
    """
    projects = Project.get_all()
    return {"projects": [project.to_dict() for project in projects]}

@router.post("/")
async def create_project(project_data: ProjectCreate):
    """
    Create a new project.
    """
    project = Project(
        title=project_data.title,
        description=project_data.description,
        target_audience=project_data.target_audience,
        style=project_data.style,
        visual_style=project_data.visual_style
    )

    if project.save():
        return {"success": True, "project": project.to_dict()}
    else:
        raise HTTPException(status_code=500, detail="Failed to create project")

@router.get("/{project_id}")
async def get_project(project_id: int):
    """
    Get a project by ID.
    """
    project = Project.get_by_id(project_id)

    if project:
        # Also fetch all image assets for the project
        from backend.models.asset import Asset
        assets = Asset.get_by_project_id(project_id, asset_type="image")
        assets_dict = [a.to_dict() for a in assets]
        print(f"[get_project] Returning project with {len(assets_dict)} image assets.")
        return {"project": project.to_dict(), "assets": assets_dict}
    else:
        raise HTTPException(status_code=404, detail="Project not found")

@router.put("/{project_id}")
async def update_project(project_id: int, project_data: ProjectUpdate):
    """
    Update a project.
    """
    project = Project.get_by_id(project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Update fields if provided
    if project_data.title is not None:
        project.title = project_data.title
    if project_data.description is not None:
        project.description = project_data.description
    if project_data.target_audience is not None:
        project.target_audience = project_data.target_audience
    if project_data.total_duration is not None:
        project.total_duration = project_data.total_duration
    if project_data.status is not None:
        project.status = project_data.status
    if project_data.style is not None:
        project.style = project_data.style
    if project_data.visual_style is not None:
        project.visual_style = project_data.visual_style

    if project.save():
        return {"success": True, "project": project.to_dict()}
    else:
        raise HTTPException(status_code=500, detail="Failed to update project")

@router.delete("/{project_id}")
async def delete_project(project_id: int):
    """
    Delete a project.
    """
    project = Project.get_by_id(project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.delete():
        return {"success": True}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete project")

# Script routes
@router.get("/{project_id}/script")
async def get_project_script(project_id: int):
    """
    Get the script for a project.
    """
    project = Project.get_by_id(project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return {"script": project.content}

@router.get("/{project_id}/full_script")
async def get_project_full_script(project_id: int):
    """
    Get the full script text for a project (concatenated narrationText from all segments).
    """
    project = Project.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    script_text = project.get_full_script()
    return {"script": script_text}


@router.put("/{project_id}/script")
async def update_project_script(project_id: int, script_data: ScriptUpdate):
    """
    Update the script for a project.
    """
    print(f"Updating script for project {project_id}")
    print(f"Script data: {script_data}")

    project = Project.get_by_id(project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    print(f"Current project content: {project.content}")
    print(f"New script content: {script_data.content}")

    if project.update_content(script_data.content):
        print(f"Script updated successfully")
        return {"success": True, "script": project.content}
    else:
        print(f"Failed to update script")
        raise HTTPException(status_code=500, detail="Failed to update script")

# Asset routes
@router.get("/{project_id}/segment/{segment_id}/images")
async def get_segment_images(project_id: int, segment_id: str):
    """
    Get all image assets for a given project and segment.
    """
    import logging
    logger = logging.getLogger("ytvidgen.segment_images")
    project = Project.get_by_id(project_id)
    print(f"[get_segment_images] Called with project_id={project_id}, segment_id={segment_id}")
    if not project:
        print(f"[get_segment_images] Project not found: {project_id}")
        raise HTTPException(status_code=404, detail="Project not found")
    # Fetch all image assets for the project
    assets = Asset.get_by_project_id(project_id, asset_type="image")
    print(f"[get_segment_images] Total image assets found for project {project_id}: {len(assets)}")
    for idx, a in enumerate(assets):
        print(f"[get_segment_images] Asset[{idx}]: id={a.id}, path={a.path}, metadata={a.metadata}")
    # Filter by segment_id in metadata
    segment_assets = [a.to_dict() for a in assets if a.metadata.get("segment_id") == segment_id]
    print(f"[get_segment_images] Segment assets after filtering by segment_id={segment_id}: {len(segment_assets)}")
    if segment_assets:
        print(f"[get_segment_images] First segment asset: {segment_assets[0]}")
    else:
        print(f"[get_segment_images] No segment images found for segment_id={segment_id}. Printing all asset metadata:")
        for a in assets:
            print(f"[get_segment_images] Asset id={a.id} metadata={a.metadata}")
    return {"assets": segment_assets}

@router.get("/{project_id}/assets")
async def get_project_assets(project_id: int, asset_type: Optional[str] = None):
    """
    Get all assets for a project.
    """
    project = Project.get_by_id(project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    assets = Asset.get_by_project_id(project_id, asset_type)
    return {"assets": [asset.to_dict() for asset in assets]}

@router.post("/{project_id}/assets")
async def create_asset(
    project_id: int,
    asset_type: str = Form(...),
    metadata: str = Form("{}"),
    file: Optional[UploadFile] = File(None),
    base64_data: Optional[str] = Form(None)
):
    """
    Create a new asset for a project.
    """
    project = Project.get_by_id(project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Parse metadata
    try:
        metadata_dict = json.loads(metadata)
    except json.JSONDecodeError:
        metadata_dict = {}

    # Handle file upload or base64 data
    if file:
        # Read file data
        file_data = await file.read()

        # Save the file
        success, file_path = save_asset(file_data, project_id, asset_type,
                                       metadata_dict.get('id'), file.filename.split('.')[-1])
    elif base64_data:
        # Save base64 data
        if asset_type == 'image':
            success, file_path = save_base64_image(base64_data, project_id, metadata_dict.get('id'))
        else:
            # Decode base64 data
            try:
                if "," in base64_data:
                    base64_data = base64_data.split(",", 1)[1]
                file_data = base64.b64decode(base64_data)
                success, file_path = save_asset(file_data, project_id, asset_type, metadata_dict.get('id'))
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Invalid base64 data: {str(e)}")
    else:
        raise HTTPException(status_code=400, detail="Either file or base64_data must be provided")

    if not success:
        raise HTTPException(status_code=500, detail="Failed to save asset file")

    # Create asset record
    asset = Asset(
        project_id=project_id,
        asset_type=asset_type,
        path=file_path,
        metadata=metadata_dict
    )

    if asset.save():
        return {"success": True, "asset": asset.to_dict()}
    else:
        raise HTTPException(status_code=500, detail="Failed to create asset record")

@router.get("/assets/{asset_id}")
async def get_asset(asset_id: int, include_data: bool = False):
    """
    Get an asset by ID.
    """
    asset = Asset.get_by_id(asset_id)

    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    result = asset.to_dict()

    # Include base64 data if requested
    if include_data and asset.path:
        if asset.asset_type == 'image':
            success, base64_data = load_image_as_base64(asset.path)
            if success:
                result['data'] = f"data:image/png;base64,{base64_data}"
        # Add support for other asset types as needed

    return {"asset": result}

@router.put("/assets/{asset_id}")
async def update_asset(asset_id: int, asset_data: AssetUpdate):
    """
    Update an asset.
    """
    asset = Asset.get_by_id(asset_id)

    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    # Update fields if provided
    if asset_data.metadata is not None:
        asset.metadata = asset_data.metadata

    if asset.save():
        return {"success": True, "asset": asset.to_dict()}
    else:
        raise HTTPException(status_code=500, detail="Failed to update asset")

@router.delete("/assets/{asset_id}")
async def delete_asset(asset_id: int):
    """
    Delete an asset.
    """
    asset = Asset.get_by_id(asset_id)

    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    if asset.delete():
        return {"success": True}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete asset")


@router.post("/segments/{segment_id}/visuals")
async def create_visual(segment_id: int, visual_data: dict):
    """
    Create a new visual for a segment.
    """
    segment = Segment.get_by_id(segment_id)
    if not segment:
        raise HTTPException(status_code=404, detail="Segment not found")
    # Get the project ID for the segment
    section = Section.get_by_id(segment.section_id)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    project_id = section.project_id
    visual = Visual(
        segment_id=segment_id,
        description=visual_data.get("description"),
        timestamp=visual_data.get("timestamp"),
        duration=visual_data.get("duration"),
        alt_text=visual_data.get("alt_text"),
        visual_type=visual_data.get("visual_type"),
        visual_style=visual_data.get("visual_style"),
        position=visual_data.get("position"),
        zoom_level=visual_data.get("zoom_level"),
        transition=visual_data.get("transition")
    )
    # Set image data if provided
    if visual_data.get("image_data"):
        visual.set_image_data(visual_data["image_data"])
    if visual.save(project_id):
        return {"success": True, "visual": visual.to_dict()}
    else:
        raise HTTPException(status_code=500, detail="Failed to create visual")

@router.get("/visuals/{visual_id}")
async def get_visual(visual_id: int, include_image_data: bool = False):
    """
    Get a visual by ID.
    """
    visual = Visual.get_by_id(visual_id, include_image_data)
    if visual:
        return {"visual": visual.to_dict(include_image_data)}
    else:
        raise HTTPException(status_code=404, detail="Visual not found")

@router.put("/visuals/{visual_id}")
async def update_visual(visual_id: int, visual_data: dict):
    """
    Update a visual.
    """
    visual = Visual.get_by_id(visual_id)
    if not visual:
        raise HTTPException(status_code=404, detail="Visual not found")
    # Get the project ID for the visual
    segment = Segment.get_by_id(visual.segment_id)
    if not segment:
        raise HTTPException(status_code=404, detail="Segment not found")
    section = Section.get_by_id(segment.section_id)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    project_id = section.project_id
    # Update fields if provided
    for field in ["description", "timestamp", "duration", "alt_text", "visual_type", "visual_style", "position", "zoom_level", "transition"]:
        if visual_data.get(field) is not None:
            setattr(visual, field, visual_data[field])
    # Set image data if provided
    if visual_data.get("image_data"):
        visual.set_image_data(visual_data["image_data"])
    if visual.save(project_id):
        return {"success": True, "visual": visual.to_dict()}
    else:
        raise HTTPException(status_code=500, detail="Failed to update visual")

@router.delete("/visuals/{visual_id}")
async def delete_visual(visual_id: int):
    """
    Delete a visual.
    """
    visual = Visual.get_by_id(visual_id)
    if not visual:
        raise HTTPException(status_code=404, detail="Visual not found")
    if visual.delete():
        return {"success": True}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete visual")
