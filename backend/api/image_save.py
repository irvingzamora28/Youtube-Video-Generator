from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field # Import BaseModel and Field
from backend.models.asset import Asset
import os, uuid, base64

router = APIRouter(prefix="/api/image", tags=["Image"])

# Define Pydantic model for the request body
class SaveImagePayload(BaseModel):
    project_id: int
    segment_id: str
    visual_id: str
    timestamp: float
    duration: float
    image_data: str # base64-encoded image
    description: str = ""

@router.post("/save")
async def save_image_asset(payload: SaveImagePayload): # Accept payload model
    """
    Save a generated image as an asset and attach it to a segment with timestamp/duration metadata.
    """
    # Access data from the payload object
    print(f"[save_image_asset] Called with project_id={payload.project_id}, segment_id={payload.segment_id}, timestamp={payload.timestamp}, duration={payload.duration}, description={payload.description}")
    print(f"[save_image_asset] image_data length: {len(payload.image_data)}")
    try:
        # --- Pre-check and Delete existing asset if necessary ---
        try:
            from backend.models.project import Project # Import here to avoid circular dependency issues if any
            from backend.config.settings import settings # Import settings for static path

            project_for_check = Project.get_by_id(payload.project_id)
            if project_for_check:
                existing_visual_asset_id = None
                for section in project_for_check.content.get('sections', []):
                    for segment in section.get('segments', []):
                         if str(segment.get('id')) == str(payload.segment_id):
                              for visual in segment.get('visuals', []):
                                   if str(visual.get('id')) == str(payload.visual_id):
                                        existing_visual_asset_id = visual.get('assetId')
                                        break
                              if existing_visual_asset_id: break # Found visual
                    if existing_visual_asset_id: break # Found visual

                if existing_visual_asset_id:
                    print(f"[save_image_asset] Found existing asset ID {existing_visual_asset_id} for visual {payload.visual_id}. Attempting deletion.")
                    old_asset = Asset.get_by_id(existing_visual_asset_id)
                    if old_asset and old_asset.asset_type == 'image':
                        old_file_path = os.path.join(settings.static_dir, old_asset.path)
                        if os.path.exists(old_file_path):
                            os.remove(old_file_path)
                            print(f"[save_image_asset] Deleted old image file: {old_file_path}")
                        else:
                            print(f"[save_image_asset] Old image file not found, skipping deletion: {old_file_path}")
                        deleted_db = old_asset.delete()
                        if deleted_db:
                            print(f"[save_image_asset] Deleted old image asset record ID: {existing_visual_asset_id}")
                        else:
                            print(f"[WARNING] Failed to delete old image asset record ID: {existing_visual_asset_id}")
                    elif old_asset:
                        print(f"[WARNING] Asset ID {existing_visual_asset_id} found but is not an image asset ({old_asset.asset_type}). Skipping deletion.")
                    else:
                        print(f"[WARNING] Old asset ID {existing_visual_asset_id} not found in database.")
            else:
                 print(f"[WARNING] Project {payload.project_id} not found during pre-check for deletion.")

        except Exception as e:
             print(f"[ERROR] Failed during pre-check and deletion of old image asset: {e}")
             # Decide whether to proceed or fail? Let's proceed for now.
        # --- End Deletion ---


        # Decode base64 image
        header, _, data = payload.image_data.partition(",")
        if data:
            image_bytes = base64.b64decode(data)
        else:
            image_bytes = base64.b64decode(payload.image_data) # Use payload data
        # Save image file
        img_dir = os.path.join("static", "projects", str(payload.project_id), "segments", str(payload.segment_id)) # Use payload data
        os.makedirs(img_dir, exist_ok=True)
        filename = f"{uuid.uuid4().hex}.png"
        img_path = os.path.join(img_dir, filename)
        with open(img_path, "wb") as f:
            f.write(image_bytes)
        rel_path = os.path.relpath(img_path, start="static")
        # Store asset in DB
        metadata = {
            "segment_id": payload.segment_id, # Use payload data
            "timestamp": payload.timestamp,   # Use payload data
            "duration": payload.duration,     # Use payload data
            "description": payload.description # Use payload data
        }
        print(f"[save_image_asset] Asset metadata: {metadata}")
        asset = Asset(
            project_id=payload.project_id, # Use payload data
            asset_type="image",
            path=rel_path,
            metadata=metadata
        )
        save_result = asset.save()
        print(f"[save_image_asset] Asset.save() result: {save_result}, asset.id: {asset.id}")
        if save_result:
            # print(f"[save_image_asset] Asset saved to DB: {asset.to_dict()}")
            # Try to attach image to the correct visual in the project structure
            try:
                from backend.models.project import Project
                project = Project.get_by_id(payload.project_id) # Use payload data
                if not project:
                    print(f"[save_image_asset] Project {payload.project_id} not found when updating content.")
                else:
                    updated = False
                    content = project.content
                    print(f"[save_image_asset] Loaded project content for update.")
                    # Traverse sections/segments/visuals
                    for section in content.get('sections', []):
                        for segment in section.get('segments', []):
                            if str(segment.get('id')) == str(payload.segment_id): # Use payload data
                                visuals = segment.get('visuals', [])
                                # print(f"[save_image_asset] Checking {len(visuals)} visuals in segment {segment.get('id')}...")
                                # Attach to the visual with the given visual_id
                                match = None
                                for idx, v in enumerate(visuals):
                                    current_visual_id = v.get('id')
                                    # print(f"[save_image_asset] Visual {idx}: ID={current_visual_id} (Type: {type(current_visual_id)}), Comparing with visual_id={payload.visual_id} (Type: {type(payload.visual_id)})") # Use payload data
                                    if str(current_visual_id) == str(payload.visual_id): # Use payload data
                                        # print(f"[save_image_asset] Match found for visual_id {payload.visual_id} at index {idx}") # Use payload data
                                        match = v
                                        break # Exit inner loop once match is found
                                if match:
                                    # print(f"[save_image_asset] Visual before update: {match}")
                                    match['imageUrl'] = asset.path
                                    match['assetId'] = asset.id  # Ensure assetId is set to the asset's DB id
                                    # Update the description too
                                    match['description'] = payload.description
                                    # print(f"[save_image_asset] Visual after update: {match}")
                                    updated = True
                                    break # Exit outer loop (segments) as we found and updated the target
                                else:
                                    print(f"[save_image_asset] No visual with id {payload.visual_id} found in segment {segment.get('id')}") # Use payload data
                            
                        if updated: # Check if updated within the inner loop to break outer loop
                            break
                    if updated:
                        # print(f"[save_image_asset] Saving updated project content with attached image. Content preview: {str(project.content)[:200]}...")
                        save_success = project.save()
                        print(f"[save_image_asset] Project.save() returned: {save_success}")

                        # After saving, find the updated segment to return it
                        updated_segment_data = None
                        if save_success:
                             # Re-access content which should now be the saved version
                            current_content = project.content
                            for section in current_content.get('sections', []):
                                for segment_in_content in section.get('segments', []):
                                    if str(segment_in_content.get('id')) == str(payload.segment_id): # Use payload data
                                        updated_segment_data = segment_in_content
                                        # print(f"[save_image_asset] Found updated segment data to return: {updated_segment_data}")
                                        break
                                if updated_segment_data:
                                    break
                        else:
                             print(f"[save_image_asset] Project save failed, cannot return updated segment.")

                    else:
                        print(f"[save_image_asset] No update made to project content.")

            except Exception as e:
                print(f"[save_image_asset] Exception while updating project content: {e}")
                import traceback
                print(traceback.format_exc())
                # Still return asset info even if content update failed, but indicate segment update failure
                return {"success": True, "asset": asset.to_dict(), "updated_segment": None, "error": f"Failed to update project content: {e}"}

            # Return success, asset details, and the updated segment data
            return {"success": True, "asset": asset.to_dict(), "updated_segment": updated_segment_data}
        else:
            print(f"[save_image_asset] Failed to save asset to DB")
            raise HTTPException(status_code=500, detail="Failed to save asset")
    except Exception as e:
        print(f"[save_image_asset] Exception occurred: {e}")
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to save image asset: {e}")
