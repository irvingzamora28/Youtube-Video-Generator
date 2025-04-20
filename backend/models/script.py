"""
Script data models.
"""
from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime


class Visual(BaseModel):
    """A visual element in a script segment."""
    id: str
    description: str = Field(..., description="Description for image generation")
    timestamp: float = Field(..., description="Specific timestamp within the segment (in seconds)")
    duration: float = Field(..., description="How long this visual should be displayed (in seconds)")
    image_url: Optional[str] = Field(None, description="URL to the generated image once created")
    alt_text: Optional[str] = Field(None, description="Accessibility description")
    visual_type: Literal["image", "animation", "diagram", "text"] = Field(..., description="Type of visual")
    visual_style: Optional[str] = Field(None, description="Style guidance for the visual")
    position: Optional[Literal["left", "right", "center", "full"]] = Field(None, description="Position on screen")
    zoom_level: Optional[float] = Field(None, description="For zoom effects")
    transition: Optional[Literal["fade", "slide", "zoom", "none"]] = Field(None, description="Transition to next visual")


class ScriptSegment(BaseModel):
    """A segment of a script section."""
    id: str
    narration_text: str = Field(..., description="Chunk of narration")
    start_time: float = Field(..., description="In seconds from the beginning of the section")
    duration: float = Field(..., description="In seconds")
    visuals: List[Visual] = Field(default_factory=list, description="Multiple visuals can be associated with a segment")


class ScriptSection(BaseModel):
    """A section of a script."""
    id: str
    title: str = Field(..., description="e.g., 'Introduction'")
    content: str = Field(..., description="Overview/summary of the section")
    segments: List[ScriptSegment] = Field(default_factory=list)
    total_duration: float = Field(..., description="Sum of all segment durations")


class ScriptRequest(BaseModel):
    """Request for generating a script."""
    topic: str = Field(..., description="The topic of the script")
    target_audience: str = Field(..., description="The target audience for the script")
    duration_minutes: float = Field(..., description="Approximate duration in minutes")
    style: str = Field(..., description="Presentation style (e.g., educational, entertaining)")
    visual_style: str = Field(..., description="Style guidance for visuals")


class Script(BaseModel):
    """A complete script for a video."""
    id: str
    title: str
    description: str
    target_audience: str
    sections: List[ScriptSection] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
    total_duration: float = Field(..., description="Total duration in seconds")
    status: Literal["draft", "complete", "in_progress"] = "draft"
    style: str = Field(..., description="Presentation style (e.g., educational, entertaining)")
    visual_style: str = Field(..., description="Style guidance for visuals")


class ScriptResponse(BaseModel):
    """Response containing a generated script."""
    script: Script
    message: str = "Script generated successfully"
