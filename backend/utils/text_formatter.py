"""
Utility functions for formatting text responses from LLMs.
"""

def format_llm_response(text: str) -> str:
    """
    Format the raw LLM response for better readability.
    
    This function cleans up and formats the raw text from LLM responses
    to ensure consistent formatting and readability.
    
    Args:
        text: The raw text from the LLM response
        
    Returns:
        Formatted text
    """
    if not text:
        return ""
    
    # Remove any leading/trailing whitespace
    formatted_text = text.strip()
    
    # Ensure consistent newlines
    formatted_text = formatted_text.replace('\r\n', '\n')
    
    return formatted_text
