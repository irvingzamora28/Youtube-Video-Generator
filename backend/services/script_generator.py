"""
Script generation service.
"""
import json
import uuid
from datetime import datetime
from typing import Dict, Any, List

from ..llm.base import LLMProvider
from ..models.script import Script, ScriptSection, ScriptSegment, Visual, ScriptRequest


class ScriptGeneratorService:
    """Service for generating scripts using LLM."""

    def __init__(self, llm_provider: LLMProvider):
        self.llm_provider = llm_provider

    async def generate_script(self, request: ScriptRequest) -> Script:
        """
        Generate a complete script based on the request.
        
        Args:
            request: The script generation request
            
        Returns:
            A complete script
        """
        # Create the prompt for the LLM
        prompt = self._create_script_generation_prompt(request)
        print("---------------------------")
        print("---------------------------")
        print("---------------------------")
        print("Prompt:", prompt)
        
        # Generate the script structure using the LLM
        # response = await self.llm_provider.generate_completion(
        #     messages=[
        #         {"role": "system", "content": "You are an expert scriptwriter for educational videos."},
        #         {"role": "user", "content": prompt}
        #     ],
        #     temperature=0.7,
        #     max_tokens=8000
        # )
        
        # Parse the response into a script
        print("---------------------------")
        print("---------------------------")
        print("---------------------------")
        # print("Response:", response["content"])
        whatnow = """
        ```json
        {
            "title": "How YOU Can Start a Conversation (Without the Awkward!)",
            "description": "Feeling stuck before you even say 'hi'? This video is for you! We'll walk through simple, practical steps to kickstart chats naturally and confidently, minus the cringe. Personal tips included!",
            "total_duration": 300,
            "sections": [
                {
                    "title": "Introduction: The Awkward Silence Monster",
                    "content": "Acknowledging the universal fear of starting conversations and setting a relatable, friendly tone. We'll define the 'Awkward Silence Monster' we're trying to defeat.",
                    "total_duration": 75,
                    "segments": [
                        {
                            "narration_text": "Hey there! So, you wanna chat with someone new, right?",
                            "start_time": 0,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Friendly host (animated or real) waving directly at the camera.",
                                    "timestamp": 0,
                                    "duration": 2,
                                    "visual_type": "image",
                                    "position": "full",
                                    "transition": "fade",
                                    "text_span": "Hey there!"
                                },
                                {
                                    "description": "Split screen: Left side shows a person looking thoughtful, Right side shows a speech bubble with '?' inside.",
                                    "timestamp": 2,
                                    "duration": 3,
                                    "visual_type": "diagram",
                                    "position": "center",
                                    "transition": "slide",
                                    "text_span": "wanna chat with someone new, right?"
                                },
                                {
                                    "description": "Subtle sparkle animation around the speech bubble.",
                                    "timestamp": 3,
                                    "duration": 2,
                                    "visual_type": "animation",
                                    "position": "right",
                                    "transition": "none"
                                }
                            ]
                        },
                        {
                            "narration_text": "But then... that awkward silence monster creeps in. You know the one.",
                            "start_time": 5,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "A cute, slightly goofy 'monster' character representing awkward silence peeking from behind a corner.",
                                    "timestamp": 0,
                                    "duration": 2.5,
                                    "visual_type": "animation",
                                    "position": "right",
                                    "transition": "slide",
                                    "text_span": "awkward silence monster creeps in."
                                },
                                {
                                    "description": "Close-up on the monster's slightly menacing (but still funny) eyes wiggling.",
                                    "timestamp": 2.5,
                                    "duration": 1.5,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "zoom",
                                    "text_span": "You know the one."
                                },
                                {
                                    "description": "Text overlay: 'Uh oh...' in a shaky font.",
                                    "timestamp": 3,
                                    "duration": 2,
                                    "visual_type": "text",
                                    "position": "center",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "Your palms get sweaty, your mind goes blank... total freeze mode.",
                            "start_time": 10,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Animation of cartoon hands with sweat drops flying off.",
                                    "timestamp": 0,
                                    "duration": 1.5,
                                    "visual_type": "animation",
                                    "position": "left",
                                    "transition": "fade",
                                    "text_span": "palms get sweaty,"
                                },
                                {
                                    "description": "Simple line drawing of a head with tumbleweeds blowing through empty space inside.",
                                    "timestamp": 1.5,
                                    "duration": 2,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "slide",
                                    "text_span": "mind goes blank..."
                                },
                                {
                                    "description": "Image of a person literally frozen in a block of ice (cartoon style).",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "right",
                                    "transition": "fade",
                                    "text_span": "total freeze mode."
                                }
                            ]
                        },
                        {
                            "narration_text": "Trust me, I've been there. Picture this: college party...",
                            "start_time": 15,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Host points to themself with a knowing, slightly embarrassed smile.",
                                    "timestamp": 0,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "left",
                                    "transition": "none",
                                    "text_span": "Trust me,"
                                },
                                {
                                    "description": "Thought bubble appearing above the host's head.",
                                    "timestamp": 1.5,
                                    "duration": 1,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Inside the thought bubble: a stylized image of a crowded, noisy college party scene.",
                                    "timestamp": 2.5,
                                    "duration": 2.5,
                                    "visual_type": "image",
                                    "position": "center",
                                    "transition": "zoom",
                                    "text_span": "Picture this: college party..."
                                }
                            ]
                        },
                        {
                            "narration_text": "...wanted to talk to this cool person, opened my mouth...",
                            "start_time": 20,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Inside thought bubble: A stick figure (representing 'me') looking towards another 'cool' stick figure wearing sunglasses.",
                                    "timestamp": 0,
                                    "duration": 2.5,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "none",
                                    "text_span": "wanted to talk to this cool person,"
                                },
                                {
                                    "description": "Close up on the 'me' stick figure's mouth opening slightly.",
                                    "timestamp": 2.5,
                                    "duration": 1,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "zoom",
                                    "text_span": "opened my mouth..."
                                },
                                {
                                    "description": "Question marks appearing around the 'me' stick figure's head.",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "...and literally just squeaked. Like a mouse. Awkward!",
                            "start_time": 25,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Inside thought bubble: A tiny speech bubble with 'Squeak!' comes out of the 'me' figure's mouth.",
                                    "timestamp": 0,
                                    "duration": 2,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "fade",
                                    "text_span": "literally just squeaked."
                                },
                                {
                                    "description": "Image of a small, startled mouse next to the stick figure.",
                                    "timestamp": 2,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "right",
                                    "transition": "slide",
                                    "text_span": "Like a mouse."
                                },
                                {
                                    "description": "Big, bold text: 'AWKWARD!' flashing on screen.",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "text",
                                    "position": "full",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "Sound familiar? Yeah, it happens to the best of us.",
                            "start_time": 30,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Host back on screen, shrugging with a 'what can you do?' expression.",
                                    "timestamp": 0,
                                    "duration": 2,
                                    "visual_type": "image",
                                    "position": "full",
                                    "transition": "fade",
                                    "text_span": "Sound familiar?"
                                },
                                {
                                    "description": "Animation of multiple diverse cartoon faces nodding in agreement.",
                                    "timestamp": 2,
                                    "duration": 1.5,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "slide"
                                },
                                {
                                    "description": "Text overlay: 'It's Okay!' with a thumbs-up icon.",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "text",
                                    "position": "lower_third",
                                    "transition": "fade",
                                    "text_span": "happens to the best of us."
                                }
                            ]
                        },
                        {
                            "narration_text": "But the good news? It doesn't have to be this way.",
                            "start_time": 35,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Host leaning in slightly, smiling conspiratorially.",
                                    "timestamp": 0,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "full",
                                    "transition": "none",
                                    "text_span": "But the good news?"
                                },
                                {
                                    "description": "Animation of a dark cloud being blown away to reveal a shining sun.",
                                    "timestamp": 1.5,
                                    "duration": 2,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Text: 'You Got This!' appearing brightly.",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "text",
                                    "position": "center",
                                    "transition": "zoom",
                                    "text_span": "doesn't have to be this way."
                                }
                            ]
                        },
                        {
                            "narration_text": "You CAN learn to kickstart conversations smoothly.",
                            "start_time": 40,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Stylized icon of a lightbulb turning on above a person's head.",
                                    "timestamp": 0,
                                    "duration": 1.5,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "fade",
                                    "text_span": "You CAN learn"
                                },
                                {
                                    "description": "Animation of gears turning smoothly together.",
                                    "timestamp": 1.5,
                                    "duration": 2,
                                    "visual_type": "animation",
                                    "position": "right",
                                    "transition": "slide"
                                },
                                {
                                    "description": "Text: 'Smooth Start' with an arrow pointing forward.",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "text",
                                    "position": "lower_third",
                                    "transition": "fade",
                                    "text_span": "kickstart conversations smoothly."
                                }
                            ]
                        },
                        {
                            "narration_text": "Think of it like a skill, like learning to ride a bike.",
                            "start_time": 45,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Icon representing a 'skill' - perhaps a toolbox or a brain with weights.",
                                    "timestamp": 0,
                                    "duration": 2,
                                    "visual_type": "image",
                                    "position": "left",
                                    "transition": "fade",
                                    "text_span": "Think of it like a skill,"
                                },
                                {
                                    "description": "Simple animation of a person wobbling on a bike, then riding smoothly.",
                                    "timestamp": 2,
                                    "duration": 3,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "slide",
                                    "text_span": "learning to ride a bike."
                                },
                                {
                                    "description": "Text: 'Practice Makes Progress'.",
                                    "timestamp": 3,
                                    "duration": 2,
                                    "visual_type": "text",
                                    "position": "lower_third",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "Maybe wobbly at first, but you'll get the hang of it!",
                            "start_time": 50,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Close-up on the wobbling bike animation.",
                                    "timestamp": 0,
                                    "duration": 1.5,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "zoom",
                                    "text_span": "wobbly at first,"
                                },
                                {
                                    "description": "Animation transitions to the person riding confidently, smiling.",
                                    "timestamp": 1.5,
                                    "duration": 2,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "fade"
                                },
                                {
                                    "description": "A 'thumbs up' icon pops up.",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "right",
                                    "transition": "pop",
                                    "text_span": "get the hang of it!"
                                }
                            ]
                        },
                        {
                            "narration_text": "So, grab a metaphorical helmet, okay?",
                            "start_time": 55,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Host pantomimes putting on a helmet.",
                                    "timestamp": 0,
                                    "duration": 2,
                                    "visual_type": "image",
                                    "position": "full",
                                    "transition": "none",
                                    "text_span": "grab a metaphorical helmet,"
                                },
                                {
                                    "description": "Animation of a brightly colored, slightly silly helmet appearing.",
                                    "timestamp": 2,
                                    "duration": 1.5,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "pop"
                                },
                                {
                                    "description": "Text: 'Safety First (from awkwardness!)'.",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "text",
                                    "position": "lower_third",
                                    "transition": "fade",
                                    "text_span": "okay?"
                                }
                            ]
                        },
                        {
                            "narration_text": "We're gonna tackle this together.",
                            "start_time": 60,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Image of two hands clasping in a friendly 'teamwork' gesture.",
                                    "timestamp": 0,
                                    "duration": 2,
                                    "visual_type": "image",
                                    "position": "center",
                                    "transition": "fade",
                                    "text_span": "tackle this together."
                                },
                                {
                                    "description": "Host gives a determined but friendly nod.",
                                    "timestamp": 2,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "left",
                                    "transition": "slide"
                                },
                                {
                                    "description": "Text: 'Let's Go!' with an arrow pointing right.",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "text",
                                    "position": "right",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "First step: learning how to spot your opening.",
                            "start_time": 65,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Text: 'Step 1' appearing prominently.",
                                    "timestamp": 0,
                                    "duration": 1.5,
                                    "visual_type": "text",
                                    "position": "center",
                                    "transition": "zoom"
                                },
                                {
                                    "description": "Animation of an eye with lines radiating out, scanning.",
                                    "timestamp": 1.5,
                                    "duration": 2,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "fade",
                                    "text_span": "spot your opening."
                                },
                                {
                                    "description": "Stylized icon of an open door.",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "right",
                                    "transition": "slide"
                                }
                            ]
                        },
                        {
                            "narration_text": "It's all about observation... let's dive in!",
                            "start_time": 70,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Icon of a magnifying glass examining something.",
                                    "timestamp": 0,
                                    "duration": 2,
                                    "visual_type": "image",
                                    "position": "left",
                                    "transition": "fade",
                                    "text_span": "It's all about observation..."
                                },
                                {
                                    "description": "Animation of someone diving into water (stylized).",
                                    "timestamp": 2,
                                    "duration": 1.5,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "slide"
                                },
                                {
                                    "description": "Text: 'Observation Power!'",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "text",
                                    "position": "center",
                                    "transition": "fade",
                                    "text_span": "let's dive in!"
                                }
                            ]
                        }
                    ]
                },
                {
                    "title": "Key Point 1: Finding Your 'In' - Observation Power!",
                    "content": "This section focuses on practical ways to initiate a conversation by observing the shared environment, situation, or something about the other person.",
                    "total_duration": 75,
                    "segments": [
                        {
                            "narration_text": "Okay, so you're near someone you want to chat with.",
                            "start_time": 75,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Simple diagram: Your character icon on one side, another person icon on the other, space between.",
                                    "timestamp": 0,
                                    "duration": 2,
                                    "visual_type": "diagram",
                                    "position": "center",
                                    "transition": "fade",
                                    "text_span": "you're near someone"
                                },
                                {
                                    "description": "A thought bubble appears above your character icon with '...' inside.",
                                    "timestamp": 2,
                                    "duration": 1.5,
                                    "visual_type": "animation",
                                    "position": "left",
                                    "transition": "pop"
                                },
                                {
                                    "description": "Zoom in slightly on the other person's icon.",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "diagram",
                                    "position": "right",
                                    "transition": "zoom",
                                    "text_span": "want to chat with."
                                }
                            ]
                        },
                        {
                            "narration_text": "Instead of panicking, activate your observation powers!",
                            "start_time": 80,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Red 'X' over a panicked face icon.",
                                    "timestamp": 0,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "left",
                                    "transition": "fade",
                                    "text_span": "Instead of panicking,"
                                },
                                {
                                    "description": "Animation of superhero-style eye mask appearing on your character icon.",
                                    "timestamp": 1.5,
                                    "duration": 2,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "pop"
                                },
                                {
                                    "description": "Text: 'Observation Mode: ON'.",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "text",
                                    "position": "lower_third",
                                    "transition": "fade",
                                    "text_span": "activate your observation powers!"
                                }
                            ]
                        },
                        {
                            "narration_text": "Look around. What's happening? Shared environment is key.",
                            "start_time": 85,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Animation: Character icon's eyes scanning left and right.",
                                    "timestamp": 0,
                                    "duration": 2,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "none",
                                    "text_span": "Look around."
                                },
                                {
                                    "description": "Icons representing common environments: coffee shop, park, conference room.",
                                    "timestamp": 2,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "center",
                                    "transition": "slide"
                                },
                                {
                                    "description": "A key icon unlocking a door icon labeled 'Conversation'.",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "diagram",
                                    "position": "right",
                                    "transition": "fade",
                                    "text_span": "Shared environment is key."
                                }
                            ]
                        },
                        {
                            "narration_text": "At a coffee shop? Comment on the long line.",
                            "start_time": 90,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Icon of a coffee cup.",
                                    "timestamp": 0,
                                    "duration": 1,
                                    "visual_type": "image",
                                    "position": "left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Animation of a long, winding queue of stick figures.",
                                    "timestamp": 1,
                                    "duration": 2.5,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "slide",
                                    "text_span": "Comment on the long line."
                                },
                                {
                                    "description": "Speech bubble: 'Wow, popular place today!'",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "text",
                                    "position": "right",
                                    "transition": "pop"
                                }
                            ]
                        },
                        {
                            "narration_text": "Or maybe the cool latte art the barista just made.",
                            "start_time": 95,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Image of intricate latte art (a heart or swan).",
                                    "timestamp": 0,
                                    "duration": 2,
                                    "visual_type": "image",
                                    "position": "center",
                                    "transition": "fade",
                                    "text_span": "cool latte art"
                                },
                                {
                                    "description": "Smiling barista icon giving a thumbs up.",
                                    "timestamp": 2,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "right",
                                    "transition": "slide"
                                },
                                {
                                    "description": "Speech bubble: 'Did you see that amazing foam swan?'",
                                    "timestamp": 3,
                                    "duration": 2,
                                    "visual_type": "text",
                                    "position": "left",
                                    "transition": "pop"
                                }
                            ]
                        },
                        {
                            "narration_text": "At an event? Mention the speaker, the food, the music.",
                            "start_time": 100,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Icon of a person speaking at a podium.",
                                    "timestamp": 0,
                                    "duration": 1,
                                    "visual_type": "image",
                                    "position": "left",
                                    "transition": "fade",
                                    "text_span": "the speaker,"
                                },
                                {
                                    "description": "Icon of a plate with food.",
                                    "timestamp": 1,
                                    "duration": 1,
                                    "visual_type": "image",
                                    "position": "center",
                                    "transition": "fade",
                                    "text_span": "the food,"
                                },
                                {
                                    "description": "Icon of musical notes.",
                                    "timestamp": 2,
                                    "duration": 1,
                                    "visual_type": "image",
                                    "position": "right",
                                    "transition": "fade",
                                    "text_span": "the music."
                                },
                                {
                                    "description": "Speech bubble: 'What did you think of that last talk?'",
                                    "timestamp": 3,
                                    "duration": 2,
                                    "visual_type": "text",
                                    "position": "lower_third",
                                    "transition": "pop"
                                }
                            ]
                        },
                        {
                            "narration_text": "Example: I once started a chat over weird conference carpet.",
                            "start_time": 105,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Host leans in again, sharing a mini-story.",
                                    "timestamp": 0,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "full",
                                    "transition": "none",
                                    "text_span": "Example: I once..."
                                },
                                {
                                    "description": "Image of a particularly loud, patterned, maybe ugly carpet design.",
                                    "timestamp": 1.5,
                                    "duration": 2,
                                    "visual_type": "image",
                                    "position": "center",
                                    "transition": "fade",
                                    "text_span": "weird conference carpet."
                                },
                                {
                                    "description": "Speech bubble: 'This carpet pattern is... something, huh?'",
                                    "timestamp": 3,
                                    "duration": 2,
                                    "visual_type": "text",
                                    "position": "lower_third",
                                    "transition": "pop"
                                }
                            ]
                        },
                        {
                            "narration_text": "Sounds silly, but it worked! We both laughed.",
                            "start_time": 110,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Icon of a lightbulb with 'Silly Idea!' text.",
                                    "timestamp": 0,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "left",
                                    "transition": "fade",
                                    "text_span": "Sounds silly,"
                                },
                                {
                                    "description": "Green checkmark icon.",
                                    "timestamp": 1.5,
                                    "duration": 1,
                                    "visual_type": "image",
                                    "position": "center",
                                    "transition": "pop",
                                    "text_span": "but it worked!"
                                },
                                {
                                    "description": "Animation of two stick figures laughing together.",
                                    "timestamp": 2.5,
                                    "duration": 2.5,
                                    "visual_type": "animation",
                                    "position": "right",
                                    "transition": "slide",
                                    "text_span": "We both laughed."
                                }
                            ]
                        },
                        {
                            "narration_text": "It's about finding common ground, however small.",
                            "start_time": 115,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Diagram: Two separate circles slightly overlapping.",
                                    "timestamp": 0,
                                    "duration": 2,
                                    "visual_type": "diagram",
                                    "position": "center",
                                    "transition": "fade",
                                    "text_span": "finding common ground,"
                                },
                                {
                                    "description": "Magnifying glass zooming into the small overlapping area.",
                                    "timestamp": 2,
                                    "duration": 1.5,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "zoom"
                                },
                                {
                                    "description": "Text: 'Shared Experience'.",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "text",
                                    "position": "lower_third",
                                    "transition": "fade",
                                    "text_span": "however small."
                                }
                            ]
                        },
                        {
                            "narration_text": "You can also observe something about the person.",
                            "start_time": 120,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Arrow pointing from 'Your Icon' towards 'Other Person Icon'.",
                                    "timestamp": 0,
                                    "duration": 2,
                                    "visual_type": "diagram",
                                    "position": "center",
                                    "transition": "slide"
                                },
                                {
                                    "description": "Magnifying glass icon hovering over the 'Other Person Icon'.",
                                    "timestamp": 2,
                                    "duration": 1.5,
                                    "visual_type": "animation",
                                    "position": "right",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Text: 'Notice Details'.",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "text",
                                    "position": "lower_third",
                                    "transition": "fade",
                                    "text_span": "observe something about the person."
                                }
                            ]
                        },
                        {
                            "narration_text": "Like a cool band t-shirt they're wearing.",
                            "start_time": 125,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Image of a stylish t-shirt with a fictional band logo.",
                                    "timestamp": 0,
                                    "duration": 2.5,
                                    "visual_type": "image",
                                    "position": "center",
                                    "transition": "fade",
                                    "text_span": "cool band t-shirt"
                                },
                                {
                                    "description": "Music note icons floating around the t-shirt.",
                                    "timestamp": 2,
                                    "duration": 2,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Speech bubble: 'Hey, awesome shirt! I love that band.'",
                                    "timestamp": 3,
                                    "duration": 2,
                                    "visual_type": "text",
                                    "position": "lower_third",
                                    "transition": "pop"
                                }
                            ]
                        },
                        {
                            "narration_text": "Or a book they're reading - 'Oh, how is that one?'",
                            "start_time": 130,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Image of a person reading a book with a generic cover.",
                                    "timestamp": 0,
                                    "duration": 2,
                                    "visual_type": "image",
                                    "position": "center",
                                    "transition": "fade",
                                    "text_span": "a book they're reading"
                                },
                                {
                                    "description": "Question mark icon appearing next to the book.",
                                    "timestamp": 2,
                                    "duration": 1,
                                    "visual_type": "image",
                                    "position": "right",
                                    "transition": "pop"
                                },
                                {
                                    "description": "Speech bubble: 'Oh, how is that one? I've heard about it.'",
                                    "timestamp": 3,
                                    "duration": 2,
                                    "visual_type": "text",
                                    "position": "lower_third",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "Keep it light, casual, and *not* overly personal yet.",
                            "start_time": 135,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Icon of a feather floating down gently.",
                                    "timestamp": 0,
                                    "duration": 1.5,
                                    "visual_type": "animation",
                                    "position": "left",
                                    "transition": "fade",
                                    "text_span": "Keep it light, casual,"
                                },
                                {
                                    "description": "A 'Stop' sign icon with 'Too Personal!' text.",
                                    "timestamp": 1.5,
                                    "duration": 2,
                                    "visual_type": "image",
                                    "position": "center",
                                    "transition": "slide"
                                },
                                {
                                    "description": "Text: 'Easy Does It'.",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "text",
                                    "position": "lower_third",
                                    "transition": "fade",
                                    "text_span": "not overly personal yet."
                                }
                            ]
                        },
                        {
                            "narration_text": "The goal is just to open the door for a chat.",
                            "start_time": 140,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Animation of a door creaking open slightly.",
                                    "timestamp": 0,
                                    "duration": 2.5,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "fade",
                                    "text_span": "open the door for a chat."
                                },
                                {
                                    "description": "A friendly handshake icon.",
                                    "timestamp": 2.5,
                                    "duration": 1,
                                    "visual_type": "image",
                                    "position": "right",
                                    "transition": "pop"
                                },
                                {
                                    "description": "Text: 'Just Begin'.",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "text",
                                    "position": "lower_third",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "Next up: How to keep it going beyond 'hello'.",
                            "start_time": 145,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Text: 'Step 2' appearing.",
                                    "timestamp": 0,
                                    "duration": 1.5,
                                    "visual_type": "text",
                                    "position": "left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Animation of a conversation bubble expanding.",
                                    "timestamp": 1.5,
                                    "duration": 2,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "zoom",
                                    "text_span": "keep it going"
                                },
                                {
                                    "description": "Arrow pointing forward labeled 'Flow'.",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "diagram",
                                    "position": "right",
                                    "transition": "slide",
                                    "text_span": "beyond 'hello'."
                                }
                            ]
                        }
                    ]
                },
                {
                    "title": "Key Point 2: The Art of the Open-Ended Question",
                    "content": "Explaining the difference between closed and open-ended questions and why the latter are crucial for keeping conversations alive and engaging.",
                    "total_duration": 75,
                    "segments": [
                        {
                            "narration_text": "Alright, you've said hi! Observation successful.",
                            "start_time": 150,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Checkmark next to the 'Observation Power' icon.",
                                    "timestamp": 0,
                                    "duration": 2,
                                    "visual_type": "image",
                                    "position": "left",
                                    "transition": "fade",
                                    "text_span": "Observation successful."
                                },
                                {
                                "description": "Two stick figures now have a small speech bubble connection.",
                                    "timestamp": 2,
                                    "duration": 1.5,
                                    "visual_type": "diagram",
                                    "position": "center",
                                    "transition": "slide"
                                },
                                {
                                    "description": "Text: 'Level Unlocked!'",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "text",
                                    "position": "right",
                                    "transition": "pop"
                                }
                            ]
                        },
                        {
                            "narration_text": "Now, how do you avoid the dreaded one-word answer?",
                            "start_time": 155,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Animation of a speech bubble appearing with just 'Yes.' or 'No.' inside, then deflating sadly.",
                                    "timestamp": 0,
                                    "duration": 2.5,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "fade",
                                    "text_span": "dreaded one-word answer?"
                                },
                                {
                                    "description": "Image of a tumbleweed rolling across the screen.",
                                    "timestamp": 2.5,
                                    "duration": 1.5,
                                    "visual_type": "animation",
                                    "position": "full",
                                    "transition": "slide"
                                },
                                {
                                    "description": "Awkward silence monster peeking again.",
                                    "timestamp": 3,
                                    "duration": 2,
                                    "visual_type": "animation",
                                    "position": "right",
                                    "transition": "pop"
                                }
                            ]
                        },
                        {
                            "narration_text": "Meet your secret weapon: the open-ended question!",
                            "start_time": 160,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "A stylized 'secret weapon' icon - maybe a sparkling key or a magic wand.",
                                    "timestamp": 0,
                                    "duration": 2,
                                    "visual_type": "image",
                                    "position": "center",
                                    "transition": "pop",
                                    "text_span": "your secret weapon:"
                                },
                                {
                                    "description": "Text appearing: 'Open-Ended Questions'.",
                                    "timestamp": 2,
                                    "duration": 1.5,
                                    "visual_type": "text",
                                    "position": "center",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Animation of a question mark expanding outwards.",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "animation",
                                    "position": "right",
                                    "transition": "zoom"
                                }
                            ]
                        },
                        {
                            "narration_text": "Closed questions get 'yes' or 'no'. Like 'Did you like the talk?'",
                            "start_time": 165,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Diagram: Question Mark -> Arrow -> 'Yes/No'.",
                                    "timestamp": 0,
                                    "duration": 2,
                                    "visual_type": "diagram",
                                    "position": "center",
                                    "transition": "fade",
                                    "text_span": "Closed questions get 'yes' or 'no'."
                                },
                                {
                                    "description": "Speech bubble: 'Did you like the talk?'",
                                    "timestamp": 2,
                                    "duration": 1.5,
                                    "visual_type": "text",
                                    "position": "left",
                                    "transition": "pop"
                                },
                                {
                                    "description": "Response bubble: 'Yes.'",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "text",
                                    "position": "right",
                                    "transition": "pop"
                                }
                            ]
                        },
                        {
                            "narration_text": "Conversation... dead end. Womp womp.",
                            "start_time": 170,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Animation of the speech bubble connection breaking.",
                                    "timestamp": 0,
                                    "duration": 2,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "fade",
                                    "text_span": "Conversation... dead end."
                                },
                                {
                                    "description": "Image of a road sign showing a dead end.",
                                    "timestamp": 2,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "center",
                                    "transition": "slide"
                                },
                                {
                                    "description": "Sad trombone sound effect icon (optional). Text: 'Womp womp'.",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "text",
                                    "position": "right",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "Open questions invite *more* detail. They start with 'What', 'How', 'Why'.",
                            "start_time": 175,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Diagram: Question Mark -> Arrow -> Long, winding line (representing detail).",
                                    "timestamp": 0,
                                    "duration": 2,
                                    "visual_type": "diagram",
                                    "position": "center",
                                    "transition": "fade",
                                    "text_span": "invite *more* detail."
                                },
                                {
                                    "description": "Text: 'What?'",
                                    "timestamp": 2,
                                    "duration": 1,
                                    "visual_type": "text",
                                    "position": "left",
                                    "transition": "pop"
                                },
                                {
                                    "description": "Text: 'How?'",
                                    "timestamp": 3,
                                    "duration": 1,
                                    "visual_type": "text",
                                    "position": "center",
                                    "transition": "pop"
                                },
                                {
                                    "description": "Text: 'Why?'",
                                    "timestamp": 4,
                                    "duration": 1,
                                    "visual_type": "text",
                                    "position": "right",
                                    "transition": "pop"
                                }
                            ]
                        },
                        {
                            "narration_text": "Instead: 'What did you find most interesting about the talk?'",
                            "start_time": 180,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Speech bubble: 'What did you find most interesting about the talk?'",
                                    "timestamp": 0,
                                    "duration": 3,
                                    "visual_type": "text",
                                    "position": "center",
                                    "transition": "fade"
                                },
                                {
                                    "description": "An 'Aha!' or lightbulb icon next to the bubble.",
                                    "timestamp": 3,
                                    "duration": 1,
                                    "visual_type": "image",
                                    "position": "right",
                                    "transition": "pop"
                                },
                                {
                                    "description": "Response bubble starts forming, much larger than before.",
                                    "timestamp": 4,
                                    "duration": 1,
                                    "visual_type": "animation",
                                    "position": "right",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "See? That requires more than just 'yes'.",
                            "start_time": 185,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Host points knowingly at the screen.",
                                    "timestamp": 0,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "left",
                                    "transition": "none",
                                    "text_span": "See?"
                                },
                                {
                                    "description": "Visual comparison: Small 'Yes' bubble vs. Large bubble with '...' indicating more text.",
                                    "timestamp": 1.5,
                                    "duration": 2,
                                    "visual_type": "diagram",
                                    "position": "center",
                                    "transition": "slide"
                                },
                                {
                                    "description": "Text: 'Invites Detail!'",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "text",
                                    "position": "lower_third",
                                    "transition": "fade",
                                    "text_span": "requires more than just 'yes'."
                                }
                            ]
                        },
                        {
                            "narration_text": "Or, 'How did you get into [their hobby/interest you observed]?'",
                            "start_time": 190,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Speech bubble: 'How did you get into...?'",
                                    "timestamp": 0,
                                    "duration": 2,
                                    "visual_type": "text",
                                    "position": "left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Icons representing hobbies: camera, guitar, book.",
                                    "timestamp": 2,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "center",
                                    "transition": "slide",
                                    "text_span": "[their hobby/interest you observed]?"
                                },
                                {
                                    "description": "A curious face emoji.",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "right",
                                    "transition": "pop"
                                }
                            ]
                        },
                        {
                            "narration_text": "It shows you're genuinely interested, not just making noise.",
                            "start_time": 195,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Icon of an ear leaning in to listen.",
                                    "timestamp": 0,
                                    "duration": 2,
                                    "visual_type": "image",
                                    "position": "left",
                                    "transition": "fade",
                                    "text_span": "genuinely interested,"
                                },
                                {
                                    "description": "Crossed out icon of random 'blah blah blah' speech.",
                                    "timestamp": 2,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "center",
                                    "transition": "slide",
                                    "text_span": "not just making noise."
                                },
                                {
                                    "description": "A heart icon inside a speech bubble.",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "right",
                                    "transition": "pop"
                                }
                            ]
                        },
                        {
                            "narration_text": "I used to ask boring stuff like 'Where are you from?'",
                            "start_time": 200,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Host makes a slightly pained/embarrassed face.",
                                    "timestamp": 0,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "full",
                                    "transition": "none",
                                    "text_span": "I used to ask boring stuff"
                                },
                                {
                                    "description": "Speech bubble: 'Where are you from?'",
                                    "timestamp": 1.5,
                                    "duration": 2,
                                    "visual_type": "text",
                                    "position": "center",
                                    "transition": "fade"
                                },
                                {
                                    "description": "A yawn emoji icon.",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "right",
                                    "transition": "pop"
                                }
                            ]
                        },
                        {
                            "narration_text": "Got the answer, then... crickets. Back to square one.",
                            "start_time": 205,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "A simple map icon with a pin dropping.",
                                    "timestamp": 0,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "left",
                                    "transition": "fade",
                                    "text_span": "Got the answer,"
                                },
                                {
                                    "description": "Animation of cricket icons chirping.",
                                    "timestamp": 1.5,
                                    "duration": 2,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "slide",
                                    "text_span": "then... crickets."
                                },
                                {
                                    "description": "Icon of a board game piece moving back to the start square.",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "right",
                                    "transition": "fade",
                                    "text_span": "Back to square one."
                                }
                            ]
                        },
                        {
                            "narration_text": "Now I try: 'What's your favorite thing about living there?'",
                            "start_time": 210,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Host smiling, looking smarter.",
                                    "timestamp": 0,
                                    "duration": 1,
                                    "visual_type": "image",
                                    "position": "left",
                                    "transition": "none",
                                    "text_span": "Now I try:"
                                },
                                {
                                    "description": "Speech bubble: 'What's your favorite thing about living there?'",
                                    "timestamp": 1,
                                    "duration": 2.5,
                                    "visual_type": "text",
                                    "position": "center",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Sparkle animation around the speech bubble.",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "animation",
                                    "position": "right",
                                    "transition": "pop"
                                }
                            ]
                        },
                        {
                            "narration_text": "Much better! Opens up stories, not just facts.",
                            "start_time": 215,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Thumbs up icon changing to a 'Much Better!' text.",
                                    "timestamp": 0,
                                    "duration": 2,
                                    "visual_type": "animation",
                                    "position": "left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Icon of an open book with pages turning.",
                                    "timestamp": 2,
                                    "duration": 1.5,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "slide",
                                    "text_span": "Opens up stories,"
                                },
                                {
                                    "description": "Crossed out icon of a dry list or spreadsheet.",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "right",
                                    "transition": "fade",
                                    "text_span": "not just facts."
                                }
                            ]
                        },
                        {
                            "narration_text": "So remember: Observe, then ask open-ended questions.",
                            "start_time": 220,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Recap icons: Magnifying glass + Open Question Mark.",
                                    "timestamp": 0,
                                    "duration": 2,
                                    "visual_type": "image",
                                    "position": "center",
                                    "transition": "fade",
                                    "text_span": "Observe, then ask open-ended questions."
                                },
                                {
                                    "description": "A 'Formula for Success' text graphic.",
                                    "timestamp": 2,
                                    "duration": 1.5,
                                    "visual_type": "text",
                                    "position": "lower_third",
                                    "transition": "slide"
                                },
                                {
                                    "description": "Brain icon with gears turning smoothly.",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "animation",
                                    "position": "right",
                                    "transition": "pop"
                                }
                            ]
                        }
                    ]
                },
                {
                    "title": "Putting it Together & Conclusion: Your Turn!",
                    "content": "Quick recap of the steps, encouragement for the viewer to practice, and a call to action.",
                    "total_duration": 75,
                    "segments": [
                        {
                            "narration_text": "Okay, deep breath! You've got the tools now.",
                            "start_time": 225,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Animation of lungs inflating and deflating gently.",
                                    "timestamp": 0,
                                    "duration": 2,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "fade",
                                    "text_span": "Okay, deep breath!"
                                },
                                {
                                "description": "Icon of a toolbox filled with conversation starter tools (magnifying glass, open question mark).",
                                    "timestamp": 2,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "center",
                                    "transition": "slide"
                                },
                                {
                                    "description": "Text: 'You're Ready!'",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "text",
                                    "position": "lower_third",
                                    "transition": "pop",
                                    "text_span": "You've got the tools now."
                                }
                            ]
                        },
                        {
                            "narration_text": "Let's recap super quick: Step 1 - Observe.",
                            "start_time": 230,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Text: 'Recap!' flashing briefly.",
                                    "timestamp": 0,
                                    "duration": 1,
                                    "visual_type": "text",
                                    "position": "center",
                                    "transition": "fade"
                                },
                                {
                                "description": "Icon for Step 1: Magnifying glass.",
                                    "timestamp": 1,
                                    "duration": 2,
                                    "visual_type": "image",
                                    "position": "left",
                                    "transition": "slide",
                                    "text_span": "Step 1 - Observe."
                                },
                                {
                                    "description": "Short text below icon: 'Find your IN'.",
                                    "timestamp": 3,
                                    "duration": 2,
                                    "visual_type": "text",
                                    "position": "left",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "Use the shared situation, the environment, or something about them.",
                            "start_time": 235,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Mini-icons cycling: Coffee cup, park bench, t-shirt, book.",
                                    "timestamp": 0,
                                    "duration": 3,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "fade",
                                    "text_span": "shared situation, the environment, or something about them."
                                },
                                {
                                "description": "Arrow pointing towards these icons labeled 'Conversation Starters'.",
                                    "timestamp": 3,
                                    "duration": 1,
                                    "visual_type": "diagram",
                                    "position": "center",
                                    "transition": "none"
                                },
                                {
                                    "description": "Focus shifts back to the Magnifying Glass icon briefly.",
                                    "timestamp": 4,
                                    "duration": 1,
                                    "visual_type": "image",
                                    "position": "left",
                                    "transition": "zoom"
                                }
                            ]
                        },
                        {
                            "narration_text": "Step 2 - Ask Open-Ended Questions.",
                            "start_time": 240,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Icon for Step 2: Open Question Mark ('?').",
                                    "timestamp": 0,
                                    "duration": 2,
                                    "visual_type": "image",
                                    "position": "right",
                                    "transition": "slide",
                                    "text_span": "Step 2 - Ask Open-Ended Questions."
                                },
                                {
                                "description": "Short text below icon: 'Keep it FLOWING'.",
                                    "timestamp": 2,
                                    "duration": 1.5,
                                    "visual_type": "text",
                                    "position": "right",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Keywords 'What, How, Why' flashing near the icon.",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "text",
                                    "position": "right",
                                    "transition": "pop"
                                }
                            ]
                        },
                        {
                            "narration_text": "Invite detail, show interest, avoid the 'yes/no' trap.",
                            "start_time": 245,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Animation: Speech bubble growing larger.",
                                    "timestamp": 0,
                                    "duration": 1.5,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "zoom",
                                    "text_span": "Invite detail,"
                                },
                                {
                                "description": "Heart icon + Ear icon.",
                                    "timestamp": 1.5,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "center",
                                    "transition": "fade",
                                    "text_span": "show interest,"
                                },
                                {
                                    "description": "Red 'X' over a 'Yes/No' sign.",
                                    "timestamp": 3,
                                    "duration": 2,
                                    "visual_type": "image",
                                    "position": "center",
                                    "transition": "slide",
                                    "text_span": "avoid the 'yes/no' trap."
                                }
                            ]
                        },
                        {
                            "narration_text": "Remember my squeaky mouse moment? We learn!",
                            "start_time": 250,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Quick flashback image: Cartoon mouse squeaking.",
                                    "timestamp": 0,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "left",
                                    "transition": "fade",
                                    "text_span": "my squeaky mouse moment?"
                                },
                                {
                                "description": "Host laughing good-naturedly.",
                                    "timestamp": 1.5,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "center",
                                    "transition": "slide"
                                },
                                {
                                    "description": "Text: 'Progress, Not Perfection!'",
                                    "timestamp": 3,
                                    "duration": 2,
                                    "visual_type": "text",
                                    "position": "right",
                                    "transition": "fade",
                                    "text_span": "We learn!"
                                }
                            ]
                        },
                        {
                            "narration_text": "It's okay if it feels a bit clunky at first.",
                            "start_time": 255,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Animation of slightly mismatched gears trying to mesh.",
                                    "timestamp": 0,
                                    "duration": 2,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "fade",
                                    "text_span": "feels a bit clunky at first."
                                },
                                {
                                "description": "A comforting 'It's OK' hand gesture icon.",
                                    "timestamp": 2,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "right",
                                    "transition": "pop"
                                },
                                {
                                    "description": "Text: 'Keep Practicing'.",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "text",
                                    "position": "lower_third",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "Every single conversation is practice for the next one.",
                            "start_time": 260,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Diagram: Small conversation bubble -> Arrow -> Slightly larger bubble -> Arrow -> Even larger bubble.",
                                    "timestamp": 0,
                                    "duration": 3,
                                    "visual_type": "diagram",
                                    "position": "center",
                                    "transition": "slide",
                                    "text_span": "Every single conversation is practice"
                                },
                                {
                                "description": "Icon of a person leveling up (like in a game).",
                                    "timestamp": 3,
                                    "duration": 1,
                                    "visual_type": "image",
                                    "position": "right",
                                    "transition": "pop"
                                },
                                {
                                    "description": "Text: 'Growth Mindset'.",
                                    "timestamp": 4,
                                    "duration": 1,
                                    "visual_type": "text",
                                    "position": "lower_third",
                                    "transition": "fade",
                                    "text_span": "for the next one."
                                }
                            ]
                        },
                        {
                            "narration_text": "So, your mission, should you choose to accept it...",
                            "start_time": 265,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Host leans in with a playful 'secret mission' expression.",
                                    "timestamp": 0,
                                    "duration": 2,
                                    "visual_type": "image",
                                    "position": "full",
                                    "transition": "none",
                                    "text_span": "your mission,"
                                },
                                {
                                "description": "Animated graphic resembling a 'Top Secret' file opening.",
                                    "timestamp": 2,
                                    "duration": 1.5,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Text: 'Your Challenge!'",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "text",
                                    "position": "lower_third",
                                    "transition": "pop",
                                    "text_span": "should you choose to accept it..."
                                }
                            ]
                        },
                        {
                            "narration_text": "...is to try starting *one* conversation this week using these tips.",
                            "start_time": 270,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Large number '1' prominently displayed.",
                                    "timestamp": 0,
                                    "duration": 1.5,
                                    "visual_type": "text",
                                    "position": "center",
                                    "transition": "zoom",
                                    "text_span": "*one* conversation"
                                },
                                {
                                "description": "Calendar icon with one day highlighted.",
                                    "timestamp": 1.5,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "left",
                                    "transition": "slide",
                                    "text_span": "this week"
                                },
                                {
                                    "description": "Checklist icon with 'Observe' and 'Ask Open Qs' ticked off.",
                                    "timestamp": 3,
                                    "duration": 2,
                                    "visual_type": "image",
                                    "position": "right",
                                    "transition": "fade",
                                    "text_span": "using these tips."
                                }
                            ]
                        },
                        {
                            "narration_text": "Just one! At the store, waiting in line, anywhere.",
                            "start_time": 275,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Text 강조: 'Just ONE!'",
                                    "timestamp": 0,
                                    "duration": 1.5,
                                    "visual_type": "text",
                                    "position": "center",
                                    "transition": "fade"
                                },
                                {
                                "description": "Icons cycling: Shopping cart, queue of people, park bench.",
                                    "timestamp": 1.5,
                                    "duration": 2,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "slide",
                                    "text_span": "At the store, waiting in line, anywhere."
                                },
                                {
                                    "description": "A small 'target' icon.",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "right",
                                    "transition": "pop"
                                }
                            ]
                        },
                        {
                            "narration_text": "You might surprise yourself with how easy it can feel.",
                            "start_time": 280,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Image of a person looking pleasantly surprised.",
                                    "timestamp": 0,
                                    "duration": 2,
                                    "visual_type": "image",
                                    "position": "center",
                                    "transition": "fade",
                                    "text_span": "You might surprise yourself"
                                },
                                {
                                "description": "A 'feather' icon representing ease.",
                                    "timestamp": 2,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "right",
                                    "transition": "slide"
                                },
                                {
                                    "description": "Text: 'Easier Than You Think!'",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "text",
                                    "position": "lower_third",
                                    "transition": "fade",
                                    "text_span": "how easy it can feel."
                                }
                            ]
                        },
                        {
                            "narration_text": "Let me know how it goes in the comments below!",
                            "start_time": 285,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Host gestures downwards towards the comment section.",
                                    "timestamp": 0,
                                    "duration": 2,
                                    "visual_type": "image",
                                    "position": "full",
                                    "transition": "none",
                                    "text_span": "Let me know how it goes"
                                },
                                {
                                "description": "Animation of comment icons scrolling.",
                                    "timestamp": 2,
                                    "duration": 1.5,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "slide"
                                },
                                {
                                    "description": "Text: 'Share Your Experience!'",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "text",
                                    "position": "lower_third",
                                    "transition": "fade",
                                    "text_span": "in the comments below!"
                                }
                            ]
                        },
                        {
                            "narration_text": "You've totally got this. Go on, give it a try!",
                            "start_time": 290,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Host gives two enthusiastic thumbs up.",
                                    "timestamp": 0,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "full",
                                    "transition": "fade",
                                    "text_span": "You've totally got this."
                                },
                                {
                                "description": "Animated 'Go!' sign flashing.",
                                    "timestamp": 1.5,
                                    "duration": 1.5,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "pop"
                                },
                                {
                                    "description": "A final encouraging smile from the host.",
                                    "timestamp": 3,
                                    "duration": 2,
                                    "visual_type": "image",
                                    "position": "full",
                                    "transition": "fade",
                                    "text_span": "Go on, give it a try!"
                                }
                            ]
                        },
                        {
                            "narration_text": "Thanks for watching! See ya next time.",
                            "start_time": 295,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Text overlay: 'Thanks for watching!'",
                                    "timestamp": 0,
                                    "duration": 2,
                                    "visual_type": "text",
                                    "position": "center",
                                    "transition": "fade"
                                },
                                {
                                "description": "End screen graphics: Subscribe button, links to other videos, social media handles.",
                                    "timestamp": 2,
                                    "duration": 3,
                                    "visual_type": "image",
                                    "position": "full",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Host waving goodbye.",
                                    "timestamp": 2.5,
                                    "duration": 2.5,
                                    "visual_type": "image",
                                    "position": "bottom_right",
                                    "transition": "fade",
                                    "text_span": "See ya next time."
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        ```
        """
        script_data = self._parse_llm_response(whatnow, request)
        
        # Create the script object
        script = Script(
            id=f"script-{uuid.uuid4()}",
            title=script_data["title"],
            description=script_data["description"],
            target_audience=request.target_audience,
            style=request.style,
            inspiration=request.inspiration,
            visual_style=request.visual_style,
            sections=self._create_sections(script_data["sections"]),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            total_duration=script_data["total_duration"],
            status="draft"
        )
        
        return script

    def _create_script_generation_prompt(self, request: ScriptRequest) -> str:
        """
        Create a prompt for generating a script.
        
        Args:
            request: The script generation request
            
        Returns:
            A prompt for the LLM
        """
        print("Creating script generation prompt")
        print(request)
        inspiration_text = f"\n\n**Inspiration:** {request.inspiration}\nUse this inspiration as the main creative or thematic driver for the script. Make sure the script reflects this inspiration throughout, in both content and tone.\n" if hasattr(request, 'inspiration') and getattr(request, 'inspiration', None) else ""
        return f"""
        Create a detailed script for an educational video about \"{request.topic}\".

        Instead of addressing a general audience, write the script as if you are speaking directly to a single person, making it personal and conversational. Use 'you' and 'your' to address the viewer, and make the tone friendly and engaging.
        Target audience: {request.target_audience}
        Approximate duration: 10 minutes (Meaning each section should contain about 2 minutes of content or 15 segments)
        Style: {request.style} and slightly humorous
        {inspiration_text}
        
        **Instructions:**
        1. Structure the script into logical sections (e.g., Introduction, Key Point 1, Key Point 2, Example, Conclusion).
        2. Divide each section into multiple short, focused segments. Each segment represents a few sentences of narration.
        3. **For EACH segment, generate AT LEAST THREE distinct visual suggestions.**
        4. **For EACH visual, you MUST ensure it is tightly aligned with the narration text at the visual's timestamp:**
           - If a segment has multiple visuals, break down the narration text so that each visual matches the exact part being spoken at its timestamp.
           - The visual's description MUST be contextually and temporally relevant—do NOT use generic illustrations. The visual should clearly reflect what is being narrated at that moment.
           - Optionally, for each visual, include a `text_span` or short excerpt from the narration text that is being visualized at that timestamp.
        5. For each visual, also provide:
           - Timestamp: When the visual should appear within the segment (relative to the segment's start time, in seconds).
           - Duration: How long the visual should be displayed (in seconds).
           - Visual type (image, animation, diagram, or text)
           - Position (left, right, center, full)
           - Transition (fade, slide, zoom, none)
        6. VERY IMPORTANT: Provide at least 15 segments for each section
        
        Format your response as a JSON object with the following structure:
        {{
            "title": "Title of the video",
            "description": "Brief description of the video",
            "total_duration": total_duration_in_seconds,
            "sections": [
                {{
                    "title": "Section title",
                    "content": "Overview of the section",
                    "total_duration": section_duration_in_seconds,
                    "segments": [
                        {{
                            "narration_text": "Text to be narrated",
                            "start_time": start_time_in_seconds,
                            "duration": duration_in_seconds,
                            "visuals": [
                                {{
                                    "description": "Description for image generation, directly reflecting the narration text (MINIMALISTIC VISUAL).",
                                }}
                            ]
                        }}
                    ]
                }}
            ]
        }}
        
        **Important:** Make sure the script is engaging, educational, and appropriate for the target audience. Ensure the total duration is respected, segment timings are sequential, and visual timestamps/durations fit within their parent segment. The visual descriptions are critical – make them specific and evocative. Generate AT LEAST TWO visuals per segment.
        """

    def _parse_llm_response(self, response: str, request: ScriptRequest) -> Dict[str, Any]:
        """
        Parse the LLM response into a script data dictionary.
        
        Args:
            response: The LLM response
            request: The original request
            
        Returns:
            A dictionary with script data
        """
        try:
            # Extract JSON from the response (in case the LLM added extra text)
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in response")
            
            json_str = response[json_start:json_end]
            script_data = json.loads(json_str)
            
            # Validate the script data
            if "title" not in script_data:
                script_data["title"] = f"Understanding {request.topic}"
            
            if "description" not in script_data:
                script_data["description"] = f"A comprehensive explanation of {request.topic} for {request.target_audience} audiences."
            
            if "total_duration" not in script_data:
                # Estimate total duration based on request
                script_data["total_duration"] = request.duration_minutes * 60
            
            # Set the section's total duration to 60
            for section in script_data["sections"]:
                section["total_duration"] = 60
                for segment in section["segments"]:
                    segment["start_time"] = 0
                    segment["duration"] = 10
                    for visual in segment["visuals"]:
                        visual['visual_style'] = request.visual_style
                        visual['timestamp'] = 0.0
                        visual['duration'] = 2.0
                        visual["visual_type"] = "image"
                        visual['zoom_level'] = 1.0
                        visual['position'] = 'center'
                        visual['text_span'] = ""
                        visual['transition'] = 'fade'
            
            # # If visual style is set, override all visual_style fields in visuals
            # if getattr(request, 'visual_style', None):
            #     def set_visual_style(obj):
            #         if isinstance(obj, dict):
            #             for k, v in obj.items():
            #                 if k == 'visuals' and isinstance(v, list):
            #                     for visual in v:
            #                         if isinstance(visual, dict):
            #                             visual['visual_style'] = request.visual_style
            #                             visual['timestamp'] = 0.0
            #                             visual['duration'] = 2.0
            #                             visual["visual_type"] = "image"
            #                             visual['zoom_level'] = 1.0
            #                             visual['position'] = 'center'
            #                             visual['text_span'] = ""
            #                             visual['transition'] = 'fade'
            #                 else:
            #                     set_visual_style(v)
            #         elif isinstance(obj, list):
            #             for item in obj:
            #                 set_visual_style(item)
            #     set_visual_style(script_data)
            return script_data
        except Exception as e:
            # If parsing fails, return None and print error with details and debug info
            import traceback
            print(f"Error parsing LLM response: {e}")
            print(traceback.format_exc())
            return None

    async def regenerate_section(self, section_id: str, sections: list, inspiration: str) -> dict:
        """
        Regenerate a single section using context from all sections and inspiration.
        Args:
            section_id: ID of the section to regenerate
            sections: List of all sections (dicts)
            inspiration: Inspiration text
            prompt: User's prompt
        Returns:
            The regenerated section as a dict (ScriptSection-like)
        """
        # Find the section to regenerate
        section_to_regen = next((s for s in sections if s.get("id") == section_id), None)
        if not section_to_regen:
            raise ValueError(f"Section with id {section_id} not found")
        # Prepare context for the LLM
        other_sections = [s for s in sections if s.get("id") != section_id]
        context_str = "\n\n".join([
            "\n".join([f"Segment: {seg.get('id', '')}\nNarrationText: {seg.get('narrationText', '')}" for seg in s.get("segments", [])])
            for s in other_sections
        ])
        regen_prompt = f"""
        You are an expert scriptwriter for educational videos. Your job is to regenerate a specific section of a script, ensuring it fits contextually with the rest of the script and is inspired by the following:

        Inspiration: {inspiration}

        Other Sections Context:
        {context_str}

        ---

        Regenerate the following section so it fits seamlessly with the rest of the script. Be creative, ensure the style and tone match the context and inspiration, and preserve any important structure or information:

        Section to Regenerate:
        Title: {section_to_regen.get('title', '')}
        Content: {section_to_regen.get('content', '')}

        User Prompt: {prompt}

        Return your result as a JSON object with the following structure:
        {{
            "id": "{section_id}",
            "title": "Section title",
            "content": "Overview of the section",
            "total_duration": section_duration_in_seconds,
            "segments": [
                {{
                    "narration_text": "Text to be narrated",
                    "start_time": start_time_in_seconds,
                    "duration": duration_in_seconds,
                    "visuals": [
                        {{
                            "description": "Description for image generation, directly reflecting the narration text (MINIMALISTIC VISUAL).",
                            "timestamp": timestamp_in_seconds,
                            "duration": duration_in_seconds,
                            "visual_type": "image|animation|diagram|text",
                            "visual_style": "Style guidance (optional)",
                            "position": "left|right|center|full",
                            "text_span": "Text span for text visuals (optional)",
                            "transition": "fade|slide|zoom|none"
                        }}
                    ]
                }}
            ]
        }}
        """
        response = await self.llm_provider.generate_completion(
            messages=[
                {"role": "system", "content": "You are an expert scriptwriter for educational videos."},
                {"role": "user", "content": regen_prompt}
            ],
            temperature=0.7
        )
        # Parse the response as a single section
        import json as _json
        try:
            json_start = response["content"].find('{')
            json_end = response["content"].rfind('}') + 1
            section_json = response["content"][json_start:json_end]
            section_data = _json.loads(section_json)
            return section_data
        except Exception as e:
            import traceback
            print(f"Error parsing regenerated section: {e}")
            print(traceback.format_exc())
            raise

    def _create_sections(self, sections_data: List[Dict[str, Any]]) -> List[ScriptSection]:
        """
        Create script sections from the parsed data.
        
        Args:
            sections_data: List of section data dictionaries
            
        Returns:
            List of ScriptSection objects
        """
        sections = []
        
        for i, section_data in enumerate(sections_data):
            # Create segments
            segments = []
            for j, segment_data in enumerate(section_data.get("segments", [])):
                # Create visuals
                visuals = []
                for k, visual_data in enumerate(segment_data.get("visuals", [])):
                    visual = Visual(
                        id=f"visual-{i+1}-{j+1}-{k+1}",
                        description=visual_data.get("description", ""),
                        timestamp=visual_data.get("timestamp", 0),
                        duration=visual_data.get("duration", 5),
                        visual_type=visual_data.get("visual_type", "image"),
                        visual_style=visual_data.get("visual_style"),
                        position=visual_data.get("position", "center"),
                        transition=visual_data.get("transition", "fade")
                    )
                    visuals.append(visual)
                
                # Create segment
                segment = ScriptSegment(
                    id=f"segment-{i+1}-{j+1}",
                    narration_text=segment_data.get("narration_text", ""),
                    start_time=segment_data.get("start_time", 0),
                    duration=segment_data.get("duration", 10),
                    visuals=visuals
                )
                segments.append(segment)
            
            # Create section
            section = ScriptSection(
                id=f"section-{i+1}",
                title=section_data.get("title", f"Section {i+1}"),
                content=section_data.get("content", ""),
                segments=segments,
                total_duration=section_data.get("total_duration", 0)
            )
            sections.append(section)
        
        return sections
