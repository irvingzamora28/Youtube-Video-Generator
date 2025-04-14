"""
Google Gemini LLM provider.
"""
from typing import Dict, List, Optional, Any, AsyncGenerator
from google import genai
from google.genai import types
from .base import LLMProvider
from backend.utils.text_formatter import format_llm_response


class GoogleProvider(LLMProvider):
    """Provider for Google Gemini API"""

    def __init__(self, api_key: str = None, default_model: str = "gemini-2.0-flash-001", client=None):
        """
        Initialize the Google Gemini provider.

        Args:
            api_key: API key for authentication
            default_model: Default model to use
            client: Optional pre-configured client (for testing)
        """
        self.default_model = default_model

        # Use provided client or create a new one
        if client:
            self.client = client
        else:
            # Use API key from parameters or environment variable
            if api_key:
                self.client = genai.Client(api_key=api_key)
            else:
                # If no API key is provided, use environment variables
                self.client = genai.Client()

    async def generate_completion(self,
                                 messages: List[Dict[str, str]],
                                 model: Optional[str] = None,
                                 temperature: float = 0.7,
                                 max_tokens: Optional[int] = None,
                                 **kwargs) -> Dict[str, Any]:
        """
        Generate a completion using the Google Gemini API.

        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            model: Optional model override (defaults to configured model)
            temperature: Controls randomness (0-1)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional Gemini-specific parameters

        Returns:
            Dictionary containing the response
        """
        # Convert messages to Google's new format
        contents = self._convert_messages_to_contents(messages)

        # Set up generation config
        config = types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
            **kwargs
        )

        # Get the model to use
        model_name = model or self.default_model

        # Generate content
        response = await self._generate_content_async(model_name, contents, config)

        # Extract and format the content
        raw_content = response.text
        formatted_content = format_llm_response(raw_content)

        # Return the response
        return {
            "content": formatted_content,
            "role": "assistant",
            "model": model_name,
            "raw_response": response
        }

    async def generate_completion_stream(self,
                                       messages: List[Dict[str, str]],
                                       model: Optional[str] = None,
                                       temperature: float = 0.7,
                                       max_tokens: Optional[int] = None,
                                       **kwargs) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Generate a streaming completion using the Google Gemini API.

        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            model: Optional model override (defaults to configured model)
            temperature: Controls randomness (0-1)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional Gemini-specific parameters

        Yields:
            Dictionaries containing partial responses
        """
        # Convert messages to Google's new format
        contents = self._convert_messages_to_contents(messages)

        # Set up generation config
        config = types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
            **kwargs
        )

        # Get the model to use
        model_name = model or self.default_model

        # Generate streaming content
        stream = await self._generate_content_stream_async(model_name, contents, config)

        full_content = ""

        async for chunk in stream:
            # Skip chunks without text
            if not hasattr(chunk, 'text') or chunk.text is None:
                continue

            # Extract the content delta
            content_delta = chunk.text
            full_content += content_delta

            # Format the content
            formatted_content = format_llm_response(full_content)

            yield {
                "content": formatted_content,
                "content_delta": content_delta,
                "role": "assistant",
                "model": model_name,
                "finished": False
            }

        # Final yield with the complete content
        yield {
            "content": format_llm_response(full_content),
            "content_delta": "",
            "role": "assistant",
            "model": model_name,
            "finished": True
        }

    def _convert_messages_to_contents(self, messages: List[Dict[str, str]]) -> List[types.Content]:
        """
        Convert OpenAI-style messages to Google Gemini content format.

        Args:
            messages: List of message dictionaries with 'role' and 'content' keys

        Returns:
            List of Content objects in Gemini format
        """
        contents = []

        for message in messages:
            role = message["role"]
            content = message["content"]

            if role == "system":
                # System messages are handled as system instructions in the config
                # We'll handle this separately in the generate methods
                continue
            elif role == "user":
                # User messages
                contents.append(types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=content)]
                ))
            elif role == "assistant":
                # Assistant messages
                contents.append(types.Content(
                    role="model",
                    parts=[types.Part.from_text(text=content)]
                ))
            elif role == "tool":
                # Tool messages (function responses)
                # This is a simplified implementation
                contents.append(types.Content(
                    role="tool",
                    parts=[types.Part.from_text(text=content)]
                ))

        return contents

    async def _generate_content_async(self, model_name: str, contents: List[types.Content],
                                     config: types.GenerateContentConfig) -> Any:
        """
        Generate content asynchronously using the Gemini API.

        Args:
            model_name: Name of the model to use
            contents: List of Content objects
            config: Generation configuration

        Returns:
            Response from the Gemini API
        """
        # Generate content
        # The new Gemini API might not be fully async, so we need to handle it properly
        try:
            # Try to use it as an awaitable
            response = await self.client.models.generate_content(
                model=model_name,
                contents=contents,
                config=config
            )
            return response
        except TypeError:
            # If it's not awaitable, use it directly
            response = self.client.models.generate_content(
                model=model_name,
                contents=contents,
                config=config
            )
            return response

    async def _generate_content_stream_async(self, model_name: str, contents: List[types.Content],
                                           config: types.GenerateContentConfig) -> AsyncGenerator:
        """
        Generate streaming content asynchronously using the Gemini API.

        Args:
            model_name: Name of the model to use
            contents: List of Content objects
            config: Generation configuration

        Returns:
            Streaming response from the Gemini API
        """
        # Generate streaming content
        # The new Gemini API might not be fully async, so we need to handle it properly
        try:
            # Try to use it as an awaitable
            stream = await self.client.models.generate_content(
                model=model_name,
                contents=contents,
                config=config,
                stream=True
            )
            return stream
        except TypeError:
            # If it's not awaitable, use it directly
            stream = self.client.models.generate_content(
                model=model_name,
                contents=contents,
                config=config,
                stream=True
            )
            return stream
