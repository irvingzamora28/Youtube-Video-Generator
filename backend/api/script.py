"""
Script generation API endpoints.
"""
import json
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel # Import BaseModel
from typing import Dict, Any, List # Import List

from backend.llm.base import LLMProvider
from backend.llm.factory import create_llm_provider_from_env
# Import ScriptSegment and Visual models
# Import BackgroundTasks
from fastapi import BackgroundTasks
from backend.models.script import ScriptRequest, ScriptResponse, ScriptSegment, Visual
from backend.services.script_generator import ScriptGeneratorService
from backend.models.project import Project # Import Project model

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
    llm_provider: LLMProvider = Depends(get_llm_provider) # Reuse LLM provider dependency
):
    """
    Uses an LLM to reorganize the timestamps and durations of visuals within a segment
    to better match the narration flow.
    """
    segment_data = request.segment
    print(f"[organize_visuals] Received request for segment ID: {segment_data.get('id')}")

    if not segment_data or not segment_data.get('visuals'):
        raise HTTPException(status_code=400, detail="Segment data with visuals is required.")

    prompt = _create_visual_organization_prompt(segment_data)

    try:
        print("[organize_visuals] Sending request to LLM...")
        response = await llm_provider.generate_completion(
            messages=[
                {"role": "system", "content": "You are an expert video editor specializing in timing visuals to narration."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5 # Lower temperature for more deterministic timing
        )
        llm_output = response["content"]
        print(f"[organize_visuals] Received LLM output: {llm_output[:200]}...") # Log preview

        # Parse the LLM response (expecting just the JSON array)
        try:
            # Attempt to find JSON array directly
            json_start = llm_output.find('[')
            json_end = llm_output.rfind(']') + 1
            if json_start == -1 or json_end == 0:
                 raise ValueError("No JSON array found in LLM response")
            json_str = llm_output[json_start:json_end]
            organized_visuals = json.loads(json_str)

            if not isinstance(organized_visuals, list):
                 raise ValueError("LLM response is not a valid JSON list.")

            # Basic validation (more could be added)
            if len(organized_visuals) != len(segment_data.get('visuals', [])):
                 print("[WARNING] LLM returned a different number of visuals than expected.")
                 # Decide how to handle: error out, or try to use? For now, error out.
                 raise ValueError("LLM returned incorrect number of visuals.")

            # TODO: Add validation for total duration sum if needed

            # --- Merge LLM timing with original visual data ---
            original_visuals_map = {v.get('id'): v for v in segment_data.get('visuals', [])}
            merged_visuals = []
            for llm_visual in organized_visuals:
                visual_id = llm_visual.get('id')
                original_visual = original_visuals_map.get(visual_id)
                if original_visual:
                    # Keep original data, update only timestamp and duration from LLM
                    merged_visual = original_visual.copy()
                    merged_visual['timestamp'] = llm_visual.get('timestamp', original_visual.get('timestamp', 0))
                    merged_visual['duration'] = llm_visual.get('duration', original_visual.get('duration', 5))
                    merged_visuals.append(merged_visual)
                else:
                    print(f"[WARNING] LLM returned visual with ID {visual_id} not present in original segment.")
                    # Optionally skip or add the LLM visual as-is (might lack fields)
                    # merged_visuals.append(llm_visual) # Add if you want to keep potentially incomplete visuals

            if len(merged_visuals) != len(segment_data.get('visuals', [])):
                 print("[WARNING] Number of merged visuals differs from original after processing LLM response.")
                 # Fallback or error? For now, let's use the merged list if it's not empty
                 if not merged_visuals:
                      raise ValueError("Failed to merge LLM visual timing results.")


            # Update the segment data with the merged visuals list
            updated_segment = segment_data.copy()
            updated_segment['visuals'] = merged_visuals # Use the merged list
            print(f"[organize_visuals] Successfully organized visuals for segment {segment_data.get('id')}")

            return OrganizeVisualsResponse(organized_segment=updated_segment)

        except (json.JSONDecodeError, ValueError) as e:
            print(f"[ERROR] Failed to parse or validate LLM response for visual organization: {e}")
            print(f"LLM Raw Output was: {llm_output}")
            raise HTTPException(status_code=500, detail=f"Failed to process visual organization response from LLM: {e}")

    except Exception as e:
        import traceback
        print(f"Error in /organize_visuals: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error organizing visuals: {str(e)}")


# --- Bulk Visual Organization ---

async def _bulk_organize_visuals_task(project_id: int, llm_provider: LLMProvider):
    """Background task to organize visuals for all segments in a project."""
    print(f"[_bulk_organize_visuals_task] Starting bulk visual organization for project {project_id}")
    project = Project.get_by_id(project_id)
    if not project:
        print(f"[ERROR][_bulk_organize_visuals_task] Project {project_id} not found.")
        return

    segments_processed = 0
    segments_failed = 0
    project_updated = False

    # Iterate through all segments
    for section in project.content.get('sections', []):
        for i, segment in enumerate(section.get('segments', [])):
            segment_id = segment.get('id')
            visuals = segment.get('visuals', [])

            if not segment_id or not visuals or len(visuals) < 2: # Need at least 2 visuals to organize
                print(f"[_bulk_organize_visuals_task] Skipping segment {segment_id}: No visuals or less than 2 visuals.")
                continue

            print(f"[_bulk_organize_visuals_task] Processing segment {segment_id}...")
            prompt = _create_visual_organization_prompt(segment)

            try:
                response = await llm_provider.generate_completion(
                    messages=[
                        {"role": "system", "content": "You are an expert video editor specializing in timing visuals to narration."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.5
                )
                llm_output = response["content"]

                # Parse response
                json_start = llm_output.find('[')
                json_end = llm_output.rfind(']') + 1
                if json_start == -1 or json_end == 0: raise ValueError("No JSON array found")
                json_str = llm_output[json_start:json_end]
                organized_visuals = json.loads(json_str)

                if not isinstance(organized_visuals, list) or len(organized_visuals) != len(visuals):
                    raise ValueError("LLM response invalid or incorrect visual count")

                # Merge results
                original_visuals_map = {v.get('id'): v for v in visuals}
                merged_visuals = []
                for llm_visual in organized_visuals:
                    visual_id = llm_visual.get('id')
                    original_visual = original_visuals_map.get(visual_id)
                    if original_visual:
                        merged_visual = original_visual.copy()
                        merged_visual['timestamp'] = llm_visual.get('timestamp', original_visual.get('timestamp', 0))
                        merged_visual['duration'] = llm_visual.get('duration', original_visual.get('duration', 5))
                        merged_visuals.append(merged_visual)

                if len(merged_visuals) == len(visuals):
                    segment['visuals'] = merged_visuals # Update visuals in the project content dict
                    project_updated = True
                    segments_processed += 1
                    print(f"[_bulk_organize_visuals_task] Successfully organized visuals for segment {segment_id}")
                else:
                     print(f"[ERROR][_bulk_organize_visuals_task] Failed to merge visuals for segment {segment_id}")
                     segments_failed += 1

            except Exception as e:
                print(f"[ERROR][_bulk_organize_visuals_task] Failed to process segment {segment_id}: {e}")
                segments_failed += 1

            import time # Add delay between LLM calls
            time.sleep(1) # Adjust as needed

    # Save the project once if changes were made
    if project_updated:
        print(f"[_bulk_organize_visuals_task] Saving updated project {project_id} with reorganized visuals...")
        save_success = project.save()
        if save_success:
            print(f"[_bulk_organize_visuals_task] Project {project_id} saved successfully.")
        else:
            print(f"[ERROR][_bulk_organize_visuals_task] Failed to save project {project_id} after bulk visual organization.")
    else:
         print(f"[_bulk_organize_visuals_task] No segments required visual organization for project {project_id}.")

    print(f"[_bulk_organize_visuals_task] Finished bulk visual organization for project {project_id}. Processed: {segments_processed}, Failed: {segments_failed}")


@router.post("/organize_all_visuals/{project_id}")
async def organize_all_project_visuals(
    project_id: int,
    background_tasks: BackgroundTasks,
    llm_provider: LLMProvider = Depends(get_llm_provider)
):
    """
    Triggers background organization of visuals for all segments in a project.
    """
    project = Project.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project {project_id} not found.")

    print(f"[organize_all_project_visuals] Adding bulk visual organization task for project {project_id} to background.")
    background_tasks.add_task(_bulk_organize_visuals_task, project_id, llm_provider)

    return {"message": f"Visual organization for all segments of project {project_id} started in the background."}
