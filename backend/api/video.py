"""
Video generation API endpoints.
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict
import os
import uuid
from backend.models.project import Project
from backend.api.bg_removal import remove_background_from_image

router = APIRouter(prefix="/api/video", tags=["Video"])

# In-memory task status store (for demo; replace with Redis/db for prod)
video_generation_tasks: Dict[str, Dict] = {}

class VideoGenerationRequest(BaseModel):
    project_id: int

@router.post("/generate")
def generate_video(request: VideoGenerationRequest, background_tasks: BackgroundTasks):
    """
    Start video generation for a project (asynchronous).
    """
    project_id = request.project_id
    task_id = str(uuid.uuid4())
    video_generation_tasks[task_id] = {"status": "pending"}
    background_tasks.add_task(_generate_video_task, project_id, task_id)
    return {"status": "started", "task_id": task_id}

@router.get("/status/{task_id}")
def get_video_status(task_id: str):
    task = video_generation_tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

def _generate_video_task(project_id: int, task_id: str):
    """
    Background task to generate a video for the project.
    """
    import traceback
    try:
        video_generation_tasks[task_id]["status"] = "processing"
        project = Project.get_by_id(project_id)
        if not project:
            video_generation_tasks[task_id]["status"] = "error"
            video_generation_tasks[task_id]["error"] = f"Project {project_id} not found."
            return
        # --- Video generation logic ---
        # For now: simple video - each segment's visual + narration, concatenated
        from moviepy.video.VideoClip import ImageClip
        from moviepy.audio.io.AudioFileClip import AudioFileClip
        from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip, concatenate_videoclips
        import ffmpeg
        import datetime
        import os
        
        def resize(input_file, output_file, width, height):
            (
                ffmpeg.input(input_file)
                .filter("scale", width, height)
                .output(output_file, vframes=1, update=1)
                .overwrite_output()
                .run()
            )

        script = project.content
        visuals = []
        audio_paths = []
        durations = []
        # Assume script has 'sections' and each section has 'segments'
        for section in script.get('sections', []):
            for segment in section.get('segments', []):
                # Get visual image path and audio path
                segment_visuals = segment.get('visuals', [])
                if not segment_visuals:
                    continue
                visual = segment_visuals[0]  # For now, use the first visual
                image_path = visual.get('imageUrl') or visual.get('image_url')
                if image_path:
                    if image_path.startswith('/static/'):
                        image_path = image_path.replace('/static/', 'static/')
                    elif not image_path.startswith('static/'):
                        image_path = 'static/' + image_path.lstrip('/')
                audio_path = segment.get('audioUrl') or segment.get('audio_url')
                if audio_path:
                    if audio_path.startswith('/static/'):
                        audio_path = audio_path.replace('/static/', 'static/')
                    elif not audio_path.startswith('static/'):
                        audio_path = 'static/' + audio_path.lstrip('/')
                # Always use absolute path for audio
                audio_abspath = os.path.abspath(audio_path) if audio_path else None
                duration = segment.get('duration', 5)
                if image_path and audio_path:
                    visuals.append(image_path)
                    audio_paths.append(audio_path)
                    durations.append(duration)
        if not visuals or not audio_paths:
            video_generation_tasks[task_id]["status"] = "error"
            video_generation_tasks[task_id]["error"] = "No visuals or audio found in script."
            return
        # Generate video clips (per segment)
        clips = []
        for section in script.get('sections', []):
            for segment in section.get('segments', []):
                segment_visuals = segment.get('visuals', [])
                audio_path = segment.get('audioUrl') or segment.get('audio_url')
                if audio_path:
                    if audio_path.startswith('/static/'):
                        audio_path = audio_path.replace('/static/', 'static/')
                    elif not audio_path.startswith('static/'):
                        audio_path = 'static/' + audio_path.lstrip('/')
                audio_abspath = os.path.abspath(audio_path) if audio_path else None
                segment_duration = segment.get('duration', 5)
                if not audio_abspath or not os.path.exists(audio_abspath):
                    print(f"Audio file not found: {audio_abspath}. Skipping this segment.")
                    continue
                visual_clips = []
                for visual in segment_visuals:
                    image_path = visual.get('imageUrl') or visual.get('image_url')
                    if image_path:
                        if image_path.startswith('/static/'):
                            image_path = image_path.replace('/static/', 'static/')
                        elif not image_path.startswith('static/'):
                            image_path = 'static/' + image_path.lstrip('/')
                        base, ext = os.path.splitext(image_path)
                        resized_img_path = f"{base}_resized{ext}"
                        # Check for removeBackground and background_image
                        remove_bg = visual.get('removeBackground') or visual.get('remove_background', False)
                        is_image = (visual.get('visualType') or visual.get('visual_type', 'image')) == 'image'
                        project_bg = project.background_image
                        if remove_bg and is_image and project_bg and os.path.exists(project_bg):
                            # Compose over project background
                            composited_path = f"{base}_composited{ext}"
                            # Use method from visual, fallback to 'color'
                            method = visual.get('removeBackgroundMethod') or visual.get('remove_background_method') or 'color'
                            remove_background_from_image(image_path, project_bg, composited_path, method)
                            resize(composited_path, resized_img_path, 1920, 1080)
                        else:
                            resize(image_path, resized_img_path, 1920, 1080)
                        start = visual.get('timestamp', 0)
                        duration = visual.get('duration', segment_duration)
                        img_clip = ImageClip(resized_img_path).with_start(start).with_duration(duration)
                        visual_clips.append(img_clip)

                audio_clip = AudioFileClip(audio_abspath)
                composite = CompositeVideoClip(visual_clips, size=(1920, 1080)).with_duration(segment_duration).with_audio(audio_clip)
                clips.append(composite)
        if not clips:
            video_generation_tasks[task_id]["status"] = "error"
            video_generation_tasks[task_id]["error"] = "Failed to create video clips."
            return
        final_clip = concatenate_videoclips(clips, method="compose")
        # Output path
        out_dir = "static/videos"
        os.makedirs(out_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        out_path = os.path.join(out_dir, f"project_{project_id}_{timestamp}.mp4")
        final_clip.write_videofile(out_path, fps=30, codec="libx264", audio_codec="aac")
        # Save result
        video_generation_tasks[task_id]["status"] = "completed"
        video_generation_tasks[task_id]["video_url"] = f"/static/videos/project_{project_id}_{timestamp}.mp4"
    except Exception as e:
        print(traceback.format_exc())
        video_generation_tasks[task_id]["status"] = "error"
        video_generation_tasks[task_id]["error"] = str(e)
