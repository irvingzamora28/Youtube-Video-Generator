"""
API endpoints for audio generation and management.
"""
import os
import uuid
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field

from backend.models.project import Project
from backend.models.asset import Asset
from backend.llm.audio_factory import get_audio_provider
from backend.llm.audio_base import AIAudioProvider
from backend.config.settings import settings # Import the instantiated settings

router = APIRouter(prefix="/api/audio", tags=["Audio"])

class GenerateAudioPayload(BaseModel):
    project_id: int
    segment_id: str
    # Optional: Add voice_name, language_code if you want frontend control
    # voice_name: str | None = None
    # language_code: str = "en-US"

class GenerateAudioResponse(BaseModel):
    success: bool
    asset: dict | None = None
    updated_segment: dict | None = None
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
        # 1. Get Project and Segment
        project = Project.get_by_id(payload.project_id)
        if not project:
            raise HTTPException(status_code=404, detail=f"Project {payload.project_id} not found.")

        target_segment = None
        segment_narration = ""
        for section in project.content.get('sections', []):
            for segment in section.get('segments', []):
                if str(segment.get('id')) == str(payload.segment_id):
                    target_segment = segment
                    segment_narration = target_segment.get('narrationText', '')
                    break
            if target_segment:
                break

        if not target_segment:
            raise HTTPException(status_code=404, detail=f"Segment {payload.segment_id} not found in project {payload.project_id}.")

        if not segment_narration:
             raise HTTPException(status_code=400, detail=f"Segment {payload.segment_id} has no narration text to generate audio from.")

        print(f"[generate_segment_audio] Found segment. Narration: '{segment_narration[:50]}...'")

        # 2. Prepare file paths
        # Use a consistent structure like static/projects/{id}/segments/{segment_id}/audio/
        audio_dir = os.path.join(settings.static_dir, "projects", str(payload.project_id), "segments", str(payload.segment_id), "audio")
        os.makedirs(audio_dir, exist_ok=True)
        filename = f"{uuid.uuid4().hex}.mp3" # Google provider generates MP3
        output_path = os.path.join(audio_dir, filename)
        # Relative path for DB and URL generation
        rel_path = os.path.relpath(output_path, start=settings.static_dir)
        print(f"[generate_segment_audio] Target audio path: {output_path}")
        print(f"[generate_segment_audio] Relative path for DB: {rel_path}")

        # 3. Generate Audio using the provider
        # Add language_code, voice_name from payload if implemented
        success = audio_provider.generate_audio(
            text=segment_narration,
            output_path=output_path
            # language_code=payload.language_code, # Example
            # voice_name=payload.voice_name # Example
        )

        if not success:
            raise HTTPException(status_code=500, detail="Audio generation failed.")

        # 4. Create Asset record
        metadata = {
            "segment_id": payload.segment_id,
            "narration_text_preview": segment_narration[:100] # Store a preview
            # Add other relevant metadata like voice used, duration? (needs ffprobe/librosa)
        }
        asset = Asset(
            project_id=payload.project_id,
            asset_type="audio",
            path=rel_path.replace("\\", "/"), # Ensure forward slashes for URLs
            metadata=metadata
        )
        asset_saved = asset.save()
        if not asset_saved or asset.id is None:
             # Attempt cleanup if DB save fails?
             if os.path.exists(output_path):
                 os.remove(output_path)
             raise HTTPException(status_code=500, detail="Failed to save audio asset to database.")

        print(f"[generate_segment_audio] Audio asset saved to DB: {asset.to_dict()}")

        # 5. Update Project Content JSON
        # Find the segment again in the *current* project content and update it
        updated = False
        current_content = project.content # Re-access potentially modified content dict
        for section in current_content.get('sections', []):
            for segment in section.get('segments', []):
                if str(segment.get('id')) == str(payload.segment_id):
                    segment['audioUrl'] = asset.path # Add audioUrl field
                    segment['audioAssetId'] = asset.id # Add audioAssetId field
                    updated = True
                    target_segment = segment # Capture the updated segment data
                    print(f"[generate_segment_audio] Updated segment JSON: {target_segment}")
                    break
            if updated:
                break

        if updated:
            project_save_success = project.save()
            if not project_save_success:
                 # Rollback asset? Difficult. Log error.
                 print(f"[ERROR] Failed to save updated project content after adding audio asset {asset.id}")
                 # Return success=True but indicate content save failure? Or raise 500?
                 # For now, let's return the asset but signal the content issue
                 return GenerateAudioResponse(
                     success=True, # Asset was created
                     asset=asset.to_dict(),
                     updated_segment=target_segment, # Return segment as it *should* be
                     error="Failed to save updated project content to database."
                 )
            print("[generate_segment_audio] Project content updated successfully.")
        else:
            # Should not happen if segment was found initially
            print(f"[ERROR] Could not find segment {payload.segment_id} in project content during update phase.")
            # Asset exists but isn't linked. Return asset but signal error.
            return GenerateAudioResponse(
                success=True, # Asset was created
                asset=asset.to_dict(),
                updated_segment=None,
                error=f"Audio asset created, but failed to find segment {payload.segment_id} in project content for linking."
            )

        # 6. Return Response
        return GenerateAudioResponse(
            success=True,
            asset=asset.to_dict(),
            updated_segment=target_segment # Return the segment with new audioUrl/audioAssetId
        )

    except HTTPException as http_exc:
        # Re-raise FastAPI HTTP exceptions
        raise http_exc
    except Exception as e:
        print(f"[generate_segment_audio] Unexpected error: {str(e)}")
        import traceback
        print(traceback.format_exc())
        # Return a generic 500 error response
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
