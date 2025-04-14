"""
Project API endpoints.
"""
from fastapi import APIRouter, HTTPException, Depends, Body, File, UploadFile, Form
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
import base64
import json
from io import BytesIO

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
    
class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    target_audience: Optional[str] = None
    total_duration: Optional[float] = None
    status: Optional[str] = None

class ScriptUpdate(BaseModel):
    content: Dict[str, Any]

class AssetCreate(BaseModel):
    asset_type: str
    metadata: Optional[Dict[str, Any]] = None
    base64_data: Optional[str] = None

class AssetUpdate(BaseModel):
    metadata: Optional[Dict[str, Any]] = None

# Project routes
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
        target_audience=project_data.target_audience
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
        return {"project": project.to_dict()}
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

@router.put("/{project_id}/script")
async def update_project_script(project_id: int, script_data: ScriptUpdate):
    """
    Update the script for a project.
    """
    project = Project.get_by_id(project_id)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project.update_content(script_data.content):
        return {"success": True, "script": project.content}
    else:
        raise HTTPException(status_code=500, detail="Failed to update script")

# Asset routes
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
