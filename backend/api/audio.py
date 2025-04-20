"""
API endpoints for audio generation and management.
"""
import os
import uuid
import math # For rounding duration
import subprocess # For calling ffprobe
import shutil # To check if ffprobe exists
import time # For delay
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks # Added BackgroundTasks
from pydantic import BaseModel, Field

from backend.models.project import Project
from backend.models.asset import Asset
from backend.llm.audio_factory import get_audio_provider
from backend.llm.audio_base import AIAudioProvider
from backend.config.settings import settings # Import the instantiated settings

router = APIRouter(prefix="/api/audio", tags=["Audio"])

# --- Helper Function ---

async def _generate_and_link_audio_for_segment(
    project_id: int,
    segment_id: str,
    segment_narration: str,
    audio_provider: AIAudioProvider,
    existing_audio_asset_id: int | None = None # Add param for existing asset ID
) -> tuple[dict | None, dict | None, float | None]:
    """
    Internal helper to generate audio, create asset, and prepare segment update data.
    Does NOT save the project itself.

    Returns:
        tuple[dict | None, dict | None, float | None]: (asset_dict, segment_update_data, audio_duration) or (None, None, None) on failure.
    """
    if not segment_narration:
        print(f"[_generate_and_link_audio] Skipping segment {segment_id}: No narration text.")
        return None, None, None

    # --- Delete existing asset and file if regenerating ---
    if existing_audio_asset_id:
        print(f"[_generate_and_link_audio] Regenerating audio for segment {segment_id}. Deleting old asset ID: {existing_audio_asset_id}")
        try:
            old_asset = Asset.get_by_id(existing_audio_asset_id)
            if old_asset and old_asset.asset_type == 'audio':
                old_file_path = os.path.join(settings.static_dir, old_asset.path)
                # Delete file
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)
                    print(f"[_generate_and_link_audio] Deleted old audio file: {old_file_path}")
                else:
                    print(f"[_generate_and_link_audio] Old audio file not found, skipping deletion: {old_file_path}")
                # Delete DB record
                deleted_db = old_asset.delete()
                if deleted_db:
                    print(f"[_generate_and_link_audio] Deleted old asset record ID: {existing_audio_asset_id}")
                else:
                    print(f"[WARNING] Failed to delete old asset record ID: {existing_audio_asset_id}")
            elif old_asset:
                 print(f"[WARNING] Asset ID {existing_audio_asset_id} found but is not an audio asset ({old_asset.asset_type}). Skipping deletion.")
            else:
                 print(f"[WARNING] Old asset ID {existing_audio_asset_id} not found in database.")
        except Exception as e:
            print(f"[ERROR] Failed to delete old audio asset {existing_audio_asset_id}: {e}")
            # Decide if we should proceed or fail? For now, let's proceed but log the error.
    # --- End Deletion ---


    print(f"[_generate_and_link_audio] Generating for segment {segment_id}. Narration: '{segment_narration[:50]}...'")

    # Prepare file paths
    audio_dir = os.path.join(settings.static_dir, "projects", str(project_id), "segments", str(segment_id), "audio")
    os.makedirs(audio_dir, exist_ok=True)
    filename = f"{uuid.uuid4().hex}.mp3"
    output_path = os.path.join(audio_dir, filename)
    rel_path = os.path.relpath(output_path, start=settings.static_dir).replace("\\", "/")

    # Generate Audio
    success = audio_provider.generate_audio(text=segment_narration, output_path=output_path)
    if not success:
        print(f"[ERROR] Audio generation failed for segment {segment_id}")
        return None, None, None # Indicate failure

    # Get Duration using ffprobe
    audio_duration = 0.0
    if os.path.exists(output_path) and shutil.which("ffprobe"):
        try:
            time.sleep(0.1) # Short delay
            print(f"[_generate_and_link_audio] Attempting duration read with ffprobe: {output_path}")
            command = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", output_path]
            result = subprocess.run(command, capture_output=True, text=True, check=True, timeout=10)
            ffprobe_duration_str = result.stdout.strip()
            if ffprobe_duration_str:
                audio_duration = math.ceil(float(ffprobe_duration_str) * 10) / 10
                print(f"[_generate_and_link_audio] Duration via ffprobe for {segment_id}: {audio_duration:.1f}s")
            else:
                 print(f"[WARNING] ffprobe returned empty duration for {segment_id}")
        except Exception as e:
            print(f"[WARNING] ffprobe error for {segment_id}: {e}")
    else:
        if not os.path.exists(output_path):
             print(f"[WARNING] Audio file missing before ffprobe check for {segment_id}")
        if not shutil.which("ffprobe"):
             print("[WARNING] ffprobe command not found in PATH.")
        print(f"[WARNING] Cannot determine duration for segment {segment_id}.")


    # Create Asset
    metadata = {
        "segment_id": segment_id,
        "narration_text_preview": segment_narration[:100],
        "duration_seconds": audio_duration
    }
    asset = Asset(project_id=project_id, asset_type="audio", path=rel_path, metadata=metadata)
    asset_saved = asset.save()
    if not asset_saved or asset.id is None:
        print(f"[ERROR] Failed to save audio asset to DB for segment {segment_id}")
        if os.path.exists(output_path): os.remove(output_path) # Cleanup attempt
        return None, None, None # Indicate failure

    print(f"[_generate_and_link_audio] Asset saved for {segment_id}: ID {asset.id}")

    # Prepare segment update data (don't modify original dict here)
    segment_update_data = {
        'audioUrl': asset.path,
        'audioAssetId': asset.id
    }
    if audio_duration > 0:
        segment_update_data['duration'] = audio_duration

    return asset.to_dict(), segment_update_data, audio_duration


# --- API Endpoints ---

class GenerateAudioPayload(BaseModel):
    project_id: int
    segment_id: str
    # Optional: Add voice_name, language_code if you want frontend control
    # voice_name: str | None = None
    # language_code: str = "en-US"

class GenerateAudioResponse(BaseModel):
    success: bool
    asset: dict | None = None
    updated_segment: dict | None = None # Segment data *after* update
    error: str | None = None

@router.post("/generate_segment_audio", response_model=GenerateAudioResponse)
async def generate_segment_audio(
    payload: GenerateAudioPayload,
    audio_provider: AIAudioProvider = Depends(get_audio_provider) # Dependency injection
):
    """
    Generates audio for a specific script segment's narration text.
    Saves the audio, creates an Asset record, and links it to the segment.
    """
    print(f"[generate_segment_audio] Received request for project {payload.project_id}, segment {payload.segment_id}")

    try:
        # 1. Get Project (needed for saving later)
        project = Project.get_by_id(payload.project_id)
        if not project:
            raise HTTPException(status_code=404, detail=f"Project {payload.project_id} not found.")

        # Find the specific segment's data
        target_segment_dict = None
        segment_narration = ""
        existing_audio_asset_id = None
        for section in project.content.get('sections', []):
            for segment in section.get('segments', []):
                if str(segment.get('id')) == str(payload.segment_id):
                    target_segment_dict = segment # Keep original data
                    segment_narration = target_segment_dict.get('narrationText', '')
                    existing_audio_asset_id = target_segment_dict.get('audioAssetId') # Get existing ID
                    break
            if target_segment_dict:
                break

        if not target_segment_dict:
            raise HTTPException(status_code=404, detail=f"Segment {payload.segment_id} not found in project {payload.project_id}.")

        # 2. Generate Audio and Asset using helper (pass existing ID)
        asset_dict, segment_update_data, audio_duration = await _generate_and_link_audio_for_segment(
            project_id=payload.project_id,
            segment_id=payload.segment_id,
            segment_narration=segment_narration,
            audio_provider=audio_provider,
            existing_audio_asset_id=existing_audio_asset_id # Pass the ID
        )

        if not asset_dict or not segment_update_data:
             raise HTTPException(status_code=500, detail="Failed to generate audio or save asset.")

        # 3. Update Project Content JSON
        updated = False
        final_updated_segment = None
        current_content = project.content # Use the content from the loaded project
        for section in current_content.get('sections', []):
            for i, segment in enumerate(section.get('segments', [])):
                if str(segment.get('id')) == str(payload.segment_id):
                    # Update the segment in the project content dict
                    segment.update(segment_update_data)
                    final_updated_segment = segment # Capture the segment dict *after* update
                    updated = True
                    print(f"[generate_segment_audio] Updated segment JSON in project content: {final_updated_segment}")
                    break
            if updated:
                break

        # 4. Save Updated Project
        if updated:
            project_save_success = project.save()
            if not project_save_success:
                 print(f"[ERROR] Failed to save updated project content after adding audio asset {asset_dict.get('id')}")
                 # Return success=True (asset created) but signal content save failure
                 return GenerateAudioResponse(
                     success=True,
                     asset=asset_dict,
                     updated_segment=final_updated_segment, # Return segment as it *should* be
                     error="Failed to save updated project content to database."
                 )
            print("[generate_segment_audio] Project content updated successfully.")
        else:
            # Should not happen if segment was found initially
            print(f"[ERROR] Could not find segment {payload.segment_id} in project content during update phase.")
            return GenerateAudioResponse(
                success=True, # Asset was created
                asset=asset_dict,
                updated_segment=None,
                error=f"Audio asset created, but failed to find segment {payload.segment_id} in project content for linking."
            )

        # 5. Return Response
        return GenerateAudioResponse(
            success=True,
            asset=asset_dict,
            updated_segment=final_updated_segment # Return the segment with new audioUrl/audioAssetId/duration
        )

    except HTTPException as http_exc:
        raise http_exc # Re-raise FastAPI HTTP exceptions
    except Exception as e:
        print(f"[generate_segment_audio] Unexpected error: {str(e)}")
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

# --- Bulk Generation Endpoint ---

async def _bulk_generate_audio_task(project_id: int, audio_provider: AIAudioProvider):
    """Background task to generate audio for all segments in a project."""
    print(f"[_bulk_generate_audio_task] Starting bulk audio generation for project {project_id}")
    project = Project.get_by_id(project_id)
    if not project:
        print(f"[ERROR][_bulk_generate_audio_task] Project {project_id} not found.")
        return

    segments_processed = 0
    segments_failed = 0
    project_updated = False

    # Iterate through all segments
    for section in project.content.get('sections', []):
        for i, segment in enumerate(section.get('segments', [])):
            segment_id = segment.get('id')
            segment_narration = segment.get('narrationText', '')
            existing_audio_asset_id = segment.get('audioAssetId') # Get existing ID

            if not segment_id or not segment_narration:
                print(f"[_bulk_generate_audio_task] Skipping segment at section '{section.get('title')}', index {i}: Missing ID or narration.")
                continue

            # Decide whether to skip or regenerate based on existing ID
            # For now, let's regenerate if called, deleting the old one via the helper
            # if existing_audio_asset_id:
            #      print(f"[_bulk_generate_audio_task] Skipping segment {segment_id}: Audio already exists (Asset ID: {existing_audio_asset_id}).")
            #      continue

            print(f"[_bulk_generate_audio_task] Processing segment {segment_id} (Existing Asset ID: {existing_audio_asset_id})...")
            asset_dict, segment_update_data, _ = await _generate_and_link_audio_for_segment(
                project_id=project_id,
                segment_id=segment_id,
                segment_narration=segment_narration,
                audio_provider=audio_provider,
                existing_audio_asset_id=existing_audio_asset_id # Pass existing ID for deletion
            )

            if asset_dict and segment_update_data:
                # Update the segment data *within the project.content dictionary*
                print(f"[_bulk_generate_audio_task][DEBUG] Segment BEFORE update: {segment}")
                print(f"[_bulk_generate_audio_task][DEBUG] segment_update_data: {segment_update_data}")
                segment.update(segment_update_data)
                print(f"[_bulk_generate_audio_task][DEBUG] Segment AFTER update: {segment}")
                project_updated = True
                segments_processed += 1
                print(f"[_bulk_generate_audio_task] Successfully processed segment {segment_id}")
            else:
                segments_failed += 1
                print(f"[ERROR][_bulk_generate_audio_task] Failed to process segment {segment_id}")

            time.sleep(1) # Add a small delay between segments

    # Save the project *once* after processing all segments if any updates were made
    if project_updated:
        print(f"[_bulk_generate_audio_task][DEBUG] Project content before save: {project.content}")
        print(f"[_bulk_generate_audio_task] Saving updated project {project_id} with new audio data...")
        save_success = project.save()
        if save_success:
            print(f"[_bulk_generate_audio_task] Project {project_id} saved successfully.")
        else:
            print(f"[ERROR][_bulk_generate_audio_task] Failed to save project {project_id} after bulk audio generation.")
    else:
         print(f"[_bulk_generate_audio_task] No segments required audio generation for project {project_id}.")


    print(f"[_bulk_generate_audio_task] Finished bulk audio generation for project {project_id}. Processed: {segments_processed}, Failed: {segments_failed}")


@router.post("/generate_all_project_audio/{project_id}")
async def generate_all_project_audio(
    project_id: int,
    background_tasks: BackgroundTasks,
    audio_provider: AIAudioProvider = Depends(get_audio_provider)
):
    """
    Triggers background generation of audio for all segments in a project.
    """
    # Check if project exists first
    project = Project.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project {project_id} not found.")

    print(f"[generate_all_project_audio] Adding bulk audio generation task for project {project_id} to background.")
    background_tasks.add_task(_bulk_generate_audio_task, project_id, audio_provider)

    return {"message": f"Audio generation for all segments of project {project_id} started in the background."}
