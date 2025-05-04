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
        print("---------------------------")
        print("---------------------------")
        print("---------------------------")
        print("Prompt:", prompt)
        
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
            style=request.style,
            inspiration=request.inspiration,
            visual_style=request.visual_style,
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
        print("Creating script generation prompt")
        print(request)
        inspiration_text = f"\n\n**Inspiration:** {request.inspiration}\nUse this inspiration as the main creative or thematic driver for the script. Make sure the script reflects this inspiration throughout, in both content and tone.\n" if hasattr(request, 'inspiration') and getattr(request, 'inspiration', None) else ""
        return f"""
        Create a detailed script for an educational video about \"{request.topic}\".

        Instead of addressing a general audience, write the script as if you are speaking directly to a single person, making it personal and conversational. Use 'you' and 'your' to address the viewer, and make the tone friendly and engaging.
        Target audience: {request.target_audience}
        Approximate duration: {request.duration_minutes} minutes (Meaning each section should contain about 2 minutes of content or 15 segments)
        Style: {request.style} and slightly humorous
        {inspiration_text}
        
        **Instructions:**
        1. Structure the script into logical sections (e.g., Introduction, Key Point 1, Key Point 2, Example, Conclusion).
        2. Divide each section into multiple short, focused segments. Each segment represents a few sentences of narration.
        3. **For EACH segment, generate AT LEAST THREE distinct visual suggestions.**
        4. **For EACH visual, you MUST ensure it is tightly aligned with the narration text at the visual's timestamp:**
           - If a segment has multiple visuals, break down the narration text so that each visual matches the exact part being spoken at its timestamp.
           - The visual's description MUST be contextually and temporally relevant—do NOT use generic illustrations. The visual should clearly reflect what is being narrated at that moment.
           - Optionally, for each visual, include a `text_span` or short excerpt from the narration text that is being visualized at that timestamp.
        5. For each visual, also provide:
           - Timestamp: When the visual should appear within the segment (relative to the segment's start time, in seconds).
           - Duration: How long the visual should be displayed (in seconds).
           - Visual type (image, animation, diagram, or text)
           - Position (left, right, center, full)
           - Transition (fade, slide, zoom, none)
        6. VERY IMPORTANT: Provide at least 15 segments for each section
        
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
                                    "description": "Description for image generation, directly reflecting the narration text (MINIMALISTIC VISUAL).",
                                }}
                            ]
                        }}
                    ]
                }}
            ]
        }}
        
        **Important:** Make sure the script is engaging, educational, and appropriate for the target audience. Ensure the total duration is respected, segment timings are sequential, and visual timestamps/durations fit within their parent segment. The visual descriptions are critical – make them specific and evocative. Generate AT LEAST TWO visuals per segment.
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
            
            # Set the section's total duration to 60
            for section in script_data["sections"]:
                section["total_duration"] = 60
                for segment in section["segments"]:
                    segment["start_time"] = 0
                    segment["duration"] = 10
                    for visual in segment["visuals"]:
                        visual['visual_style'] = request.visual_style
                        visual['timestamp'] = 0.0
                        visual['duration'] = 2.0
                        visual["visual_type"] = "image"
                        visual['zoom_level'] = 1.0
                        visual['position'] = 'center'
                        visual['text_span'] = ""
                        visual['transition'] = 'fade'
            
            # # If visual style is set, override all visual_style fields in visuals
            # if getattr(request, 'visual_style', None):
            #     def set_visual_style(obj):
            #         if isinstance(obj, dict):
            #             for k, v in obj.items():
            #                 if k == 'visuals' and isinstance(v, list):
            #                     for visual in v:
            #                         if isinstance(visual, dict):
            #                             visual['visual_style'] = request.visual_style
            #                             visual['timestamp'] = 0.0
            #                             visual['duration'] = 2.0
            #                             visual["visual_type"] = "image"
            #                             visual['zoom_level'] = 1.0
            #                             visual['position'] = 'center'
            #                             visual['text_span'] = ""
            #                             visual['transition'] = 'fade'
            #                 else:
            #                     set_visual_style(v)
            #         elif isinstance(obj, list):
            #             for item in obj:
            #                 set_visual_style(item)
            #     set_visual_style(script_data)
            return script_data
        except Exception as e:
            # If parsing fails, return None and print error with details and debug info
            import traceback
            print(f"Error parsing LLM response: {e}")
            print(traceback.format_exc())
            return None

    async def regenerate_section(self, section_id: str, sections: list, inspiration: str) -> dict:
        """
        Regenerate a single section using context from all sections and inspiration.
        Args:
            section_id: ID of the section to regenerate
            sections: List of all sections (dicts)
            inspiration: Inspiration text
            prompt: User's prompt
        Returns:
            The regenerated section as a dict (ScriptSection-like)
        """
        # Find the section to regenerate
        section_to_regen = next((s for s in sections if s.get("id") == section_id), None)
        if not section_to_regen:
            raise ValueError(f"Section with id {section_id} not found")
        # Prepare context for the LLM
        other_sections = [s for s in sections if s.get("id") != section_id]
        context_str = "\n\n".join([
            "\n".join([f"Segment: {seg.get('id', '')}\nNarrationText: {seg.get('narrationText', '')}" for seg in s.get("segments", [])])
            for s in other_sections
        ])
        regen_prompt = f"""
        You are an expert scriptwriter for educational videos. Your job is to regenerate a specific section of a script, ensuring it fits contextually with the rest of the script and is inspired by the following:

        Inspiration: {inspiration}

        Other Sections Context:
        {context_str}

        ---

        Regenerate the following section so it fits seamlessly with the rest of the script. Be creative, ensure the style and tone match the context and inspiration, and preserve any important structure or information:

        Section to Regenerate:
        Title: {section_to_regen.get('title', '')}
        Content: {section_to_regen.get('content', '')}

        User Prompt: {prompt}

        Return your result as a JSON object with the following structure:
        {{
            "id": "{section_id}",
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
                            "description": "Description for image generation, directly reflecting the narration text (MINIMALISTIC VISUAL).",
                            "timestamp": timestamp_in_seconds,
                            "duration": duration_in_seconds,
                            "visual_type": "image|animation|diagram|text",
                            "visual_style": "Style guidance (optional)",
                            "position": "left|right|center|full",
                            "text_span": "Text span for text visuals (optional)",
                            "transition": "fade|slide|zoom|none"
                        }}
                    ]
                }}
            ]
        }}
        """
        response = await self.llm_provider.generate_completion(
            messages=[
                {"role": "system", "content": "You are an expert scriptwriter for educational videos."},
                {"role": "user", "content": regen_prompt}
            ],
            temperature=0.7
        )
        # Parse the response as a single section
        import json as _json
        try:
            json_start = response["content"].find('{')
            json_end = response["content"].rfind('}') + 1
            section_json = response["content"][json_start:json_end]
            section_data = _json.loads(section_json)
            return section_data
        except Exception as e:
            import traceback
            print(f"Error parsing regenerated section: {e}")
            print(traceback.format_exc())
            raise

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
