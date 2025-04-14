"""
Script generation service.
"""
import json
import uuid
from datetime import datetime
from typing import Dict, Any, List

from ..llm.base import LLMProvider
from ..models.script import Script, ScriptSection, ScriptSegment, Visual, ScriptRequest


class ScriptGeneratorService:
    """Service for generating scripts using LLM."""

    def __init__(self, llm_provider: LLMProvider):
        self.llm_provider = llm_provider

    async def generate_script(self, request: ScriptRequest) -> Script:
        """
        Generate a complete script based on the request.
        
        Args:
            request: The script generation request
            
        Returns:
            A complete script
        """
        # Create the prompt for the LLM
        prompt = self._create_script_generation_prompt(request)
        
        # Generate the script structure using the LLM
        response = await self.llm_provider.generate_completion(
            messages=[
                {"role": "system", "content": "You are an expert scriptwriter for educational videos."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        # Parse the response into a script
        script_data = self._parse_llm_response(response["content"], request)
        
        # Create the script object
        script = Script(
            id=f"script-{uuid.uuid4()}",
            title=script_data["title"],
            description=script_data["description"],
            target_audience=request.target_audience,
            sections=self._create_sections(script_data["sections"]),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            total_duration=script_data["total_duration"],
            status="draft"
        )
        
        return script

    def _create_script_generation_prompt(self, request: ScriptRequest) -> str:
        """
        Create a prompt for generating a script.
        
        Args:
            request: The script generation request
            
        Returns:
            A prompt for the LLM
        """
        return f"""
        Create a detailed script for an educational video about "{request.topic}".
        
        Target audience: {request.target_audience}
        Approximate duration: {request.duration_minutes} minutes
        Style: {request.style}
        
        The script should be structured with sections (like Introduction, Key Concepts, etc.).
        Each section should have multiple segments, and each segment should have one or more visuals.
        
        For each visual, provide:
        - A detailed description for image generation
        - Timestamp within the segment
        - Duration
        - Visual type (image, animation, diagram, or text)
        - Position (left, right, center, full)
        - Transition (fade, slide, zoom, none)
        
        Format your response as a JSON object with the following structure:
        {{
            "title": "Title of the video",
            "description": "Brief description of the video",
            "total_duration": total_duration_in_seconds,
            "sections": [
                {{
                    "title": "Section title",
                    "content": "Overview of the section",
                    "total_duration": section_duration_in_seconds,
                    "segments": [
                        {{
                            "narration_text": "Text to be narrated",
                            "start_time": start_time_in_seconds,
                            "duration": duration_in_seconds,
                            "visuals": [
                                {{
                                    "description": "Detailed description for image generation",
                                    "timestamp": timestamp_in_seconds,
                                    "duration": duration_in_seconds,
                                    "visual_type": "image|animation|diagram|text",
                                    "visual_style": "Style guidance (optional)",
                                    "position": "left|right|center|full",
                                    "transition": "fade|slide|zoom|none"
                                }}
                            ]
                        }}
                    ]
                }}
            ]
        }}
        
        Make sure the script is engaging, educational, and appropriate for the target audience.
        The visuals should complement the narration and help explain the concepts.
        """

    def _parse_llm_response(self, response: str, request: ScriptRequest) -> Dict[str, Any]:
        """
        Parse the LLM response into a script data dictionary.
        
        Args:
            response: The LLM response
            request: The original request
            
        Returns:
            A dictionary with script data
        """
        try:
            # Extract JSON from the response (in case the LLM added extra text)
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in response")
            
            json_str = response[json_start:json_end]
            script_data = json.loads(json_str)
            
            # Validate the script data
            if "title" not in script_data:
                script_data["title"] = f"Understanding {request.topic}"
            
            if "description" not in script_data:
                script_data["description"] = f"A comprehensive explanation of {request.topic} for {request.target_audience} audiences."
            
            if "total_duration" not in script_data:
                # Estimate total duration based on request
                script_data["total_duration"] = request.duration_minutes * 60
            
            return script_data
        except Exception as e:
            # If parsing fails, create a fallback script
            return self._create_fallback_script(request)

    def _create_fallback_script(self, request: ScriptRequest) -> Dict[str, Any]:
        """
        Create a fallback script if parsing fails.
        
        Args:
            request: The original request
            
        Returns:
            A dictionary with script data
        """
        # Calculate durations
        total_duration = request.duration_minutes * 60
        section_count = 4  # Introduction, Key Concepts, Applications, Conclusion
        section_duration = total_duration / section_count
        
        return {
            "title": f"Understanding {request.topic}",
            "description": f"A comprehensive explanation of {request.topic} for {request.target_audience} audiences.",
            "total_duration": total_duration,
            "sections": [
                {
                    "title": "Introduction",
                    "content": f"An introduction to {request.topic} and why it matters.",
                    "total_duration": section_duration,
                    "segments": [
                        {
                            "narration_text": f"Welcome to this video about {request.topic}. Today we'll explore the key concepts and show you how it all works.",
                            "start_time": 0,
                            "duration": section_duration / 2,
                            "visuals": [
                                {
                                    "description": f"A stickman looking curious about {request.topic}, with a thought bubble showing the topic name.",
                                    "timestamp": 0,
                                    "duration": section_duration / 4,
                                    "visual_type": "image",
                                    "visual_style": "simple, clear, educational",
                                    "position": "center",
                                    "transition": "fade"
                                },
                                {
                                    "description": f"The stickman gesturing towards a title card that says '{request.topic}'.",
                                    "timestamp": section_duration / 4,
                                    "duration": section_duration / 4,
                                    "visual_type": "image",
                                    "visual_style": "simple, clear, educational",
                                    "position": "center",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": f"{request.topic} has become increasingly important in today's world. Let's explore why it matters.",
                            "start_time": section_duration / 2,
                            "duration": section_duration / 2,
                            "visuals": [
                                {
                                    "description": f"A stickman pointing to a world map with areas highlighting where {request.topic} is relevant.",
                                    "timestamp": 0,
                                    "duration": section_duration / 2,
                                    "visual_type": "image",
                                    "visual_style": "simple, clear, educational",
                                    "position": "full",
                                    "transition": "fade"
                                }
                            ]
                        }
                    ]
                },
                {
                    "title": f"Key Concepts of {request.topic}",
                    "content": f"The fundamental principles and concepts that make up {request.topic}.",
                    "total_duration": section_duration,
                    "segments": [
                        {
                            "narration_text": f"Let's start with the basics. At its core, {request.topic} consists of several key principles.",
                            "start_time": 0,
                            "duration": section_duration,
                            "visuals": [
                                {
                                    "description": f"A stickman teacher pointing at a blackboard with the title '{request.topic} Fundamentals'.",
                                    "timestamp": 0,
                                    "duration": section_duration,
                                    "visual_type": "image",
                                    "visual_style": "simple, clear, educational",
                                    "position": "center",
                                    "transition": "fade"
                                }
                            ]
                        }
                    ]
                },
                {
                    "title": "Practical Applications",
                    "content": f"How {request.topic} is applied in real-world scenarios.",
                    "total_duration": section_duration,
                    "segments": [
                        {
                            "narration_text": f"Now that we understand the theory, let's look at how {request.topic} is applied in practice.",
                            "start_time": 0,
                            "duration": section_duration,
                            "visuals": [
                                {
                                    "description": f"A stickman demonstrating practical applications of {request.topic} in everyday scenarios.",
                                    "timestamp": 0,
                                    "duration": section_duration,
                                    "visual_type": "image",
                                    "visual_style": "simple, clear, educational",
                                    "position": "center",
                                    "transition": "fade"
                                }
                            ]
                        }
                    ]
                },
                {
                    "title": "Conclusion",
                    "content": f"Summary of what we've learned about {request.topic} and next steps.",
                    "total_duration": section_duration,
                    "segments": [
                        {
                            "narration_text": f"To summarize, we've explored the key concepts of {request.topic} and its practical applications.",
                            "start_time": 0,
                            "duration": section_duration,
                            "visuals": [
                                {
                                    "description": f"A stickman standing next to a summary board with bullet points of the key concepts of {request.topic}.",
                                    "timestamp": 0,
                                    "duration": section_duration,
                                    "visual_type": "image",
                                    "visual_style": "simple, clear, educational",
                                    "position": "center",
                                    "transition": "fade"
                                }
                            ]
                        }
                    ]
                }
            ]
        }

    def _create_sections(self, sections_data: List[Dict[str, Any]]) -> List[ScriptSection]:
        """
        Create script sections from the parsed data.
        
        Args:
            sections_data: List of section data dictionaries
            
        Returns:
            List of ScriptSection objects
        """
        sections = []
        
        for i, section_data in enumerate(sections_data):
            # Create segments
            segments = []
            for j, segment_data in enumerate(section_data.get("segments", [])):
                # Create visuals
                visuals = []
                for k, visual_data in enumerate(segment_data.get("visuals", [])):
                    visual = Visual(
                        id=f"visual-{i+1}-{j+1}-{k+1}",
                        description=visual_data.get("description", ""),
                        timestamp=visual_data.get("timestamp", 0),
                        duration=visual_data.get("duration", 5),
                        visual_type=visual_data.get("visual_type", "image"),
                        visual_style=visual_data.get("visual_style"),
                        position=visual_data.get("position", "center"),
                        transition=visual_data.get("transition", "fade")
                    )
                    visuals.append(visual)
                
                # Create segment
                segment = ScriptSegment(
                    id=f"segment-{i+1}-{j+1}",
                    narration_text=segment_data.get("narration_text", ""),
                    start_time=segment_data.get("start_time", 0),
                    duration=segment_data.get("duration", 10),
                    visuals=visuals
                )
                segments.append(segment)
            
            # Create section
            section = ScriptSection(
                id=f"section-{i+1}",
                title=section_data.get("title", f"Section {i+1}"),
                content=section_data.get("content", ""),
                segments=segments,
                total_duration=section_data.get("total_duration", 0)
            )
            sections.append(section)
        
        return sections
