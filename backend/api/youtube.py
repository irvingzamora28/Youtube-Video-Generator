"""
YouTube Title Generation API endpoint.
"""
from fastapi import APIRouter, HTTPException, Body, Depends
from pydantic import BaseModel
from backend.llm.factory import create_llm_provider_from_env
from backend.llm.base import LLMProvider

router = APIRouter(prefix="/api/youtube", tags=["YouTube"])

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
