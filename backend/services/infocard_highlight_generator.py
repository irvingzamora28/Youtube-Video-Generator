from typing import List, Dict, Any

class InfocardHighlightGeneratorService:
    def __init__(self, llm_provider):
        self.llm_provider = llm_provider

    async def generate_highlights(self, script_text: str, max_highlights: int = 6, model: str = None, temperature: float = 0.7) -> List[Dict[str, Any]]:
        prompt = (
            f"""
            You are an expert at summarizing stories and creating story-driven infographics for social media. Given the following script, extract a sequence of {max_highlights} key highlights or moments that together tell the story. For each highlight, provide:
            - index (number, order in the story)
            - text (the main message for the infocard, concise and impactful)
            - visual_description (a prompt for an image generation model describing the visual/infographic for this highlight)
            - story_context (e.g., introduction, problem, solution, conclusion, etc.)

            Output as a JSON list of objects.

            SCRIPT:
            {script_text}
            """
        )
        messages = [
            {"role": "system", "content": "You are an expert at extracting social media infocards."},
            {"role": "user", "content": prompt}
        ]
        llm_response = await self.llm_provider.generate_completion(
            messages, model=model, temperature=temperature, max_tokens=1200
        )
        content = llm_response["content"]
        import json
        import re
        def extract_json_from_code_block(text: str) -> str:
            match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text, re.IGNORECASE)
            if match:
                return match.group(1)
            return text
        cleaned_content = extract_json_from_code_block(content).strip()
        try:
            highlights = json.loads(cleaned_content)
            for idx, h in enumerate(highlights):
                h["index"] = idx + 1
        except Exception as e:
            raise ValueError(f"Failed to parse highlights from LLM: {str(e)}. Raw content: {content}")
        return highlights
