"""
Social Media API endpoints.
"""
from fastapi import APIRouter, HTTPException
from fastapi import Depends, Body
from backend.api.llm import get_llm_provider
from typing import Dict, Any, Optional
from pydantic import BaseModel
from backend.models.project import Project
import json

router = APIRouter(prefix="/api/social", tags=["Social Media"])

class GenerateSocialPostsRequest(BaseModel):
    context: Optional[str] = None

@router.get("/{project_id}/social_posts")
async def get_social_posts(project_id: int):
    """
    Retrieve the saved social posts for a project.
    """
    project = Project.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if not project.social_posts:
        raise HTTPException(status_code=404, detail="No social posts found for this project")
    return {"social_posts": project.social_posts}

@router.post("/{project_id}/generate_social_posts")
async def generate_social_posts(project_id: int, req: GenerateSocialPostsRequest = None):
    """
    Generate three social post options (twitter, youtube, facebook) using the LLM and save to project.
    """
    project = Project.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Prepare context: use highlights and title
    highlights = project.infocard_highlights or []
    title = project.title or ""
    context = req.context if req and req.context else None
    # Compose prompt for LLM
    highlight_texts = [h.get("text") for h in highlights if h.get("text")]
    joined_highlights = "\n".join(highlight_texts)
    base_prompt = f"""
Given the following video project title and its main highlights, write three unique, engaging social media post options for each platform: Twitter, YouTube, and Facebook. Each post should be tailored for the platform's style and audience, and should entice viewers to watch or engage with the video. Return your response as a JSON object with keys 'twitter', 'youtube', and 'facebook'.

Title: {title}
Highlights:
{joined_highlights}
"""
    if context:
        base_prompt += f"\nAdditional context: {context}\n"
    llm_provider = get_llm_provider()
    messages = [
        {"role": "system", "content": "You are an expert social media copywriter."},
        {"role": "user", "content": base_prompt}
    ]
    llm_response = await llm_provider.generate_completion(messages, max_tokens=4000, temperature=0.7)
    content = llm_response["content"]
    import re, logging
    # Remove code block markers and leading/trailing whitespace
    # Use the same robust extraction as InfocardHighlightGeneratorService
    def extract_json_from_code_block(text: str) -> str:
        match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text, re.IGNORECASE)
        if match:
            return match.group(1)
        return text
    cleaned_content = extract_json_from_code_block(content).strip()
    try:
        posts = json.loads(cleaned_content)
    except Exception as e:
        logging.error(f"Failed to parse LLM response as JSON. Raw content: {repr(cleaned_content)}")
        raise HTTPException(status_code=500, detail=f"Failed to parse LLM response: {str(e)}. Raw: {cleaned_content[:500]}")
    project.social_posts = posts
    project.save()
    return {"social_posts": posts}
