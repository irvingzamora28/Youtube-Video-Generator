"""
LLM data models.
"""
from pydantic import BaseModel, Field
from typing import List, Optional

class Message(BaseModel):
    """
    A message in a conversation.
    """
    role: str = Field(..., description="The role of the message sender (user or assistant)")
    content: str = Field(..., description="The content of the message")

class CompletionRequest(BaseModel):
    """
    A request for a completion.
    """
    messages: List[Message] = Field(..., description="The conversation history")
    model: Optional[str] = Field(None, description="The model to use for completion")
    temperature: float = Field(0.7, description="Controls randomness (0-1)")
    max_tokens: Optional[int] = Field(None, description="Maximum tokens to generate")
    stream: bool = Field(False, description="Whether to stream the response")

class CompletionResponse(BaseModel):
    """
    A response from a completion request.
    """
    content: str = Field(..., description="The generated content")
    role: str = Field("assistant", description="The role of the message sender")
    model: str = Field(..., description="The model used for completion")
