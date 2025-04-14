"""
Script generation API endpoints.
"""
from fastapi import APIRouter, HTTPException, Depends
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
        raise HTTPException(status_code=500, detail=str(e))
