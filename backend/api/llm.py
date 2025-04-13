"""
LLM API endpoints.
"""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from typing import Dict, Any, List
import json

from backend.llm.factory import create_llm_provider_from_env
from backend.llm.base import LLMProvider
from backend.models.llm import Message, CompletionRequest, CompletionResponse

# Create router
router = APIRouter(prefix="/api/llm", tags=["LLM"])

# Dependencies
def get_llm_provider() -> LLMProvider:
    """
    Get the LLM provider from environment variables.
    """
    try:
        return create_llm_provider_from_env()
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Routes
@router.post("/completions", response_model=CompletionResponse)
async def create_completion(
    request: CompletionRequest,
    llm_provider: LLMProvider = Depends(get_llm_provider)
):
    """
    Create a completion using the LLM provider.
    """
    try:
        # Convert Pydantic models to dictionaries
        messages = [message.model_dump() for message in request.messages]

        if request.stream:
            # For streaming responses
            async def generate_stream():
                async for chunk in llm_provider.generate_completion_stream(
                    messages=messages,
                    model=request.model,
                    temperature=request.temperature,
                    max_tokens=request.max_tokens
                ):
                    # Format the chunk as a server-sent event
                    if chunk["finished"]:
                        yield f"data: [DONE]\n\n"
                    else:
                        yield f"data: {chunk['content_delta']}\n\n"

            return StreamingResponse(
                generate_stream(),
                media_type="text/event-stream"
            )
        else:
            # For non-streaming responses
            response = await llm_provider.generate_completion(
                messages=messages,
                model=request.model,
                temperature=request.temperature,
                max_tokens=request.max_tokens
            )

            return CompletionResponse(
                content=response["content"],
                role=response["role"],
                model=response["model"]
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
