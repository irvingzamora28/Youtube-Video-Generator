"""
YouTube Title Generation API endpoint.
"""
from fastapi import APIRouter, HTTPException, Body, Depends, Request
from pydantic import BaseModel
from typing import List
from fastapi import APIRouter, HTTPException, Body, Depends
from pydantic import BaseModel
from backend.llm.factory import create_llm_provider_from_env
from backend.llm.base import LLMProvider

router = APIRouter(prefix="/api/youtube", tags=["YouTube"])

class YoutubeTimestampsRequest(BaseModel):
    project_description: str
    script_structure: dict  # Should include sections/segments/startTimes/titles

class YoutubeTimestampsResponse(BaseModel):
    timestamps: str

def get_llm_provider() -> LLMProvider:
    try:
        return create_llm_provider_from_env()
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

from backend.models.project import extract_word_timings_from_content

@router.post("/generate_timestamps", response_model=YoutubeTimestampsResponse)
async def generate_youtube_timestamps(
    req: YoutubeTimestampsRequest = Body(...),
    llm_provider: LLMProvider = Depends(get_llm_provider)
):
    """
    Generate YouTube-style video timestamps using the LLM, given the script structure and word timings.
    """
    # Extract flat word timings from script_structure
    word_timings = extract_word_timings_from_content(req.script_structure, accum=True)
    print(f"Word timings: ", word_timings)
    # Build a compact string for LLM: "word (start)"
    word_timing_lines = "\n".join([
        f"{w['word']} ({w['start']:.2f}s)" for w in word_timings
    ])
    prompt = (
        "You are a YouTube expert. Given the following project description and a list of words with their start times, "
        "generate a clean, copy-pasteable list of timestamps for the video description. "
        "Each line should be in the format [MM:SS] [Topic or Section Title], e.g. 0:00 Introduction. "
        "Use the timing information to group words into logical topics or sections, and assign a descriptive title to each."
        "They have to be between 4 and 6 timestamps reflecting keypoints in the video"
        "Do not invent extra content, just use the information provided.\n"
        f"Project description: {req.project_description}\n"
        f"Word timings:\n{word_timing_lines}"
    )
    # print(f"Prompt: ", prompt)
    response = await llm_provider.generate_completion(
        messages=[{"role": "user", "content": prompt}],
        model=None,
        temperature=0.2,
        max_tokens=300
    )
    # Remove markdown/code block if present
    import re
    raw = response["content"].strip()
    codeblock_match = re.match(r"^```(?:[a-zA-Z]+)?\s*([\s\S]*?)\s*```$", raw)
    if codeblock_match:
        raw = codeblock_match.group(1).strip()
    return YoutubeTimestampsResponse(timestamps=raw)

@router.get("/project/{project_id}/word_timings", response_model=List[dict])
def get_word_timings(project_id: int):
    project = Project.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    content = project.content or {}
    word_timings = extract_word_timings_from_content(content)
    return word_timings

def get_llm_provider() -> LLMProvider:
    try:
        return create_llm_provider_from_env()
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

class YoutubeTitleRequest(BaseModel):
    project_description: str
    script: str

from typing import List
class YoutubeTitleResponse(BaseModel):
    titles: List[str]

@router.post("/generate_title", response_model=YoutubeTitleResponse)
async def generate_youtube_title(
    req: YoutubeTitleRequest = Body(...),
    llm_provider: LLMProvider = Depends(get_llm_provider)
):
    """
    Generate a YouTube title using the LLM provider.
    """
    try:
        prompt = (
            "You are an expert YouTube strategist. Generate 5 catchy YouTube video titles for the following project, following these rules:\n"
            "- Avoid insider language. Use simple, clear words (aim for 5th-grade reading level).\n"
            "- Use analogies or visual descriptions for any complex terms.\n"
            "- Default to common language unless the target audience is advanced.\n"
            "- Prioritize short, front-loaded titles (hook with the most intriguing/searchable phrase first).\n"
            "- Keep titles under ~50 characters or ensure the first part stands alone.\n"
            "- Understand viewer intent: pair what viewers want with what they need (the 'chocolate-covered carrot').\n"
            "- Avoid clickbait. Match the title's promise to the video.\n"
            "- Use the 'Value Equation': try to hit at least 2 of these—Dream Outcome, Likelihood of Achievement, Time Delay, Effort & Sacrifice.\n"
            "- Use high-appeal keywords: 'How to...', 'In [timeframe]', 'Guaranteed', 'Without [painful effort]', 'This Dumb/Simple Trick...'.\n"
            "- Keep titles short, punchy, and cut anything that doesn't add value or intrigue.\n"
            "Return ONLY a JSON array of 5 title strings, with no extra text, commentary, or markdown.\n"
            f"Project description: {req.project_description}\n"
            f"Project script: {req.script}"
        )
        response = await llm_provider.generate_completion(
            messages=[{"role": "user", "content": prompt}],
            model=None,
            temperature=0.7,
            max_tokens=500
        )
        import json, re
        raw = response["content"].strip()
        # Remove markdown code block wrappers if present
        codeblock_match = re.match(r"^```(?:json)?\s*([\s\S]*?)\s*```$", raw)
        if codeblock_match:
            raw = codeblock_match.group(1).strip()
        try:
            titles = json.loads(raw)
            if not isinstance(titles, list):
                raise ValueError("Response is not a list")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Could not parse LLM response as JSON array: {str(e)}. Raw response: {response['content']}")
        return YoutubeTitleResponse(titles=[str(t) for t in titles])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
