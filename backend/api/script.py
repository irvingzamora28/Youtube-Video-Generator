"""
Script generation API endpoints.
"""
import os
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel # Import BaseModel
from typing import Dict, Any

from backend.llm.base import LLMProvider
from backend.llm.factory import create_llm_provider_from_env
from backend.models.script import ScriptRequest, ScriptResponse
from backend.services.script_generator import ScriptGeneratorService

# Create router
router = APIRouter(prefix="/api/script", tags=["Script"])

# Dependencies
def get_llm_provider() -> LLMProvider:
    """
    Get the LLM provider from environment variables.
    """
    try:
        return create_llm_provider_from_env()
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_script_generator(llm_provider: LLMProvider = Depends(get_llm_provider)) -> ScriptGeneratorService:
    """
    Get the script generator service.
    """
    return ScriptGeneratorService(llm_provider)

# Routes
@router.post("/generate", response_model=ScriptResponse)
async def generate_script(
    request: ScriptRequest,
    script_generator: ScriptGeneratorService = Depends(get_script_generator)
):
    """
    Generate a script based on the request.
    """
    try:
        script = await script_generator.generate_script(request)
        return ScriptResponse(script=script)
    except Exception as e:
        import traceback # Correct indentation
        print(f"Error in /generate: {e}") # Correct indentation
        print(traceback.format_exc()) # Correct indentation
        raise HTTPException(status_code=500, detail=str(e)) # Correct indentation


# --- Visual Organization Endpoint ---

class OrganizeVisualsRequest(BaseModel):
    segment: Dict[str, Any] # Pass the whole segment dictionary
    projectId: str
    sectionId: str

class OrganizeVisualsResponse(BaseModel):
    organized_segment: Dict[str, Any] # Return the segment with updated visuals

def _create_visual_organization_prompt(segment_data: Dict[str, Any]) -> str:
    """Creates the prompt for the LLM to organize visuals."""
    narration = segment_data.get('narrationText', '')
    duration = segment_data.get('duration', 0)
    visuals = segment_data.get('visuals', [])

    visuals_str = "\n".join([
        f"- ID: {v.get('id')}, Desc: {v.get('description', '')}"
        for v in visuals
    ])

    return f"""
    Analyze the following script segment narration and its associated visuals:

    Narration Text: "{narration}"
    Total Segment Duration: {duration} seconds

    Current Visuals (with IDs and Descriptions):
    {visuals_str}

    Task: Reorganize the timing of these visuals to best match the flow of the narration.
    - Adjust the 'timestamp' (start time relative to segment start) and 'duration' for each visual.
    - The timestamps must be sequential and non-overlapping within the segment.
    - The sum of all visual durations MUST equal the Total Segment Duration ({duration} seconds).
    - Do NOT change the visual 'id', 'description', 'visual_type', 'visual_style', 'position', or 'transition'. Only modify 'timestamp' and 'duration'.
    - Ensure the timing makes logical sense with the narration content.

    Return ONLY the reorganized 'visuals' array as a valid JSON list, like this:
    [
        {{
            "id": "visual-id-1",
            "description": "Existing description...",
            "timestamp": new_start_time_1,
            "duration": new_duration_1,
            "visual_type": "image", // Keep original type
            "visual_style": "...", // Keep original style
            "position": "...", // Keep original position
            "transition": "..." // Keep original transition
        }},
        {{
            "id": "visual-id-2",
            "description": "Existing description...",
            "timestamp": new_start_time_2, // Should be >= new_start_time_1 + new_duration_1
            "duration": new_duration_2,
            // ... other original properties ...
        }}
        // ... etc.
    ]
    Ensure the output is ONLY the JSON array, with no introductory text or explanations.
    """


@router.post("/organize_visuals", response_model=OrganizeVisualsResponse)
async def organize_segment_visuals(
    request: OrganizeVisualsRequest,
):
    """
    Reorganizes the timestamps and durations of visuals within a script segment to better match the narration flow.
    - Uses forced alignment to align narration text to audio (if provided).
    - Updates each visual's timestamp and duration as needed.
    - Ensures all visuals' imageUrl fields are saved with the '/static/' prefix for consistency.
    """
    segment_data = request.segment
    projectId = request.projectId
    sectionId = request.sectionId
    print(f"[organize_visuals] Received request for segment ID: {segment_data.get('id')}")

    if not segment_data or not segment_data.get('visuals'):
        raise HTTPException(status_code=400, detail="Segment data with visuals is required.")

    # Use forced alignment for each visual
    updated_segment = segment_data.copy()
    audio_url = segment_data.get('audioUrl', '')
    narration_text = segment_data.get('narrationText', '')
    word_segments = []
    if audio_url and narration_text:
        try:
            # Only run forced alignment ONCE per segment
            from backend.utils.forced_alignment import get_word_timestamps, get_reference_text_timing
            # Resolve audio_path
            if os.path.isabs(audio_url) and os.path.exists(audio_url):
                audio_path = audio_url
            else:
                backend_dir = os.path.dirname(os.path.dirname(__file__))
                # Always prepend 'static/' if not already present
                rel_audio_url = audio_url if audio_url.startswith('static/') else f'static/{audio_url}'
                audio_path = os.path.abspath(os.path.join(backend_dir, rel_audio_url))
            if not os.path.exists(audio_path):
                raise FileNotFoundError(f"Audio file not found: {audio_path}")
            word_segments = get_word_timestamps(audio_path)
        except Exception as e:
            print(f"[forced_alignment] Error in word-level forced alignment: {e}")
            word_segments = []
    # --- Ensure all visuals have '/static/' prefix on imageUrl before saving ---
    def ensure_static_prefix(image_url):
        if image_url and not image_url.startswith('/static/'):
            return '/static/' + image_url.lstrip('/')
        return image_url
    for visual in updated_segment['visuals']:
        if 'imageUrl' in visual:
            visual['imageUrl'] = ensure_static_prefix(visual.get('imageUrl', ''))
        reference_text = visual.get('referenceText', '')
        if not reference_text or not word_segments:
            continue
        try:
            # Find timing for this visual's reference_text in the precomputed word_segments
            from backend.utils.forced_alignment import get_reference_text_timing
            alignment_result = get_reference_text_timing(reference_text, word_segments)
            if alignment_result and alignment_result['found']:
                visual['timestamp'] = round(float(alignment_result['start']), 2)
                visual['duration'] = round(float(alignment_result['end']) - float(alignment_result['start']), 2)
        except Exception as e:
            print(f"[forced_alignment] Error aligning visual: {e}")
            continue
    # --- Sort visuals in chronological order by timestamp ---
    updated_segment['visuals'].sort(key=lambda v: v.get('timestamp', 0))

    # --- Adjust visuals to close gaps ---
    visuals = updated_segment['visuals']
    segment_duration = round(float(updated_segment.get('duration', 0)), 2)
    if visuals:
        visuals[0]['timestamp'] = 0.0
        for i in range(len(visuals)):
            current = visuals[i]
            if i < len(visuals) - 1:
                next_timestamp = visuals[i+1].get('timestamp', 0)
                current['duration'] = round(float(next_timestamp) - float(current['timestamp']), 2)
            else:
                # Last visual
                current['duration'] = round(segment_duration - float(current['timestamp']), 2)

    # --- Persist updated visuals in DB ---
    # Assume segment_data contains projectId, sectionId, and segment id
    project_id = projectId
    section_id = sectionId
    segment_id = segment_data.get('id')
    print(f"[DEBUG] organize_visuals: project_id={project_id}, section_id={section_id}, segment_id={segment_data.get('id')}")
    if project_id and section_id and segment_data.get('id'):
        print(f"[DEBUG] organize_visuals: project_id={project_id}, section_id={section_id}, segment_id={segment_id}")
        if project_id and section_id and segment_id:
            from backend.models.project import Project
            project = Project.get_by_id(project_id)
            print(f"[DEBUG] organize_visuals: Loaded project: {project}")
            print(f"[DEBUG] organize_visuals: project.content type: {type(project.content)}")
            if project:
                found_section = False
                found_segment = False
                for section in project.content.get('sections', []):
                    if str(section.get('id')) == str(section_id):
                        found_section = True
                        for segment in section.get('segments', []):
                            if str(segment.get('id')) == str(segment_id):
                                found_segment = True
                                segment['visuals'] = updated_segment['visuals']
                                break
                if not found_section:
                    print(f"[DEBUG] organize_visuals: Section with id {section_id} not found in project.content['sections']")
                if not found_segment:
                    print(f"[DEBUG] organize_visuals: Segment with id {segment_id} not found in section['segments']")
                save_result = project.save()
                print(f"[DEBUG] organize_visuals: project.save() result: {save_result}")

    return OrganizeVisualsResponse(organized_segment=updated_segment)


@router.post("/organize_all_visuals/{project_id}")
async def organize_all_project_visuals(
    project_id: int,
):
    """
    Organizes visuals for all segments in a project by calling organize_segment_visuals for each segment.
    """
    from backend.models.project import Project
    project = Project.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project {project_id} not found.")

    segments_organized = 0
    total_segments = 0
    for section in project.content.get('sections', []):
        section_id = section.get('id')
        for segment in section.get('segments', []):
            total_segments += 1
            visuals = segment.get('visuals', [])
            if not visuals or len(visuals) < 2:
                continue
            from .script import organize_segment_visuals, OrganizeVisualsRequest
            req = OrganizeVisualsRequest(segment=segment, projectId=str(project_id), sectionId=str(section_id))
            # Call the endpoint logic directly
            await organize_segment_visuals(req)
            segments_organized += 1
    project.save()
    return {"message": f"Visual organization complete for project {project_id}.", "segments_organized": segments_organized, "total_segments": total_segments}
