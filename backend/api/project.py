"""
Project API endpoints.
"""
from fastapi import APIRouter, HTTPException, Depends, Body
from typing import Dict, Any, Optional, List
from pydantic import BaseModel

from backend.models.project import Project
from backend.models.section import Section
from backend.models.segment import Segment
from backend.models.visual import Visual
from backend.database.db import init_db
from backend.utils.file_storage import ensure_storage_dirs

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

class SectionCreate(BaseModel):
    title: str
    content: Optional[str] = ""
    position: Optional[int] = 0
    
class SectionUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    total_duration: Optional[float] = None
    position: Optional[int] = None

class SegmentCreate(BaseModel):
    narration_text: str
    start_time: Optional[float] = 0.0
    duration: Optional[float] = 0.0
    position: Optional[int] = 0
    
class SegmentUpdate(BaseModel):
    narration_text: Optional[str] = None
    start_time: Optional[float] = None
    duration: Optional[float] = None
    position: Optional[int] = None

class VisualCreate(BaseModel):
    description: str
    timestamp: Optional[float] = 0.0
    duration: Optional[float] = 0.0
    image_data: Optional[str] = None
    alt_text: Optional[str] = ""
    visual_type: Optional[str] = "image"
    visual_style: Optional[str] = ""
    position: Optional[int] = 0
    zoom_level: Optional[float] = 1.0
    transition: Optional[str] = ""
    
class VisualUpdate(BaseModel):
    description: Optional[str] = None
    timestamp: Optional[float] = None
    duration: Optional[float] = None
    image_data: Optional[str] = None
    alt_text: Optional[str] = None
    visual_type: Optional[str] = None
    visual_style: Optional[str] = None
    position: Optional[int] = None
    zoom_level: Optional[float] = None
    transition: Optional[str] = None

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

# Section routes
@router.get("/{project_id}/sections")
async def get_project_sections(project_id: int):
    """
    Get all sections for a project.
    """
    project = Project.get_by_id(project_id)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    sections = Section.get_by_project_id(project_id)
    return {"sections": [section.to_dict() for section in sections]}

@router.post("/{project_id}/sections")
async def create_section(project_id: int, section_data: SectionCreate):
    """
    Create a new section for a project.
    """
    project = Project.get_by_id(project_id)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    section = Section(
        project_id=project_id,
        title=section_data.title,
        content=section_data.content,
        position=section_data.position
    )
    
    if section.save():
        return {"success": True, "section": section.to_dict()}
    else:
        raise HTTPException(status_code=500, detail="Failed to create section")

@router.get("/sections/{section_id}")
async def get_section(section_id: int):
    """
    Get a section by ID.
    """
    section = Section.get_by_id(section_id)
    
    if section:
        return {"section": section.to_dict()}
    else:
        raise HTTPException(status_code=404, detail="Section not found")

@router.put("/sections/{section_id}")
async def update_section(section_id: int, section_data: SectionUpdate):
    """
    Update a section.
    """
    section = Section.get_by_id(section_id)
    
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    
    # Update fields if provided
    if section_data.title is not None:
        section.title = section_data.title
    if section_data.content is not None:
        section.content = section_data.content
    if section_data.total_duration is not None:
        section.total_duration = section_data.total_duration
    if section_data.position is not None:
        section.position = section_data.position
    
    if section.save():
        return {"success": True, "section": section.to_dict()}
    else:
        raise HTTPException(status_code=500, detail="Failed to update section")

@router.delete("/sections/{section_id}")
async def delete_section(section_id: int):
    """
    Delete a section.
    """
    section = Section.get_by_id(section_id)
    
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    
    if section.delete():
        return {"success": True}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete section")

# Segment routes
@router.get("/sections/{section_id}/segments")
async def get_section_segments(section_id: int):
    """
    Get all segments for a section.
    """
    section = Section.get_by_id(section_id)
    
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    
    segments = Segment.get_by_section_id(section_id)
    return {"segments": [segment.to_dict() for segment in segments]}

@router.post("/sections/{section_id}/segments")
async def create_segment(section_id: int, segment_data: SegmentCreate):
    """
    Create a new segment for a section.
    """
    section = Section.get_by_id(section_id)
    
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    
    segment = Segment(
        section_id=section_id,
        narration_text=segment_data.narration_text,
        start_time=segment_data.start_time,
        duration=segment_data.duration,
        position=segment_data.position
    )
    
    if segment.save():
        return {"success": True, "segment": segment.to_dict()}
    else:
        raise HTTPException(status_code=500, detail="Failed to create segment")

@router.get("/segments/{segment_id}")
async def get_segment(segment_id: int):
    """
    Get a segment by ID.
    """
    segment = Segment.get_by_id(segment_id)
    
    if segment:
        return {"segment": segment.to_dict()}
    else:
        raise HTTPException(status_code=404, detail="Segment not found")

@router.put("/segments/{segment_id}")
async def update_segment(segment_id: int, segment_data: SegmentUpdate):
    """
    Update a segment.
    """
    segment = Segment.get_by_id(segment_id)
    
    if not segment:
        raise HTTPException(status_code=404, detail="Segment not found")
    
    # Update fields if provided
    if segment_data.narration_text is not None:
        segment.narration_text = segment_data.narration_text
    if segment_data.start_time is not None:
        segment.start_time = segment_data.start_time
    if segment_data.duration is not None:
        segment.duration = segment_data.duration
    if segment_data.position is not None:
        segment.position = segment_data.position
    
    if segment.save():
        return {"success": True, "segment": segment.to_dict()}
    else:
        raise HTTPException(status_code=500, detail="Failed to update segment")

@router.delete("/segments/{segment_id}")
async def delete_segment(segment_id: int):
    """
    Delete a segment.
    """
    segment = Segment.get_by_id(segment_id)
    
    if not segment:
        raise HTTPException(status_code=404, detail="Segment not found")
    
    if segment.delete():
        return {"success": True}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete segment")

# Visual routes
@router.get("/segments/{segment_id}/visuals")
async def get_segment_visuals(segment_id: int, include_image_data: bool = False):
    """
    Get all visuals for a segment.
    """
    segment = Segment.get_by_id(segment_id)
    
    if not segment:
        raise HTTPException(status_code=404, detail="Segment not found")
    
    visuals = Visual.get_by_segment_id(segment_id, include_image_data)
    return {"visuals": [visual.to_dict(include_image_data) for visual in visuals]}

@router.post("/segments/{segment_id}/visuals")
async def create_visual(segment_id: int, visual_data: VisualCreate):
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
        description=visual_data.description,
        timestamp=visual_data.timestamp,
        duration=visual_data.duration,
        alt_text=visual_data.alt_text,
        visual_type=visual_data.visual_type,
        visual_style=visual_data.visual_style,
        position=visual_data.position,
        zoom_level=visual_data.zoom_level,
        transition=visual_data.transition
    )
    
    # Set image data if provided
    if visual_data.image_data:
        visual.set_image_data(visual_data.image_data)
    
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
async def update_visual(visual_id: int, visual_data: VisualUpdate):
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
    if visual_data.description is not None:
        visual.description = visual_data.description
    if visual_data.timestamp is not None:
        visual.timestamp = visual_data.timestamp
    if visual_data.duration is not None:
        visual.duration = visual_data.duration
    if visual_data.alt_text is not None:
        visual.alt_text = visual_data.alt_text
    if visual_data.visual_type is not None:
        visual.visual_type = visual_data.visual_type
    if visual_data.visual_style is not None:
        visual.visual_style = visual_data.visual_style
    if visual_data.position is not None:
        visual.position = visual_data.position
    if visual_data.zoom_level is not None:
        visual.zoom_level = visual_data.zoom_level
    if visual_data.transition is not None:
        visual.transition = visual_data.transition
    
    # Set image data if provided
    if visual_data.image_data:
        visual.set_image_data(visual_data.image_data)
    
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
