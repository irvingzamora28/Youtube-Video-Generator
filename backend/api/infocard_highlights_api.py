from fastapi import APIRouter, HTTPException, Body
from typing import List, Optional
from pydantic import BaseModel
import os
import json
from backend.models.project import Project
from backend.llm.factory import create_llm_provider_from_env
from backend.services.infocard_highlight_generator import InfocardHighlightGeneratorService

router = APIRouter(prefix="/api/infocard_highlights", tags=["InfocardHighlights"])

class InfocardHighlight(BaseModel):
    index: int
    text: str
    visual_description: str
    story_context: str = ""

class GenerateInfocardHighlightsRequest(BaseModel):
    max_highlights: int = 6

@router.post("/{project_id}/generate")
async def generate_infocard_highlights(
    project_id: int,
    request: GenerateInfocardHighlightsRequest = Body(...)
):
    """
    Generate infocard highlights for a project using the LLM provider.
    """
    project = Project.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    script_text = project.get_full_script()
    if not script_text:
        raise HTTPException(status_code=400, detail="Project script is empty")

    llm_provider = create_llm_provider_from_env()
    highlight_generator = InfocardHighlightGeneratorService(llm_provider)
    try:
        highlights = await highlight_generator.generate_highlights(
            script_text,
            max_highlights=request.max_highlights if request.max_highlights else 6
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate highlights: {str(e)}")

    project.infocard_highlights = highlights
    project.save()
    return {"success": True, "highlights": highlights}

@router.get("/{project_id}")
async def get_infocard_highlights(project_id: int):
    """
    Retrieve the current infocard highlights for a project.
    """
    project = Project.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"highlights": project.infocard_highlights or []}
