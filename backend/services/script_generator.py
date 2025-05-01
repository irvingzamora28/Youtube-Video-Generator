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
            "title": "Why Your Best Ideas Hit You in the Shower",
            "description": "A friendly chat explaining the science behind why you often get brilliant ideas while showering, focusing on relaxation and the brain's Default Mode Network.",
            "total_duration": 300,
            "sections": [
                {
                    "title": "Introduction: The Shower Epiphany",
                    "content": "Hooking you with the common experience of shower thoughts and setting the stage for the explanation.",
                    "total_duration": 75,
                    "segments": [
                        {
                            "narration_text": "Hey there! Ever notice how some of your best, most brilliant ideas pop into your head... in the shower?",
                            "start_time": 0,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Minimalist animation: A lightbulb icon appearing above a simple outline of a person's head inside a shower outline.",
                                    "text_span": "...brilliant ideas pop into your head...",
                                    "timestamp": 0.5,
                                    "duration": 2.0,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Image: Close-up, slightly steamy view of water droplets on shower tiles.",
                                    "text_span": "...in the shower?",
                                    "timestamp": 2.5,
                                    "duration": 2.0,
                                    "visual_type": "image",
                                    "position": "full",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Text Overlay: Question mark symbol (?) styled like dripping water.",
                                    "text_span": "Ever notice how...",
                                    "timestamp": 0.0,
                                    "duration": 4.5,
                                    "visual_type": "text",
                                    "position": "top_right",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "You're just standing there, minding your own business, lathering up...",
                            "start_time": 5,
                            "duration": 4,
                            "visuals": [
                                {
                                    "description": "Simple line drawing animation: A figure nonchalantly standing under falling lines representing shower water.",
                                    "text_span": "You're just standing there...",
                                    "timestamp": 0.0,
                                    "duration": 2.0,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "slide_in_left"
                                },
                                {
                                    "description": "Image: Close-up shot of soap bubbles forming on skin.",
                                    "text_span": "...lathering up...",
                                    "timestamp": 2.0,
                                    "duration": 2.0,
                                    "visual_type": "image",
                                    "position": "center",
                                    "transition": "zoom_in"
                                },
                                {
                                    "description": "Text Overlay: Simple text 'Minding my own business...' appearing briefly.",
                                    "text_span": "...minding your own business...",
                                    "timestamp": 1.0,
                                    "duration": 2.5,
                                    "visual_type": "text",
                                    "position": "bottom_center",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "...and BAM! Suddenly, the solution to that tricky problem you were stuck on appears.",
                            "start_time": 9,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Animation: A stylized 'BAM!' comic book graphic explodes on screen.",
                                    "text_span": "...and BAM!",
                                    "timestamp": 0.0,
                                    "duration": 1.5,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "zoom_out"
                                },
                                {
                                    "description": "Diagram: A tangled knot icon quickly unraveling into a straight line.",
                                    "text_span": "...solution to that tricky problem...",
                                    "timestamp": 1.5,
                                    "duration": 2.0,
                                    "visual_type": "diagram",
                                    "position": "center_right",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Image: A person's eyes widening slightly in surprise (viewed from side, minimalist).",
                                    "text_span": "Suddenly... appears.",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "center_left",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "Or maybe a completely new, creative idea just materializes out of the steam.",
                            "start_time": 14,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Animation: A thought bubble containing a sparkling star rising from stylized steam clouds.",
                                    "text_span": "...new, creative idea just materializes...",
                                    "timestamp": 0.5,
                                    "duration": 2.5,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Image: Abstract blurry image suggesting steam or mist.",
                                    "text_span": "...out of the steam.",
                                    "timestamp": 3.0,
                                    "duration": 2.0,
                                    "visual_type": "image",
                                    "position": "full",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Text Overlay: 'Eureka!' styled like it's written on a steamy mirror.",
                                    "text_span": "creative idea",
                                    "timestamp": 1.0,
                                    "duration": 3.0,
                                    "visual_type": "text",
                                    "position": "top_center",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "It feels almost magical, right? Like the shower has some secret idea-generating power.",
                            "start_time": 19,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Animation: Sparkles briefly appearing around a minimalist shower head icon.",
                                    "text_span": "It feels almost magical...",
                                    "timestamp": 0.0,
                                    "duration": 2.0,
                                    "visual_type": "animation",
                                    "position": "center_left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Image: A person looking thoughtfully upwards, slight smile (minimalist style).",
                                    "text_span": "...right?",
                                    "timestamp": 2.0,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "center_right",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Text Overlay: 'Secret Power?' with a water drop replacing the dot.",
                                    "text_span": "...secret idea-generating power.",
                                    "timestamp": 2.5,
                                    "duration": 2.5,
                                    "visual_type": "text",
                                    "position": "bottom_center",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "Well, you're not imagining it! There's actually some cool brain science behind this.",
                            "start_time": 24,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Animation: A simple brain icon with gears turning slowly inside.",
                                    "text_span": "...cool brain science...",
                                    "timestamp": 1.0,
                                    "duration": 2.5,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "zoom_in"
                                },
                                {
                                    "description": "Text Overlay: 'It's SCIENCE!' appearing in a fun, bubbly font.",
                                    "text_span": "Well, you're not imagining it!",
                                    "timestamp": 0.0,
                                    "duration": 2.0,
                                    "visual_type": "text",
                                    "position": "top_left",
                                    "transition": "slide_down"
                                },
                                {
                                    "description": "Image: A finger pointing upwards as if making a point (simple illustration).",
                                    "text_span": "behind this.",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "center_right",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "It's not the water itself, obviously, though the shower environment plays a huge role.",
                            "start_time": 29,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Animation: Water droplet icon with a red 'X' crossed over it.",
                                    "text_span": "It's not the water itself...",
                                    "timestamp": 0.0,
                                    "duration": 2.0,
                                    "visual_type": "animation",
                                    "position": "center_left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Image: Silhouette of a person comfortably inside a shower cubicle outline.",
                                    "text_span": "...shower environment plays a huge role.",
                                    "timestamp": 2.0,
                                    "duration": 3.0,
                                    "visual_type": "image",
                                    "position": "center_right",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Text Overlay: 'Environment is Key' appearing.",
                                    "text_span": "environment plays a huge role.",
                                    "timestamp": 2.5,
                                    "duration": 2.0,
                                    "visual_type": "text",
                                    "position": "bottom_center",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "Think about what happens when you step into that warm, private space.",
                            "start_time": 34,
                            "duration": 4,
                            "visuals": [
                                {
                                    "description": "Animation: Steam/heat waves rising from a simple line.",
                                    "text_span": "...warm...",
                                    "timestamp": 0.5,
                                    "duration": 1.5,
                                    "visual_type": "animation",
                                    "position": "center_left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Image: A simple 'Do Not Disturb' sign icon.",
                                    "text_span": "...private space.",
                                    "timestamp": 2.0,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "center_right",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Text Overlay: 'Your Zone' inside a bubble.",
                                    "text_span": "private space.",
                                    "timestamp": 2.0,
                                    "duration": 2.0,
                                    "visual_type": "text",
                                    "position": "bottom_center",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "Firstly, you're usually alone. No emails pinging, no one asking you questions.",
                            "start_time": 38,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Animation: A stylized email notification icon with a red slash through it.",
                                    "text_span": "No emails pinging...",
                                    "timestamp": 0.5,
                                    "duration": 2.0,
                                    "visual_type": "animation",
                                    "position": "center_left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Animation: A speech bubble icon with a question mark inside, also crossed out.",
                                    "text_span": "...no one asking you questions.",
                                    "timestamp": 2.5,
                                    "duration": 2.0,
                                    "visual_type": "animation",
                                    "position": "center_right",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Image: A simple icon of a person with headphones on, looking peaceful.",
                                    "text_span": "Firstly, you're usually alone.",
                                    "timestamp": 0.0,
                                    "duration": 4.5,
                                    "visual_type": "image",
                                    "position": "top_center",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "It's a rare moment of solitude in our busy lives, wouldn't you agree?",
                            "start_time": 43,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Image: A minimalist clock icon with hands spinning rapidly.",
                                    "text_span": "...busy lives...",
                                    "timestamp": 1.0,
                                    "duration": 2.0,
                                    "visual_type": "image",
                                    "position": "center_left",
                                    "transition": "zoom_in"
                                },
                                {
                                    "description": "Animation: A simple 'pause' button icon appearing.",
                                    "text_span": "rare moment of solitude...",
                                    "timestamp": 0.0,
                                    "duration": 2.0,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Text Overlay: 'Agree?' with a simple checkmark.",
                                    "text_span": "...wouldn't you agree?",
                                    "timestamp": 3.0,
                                    "duration": 2.0,
                                    "visual_type": "text",
                                    "position": "bottom_right",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "This lack of external distraction is crucial. It lets your mind off the leash.",
                            "start_time": 48,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Animation: Icons representing distractions (phone, email, bell) fading away.",
                                    "text_span": "lack of external distraction...",
                                    "timestamp": 0.0,
                                    "duration": 2.5,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Image: A simple drawing of a dog happily running free from a leash.",
                                    "text_span": "...lets your mind off the leash.",
                                    "timestamp": 2.5,
                                    "duration": 2.5,
                                    "visual_type": "image",
                                    "position": "center",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Text Overlay: 'Mind Unleashed!' in a playful font.",
                                    "text_span": "mind off the leash.",
                                    "timestamp": 3.0,
                                    "duration": 2.0,
                                    "visual_type": "text",
                                    "position": "top_center",
                                    "transition": "slide_down"
                                }
                            ]
                        },
                        {
                            "narration_text": "Secondly, the warm water and the white noise of the shower are incredibly relaxing.",
                            "start_time": 53,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Animation: Gentle wavy lines representing warmth radiating.",
                                    "text_span": "warm water...",
                                    "timestamp": 0.5,
                                    "duration": 2.0,
                                    "visual_type": "animation",
                                    "position": "center_left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Animation: Sound wave icon representing 'white noise'.",
                                    "text_span": "...white noise of the shower...",
                                    "timestamp": 2.0,
                                    "duration": 2.0,
                                    "visual_type": "animation",
                                    "position": "center_right",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Image: A simple icon of a person leaning back with eyes closed, relaxed.",
                                    "text_span": "...incredibly relaxing.",
                                    "timestamp": 3.0,
                                    "duration": 2.0,
                                    "visual_type": "image",
                                    "position": "bottom_center",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "This relaxation isn't just pleasant; it changes your brain activity.",
                            "start_time": 58,
                            "duration": 4,
                            "visuals": [
                                {
                                    "description": "Image: A simple 'thumbs up' icon for 'pleasant'.",
                                    "text_span": "...isn't just pleasant...",
                                    "timestamp": 0.0,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "center_left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Diagram: Simple brain outline with wave patterns inside changing.",
                                    "text_span": "...changes your brain activity.",
                                    "timestamp": 1.5,
                                    "duration": 2.5,
                                    "visual_type": "diagram",
                                    "position": "center_right",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Text Overlay: 'Brain Shift' with an arrow.",
                                    "text_span": "changes your brain activity.",
                                    "timestamp": 2.0,
                                    "duration": 2.0,
                                    "visual_type": "text",
                                    "position": "top_center",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "So, you're alone, relaxed, and not actively trying to think.",
                            "start_time": 62,
                            "duration": 4,
                            "visuals": [
                                {
                                    "description": "Image: Icon of a single person symbol.",
                                    "text_span": "So, you're alone...",
                                    "timestamp": 0.0,
                                    "duration": 1.0,
                                    "visual_type": "image",
                                    "position": "left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Image: A simple 'zen' or meditating icon.",
                                    "text_span": "...relaxed...",
                                    "timestamp": 1.0,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "center",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Animation: A brain icon with a 'no entry' sign over the 'thinking hard' area.",
                                    "text_span": "...not actively trying to think.",
                                    "timestamp": 2.5,
                                    "duration": 1.5,
                                    "visual_type": "animation",
                                    "position": "right",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "That's the perfect recipe! Let's dive into exactly what happens in your brain next.",
                            "start_time": 66,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Image: A simple icon of a recipe card with a checkmark.",
                                    "text_span": "That's the perfect recipe!",
                                    "timestamp": 0.0,
                                    "duration": 2.0,
                                    "visual_type": "image",
                                    "position": "center_left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Animation: An arrow pointing downwards, indicating 'diving in'.",
                                    "text_span": "Let's dive into...",
                                    "timestamp": 2.0,
                                    "duration": 1.0,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "bounce"
                                },
                                {
                                    "description": "Diagram: A magnifying glass hovering over a simple brain icon.",
                                    "text_span": "...exactly what happens in your brain next.",
                                    "timestamp": 3.0,
                                    "duration": 2.0,
                                    "visual_type": "diagram",
                                    "position": "center_right",
                                    "transition": "fade"
                                }
                            ]
                        }
                    ]
                },
                {
                    "title": "Key Point 1: The Power of Relaxation & Alpha Waves",
                    "content": "Explaining how the relaxed shower state shifts brain activity, allowing for less constrained thinking.",
                    "total_duration": 75,
                    "segments": [
                        {
                            "narration_text": "Okay, so first ingredient: relaxation. That warm water isn't just cozy, it's a signal to your body.",
                            "start_time": 75,
                            "duration": 6,
                            "visuals": [
                                {
                                    "description": "Image: A simple icon of a steaming mug or bath.",
                                    "text_span": "That warm water isn't just cozy...",
                                    "timestamp": 1.0,
                                    "duration": 2.0,
                                    "visual_type": "image",
                                    "position": "center_left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Animation: A simple 'signal' icon (like radio waves) emitting from the water icon towards a body outline.",
                                    "text_span": "...it's a signal to your body.",
                                    "timestamp": 3.0,
                                    "duration": 2.5,
                                    "visual_type": "animation",
                                    "position": "center_right",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Text Overlay: 'Ingredient #1: Relax!'",
                                    "text_span": "first ingredient: relaxation.",
                                    "timestamp": 0.0,
                                    "duration": 3.0,
                                    "visual_type": "text",
                                    "position": "top_center",
                                    "transition": "slide_down"
                                }
                            ]
                        },
                        {
                            "narration_text": "It tells your nervous system, 'Hey, you can chill out now. No tigers chasing you.'",
                            "start_time": 81,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Diagram: Simple icon showing a switch flipping from 'Stress' (red) to 'Relax' (green).",
                                    "text_span": "It tells your nervous system...",
                                    "timestamp": 0.0,
                                    "duration": 2.5,
                                    "visual_type": "diagram",
                                    "position": "center",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Animation: A cartoonish sabre-tooth tiger icon with a red 'X' over it.",
                                    "text_span": "No tigers chasing you.",
                                    "timestamp": 2.5,
                                    "duration": 2.0,
                                    "visual_type": "animation",
                                    "position": "center_right",
                                    "transition": "pop"
                                },
                                {
                                    "description": "Text Overlay: 'Chill Mode: ON'",
                                    "text_span": "'Hey, you can chill out now.",
                                    "timestamp": 1.0,
                                    "duration": 2.5,
                                    "visual_type": "text",
                                    "position": "bottom_center",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "This reduces your stress levels, lowering cortisol, the stress hormone.",
                            "start_time": 86,
                            "duration": 4,
                            "visuals": [
                                {
                                    "description": "Animation: A bar graph labeled 'Stress Level' quickly decreasing.",
                                    "text_span": "reduces your stress levels...",
                                    "timestamp": 0.0,
                                    "duration": 2.0,
                                    "visual_type": "animation",
                                    "position": "center_left",
                                    "transition": "slide_down"
                                },
                                {
                                    "description": "Text Overlay: Chemical symbol for Cortisol (stylized) with a downward arrow.",
                                    "text_span": "...lowering cortisol...",
                                    "timestamp": 1.5,
                                    "duration": 2.0,
                                    "visual_type": "text",
                                    "position": "center_right",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Image: A simple 'down arrow' icon.",
                                    "text_span": "lowering",
                                    "timestamp": 1.5,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "center",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "When you're less stressed and more relaxed, your brain shifts gears.",
                            "start_time": 90,
                            "duration": 4,
                            "visuals": [
                                {
                                    "description": "Image: A simple icon of a person sighing contentedly.",
                                    "text_span": "less stressed and more relaxed...",
                                    "timestamp": 0.0,
                                    "duration": 2.0,
                                    "visual_type": "image",
                                    "position": "center_left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Animation: Simple gear icons meshing and then shifting position.",
                                    "text_span": "...your brain shifts gears.",
                                    "timestamp": 2.0,
                                    "duration": 2.0,
                                    "visual_type": "animation",
                                    "position": "center_right",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Text Overlay: 'Brain Shift 2.0'",
                                    "text_span": "brain shifts gears.",
                                    "timestamp": 2.0,
                                    "duration": 1.5,
                                    "visual_type": "text",
                                    "position": "top_center",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "It moves away from sharp, focused attention – what scientists call 'beta waves'.",
                            "start_time": 94,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Diagram: Icon of a brain with jagged, fast 'Beta Wave' patterns highlighted.",
                                    "text_span": "...'beta waves'.",
                                    "timestamp": 2.5,
                                    "duration": 2.0,
                                    "visual_type": "diagram",
                                    "position": "center_right",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Animation: A spotlight icon narrowing its beam, then fading out.",
                                    "text_span": "sharp, focused attention...",
                                    "timestamp": 0.5,
                                    "duration": 2.0,
                                    "visual_type": "animation",
                                    "position": "center_left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Text Overlay: Greek letter Beta (β) displayed.",
                                    "text_span": "'beta waves'",
                                    "timestamp": 3.0,
                                    "duration": 1.5,
                                    "visual_type": "text",
                                    "position": "bottom_center",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "Beta waves are great when you need to concentrate hard on a task, like solving a math problem.",
                            "start_time": 99,
                            "duration": 6,
                            "visuals": [
                                {
                                    "description": "Image: Icon of a person intensely focused on a laptop screen.",
                                    "text_span": "concentrate hard on a task...",
                                    "timestamp": 1.0,
                                    "duration": 2.5,
                                    "visual_type": "image",
                                    "position": "center_left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Image: A simple illustration of a math equation (e.g., x + y = z).",
                                    "text_span": "...solving a math problem.",
                                    "timestamp": 3.5,
                                    "duration": 2.0,
                                    "visual_type": "image",
                                    "position": "center_right",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Text Overlay: 'Focus Mode' with a target icon.",
                                    "text_span": "Beta waves are great",
                                    "timestamp": 0.0,
                                    "duration": 3.0,
                                    "visual_type": "text",
                                    "position": "top_center",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "But in the shower, your brain often shifts into a state dominated by 'alpha waves'.",
                            "start_time": 105,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Animation: Brain icon transitioning from jagged 'Beta' waves to slower, rounded 'Alpha' waves.",
                                    "text_span": "...shifts into a state dominated by 'alpha waves'.",
                                    "timestamp": 1.5,
                                    "duration": 3.0,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Image: Simple shower head icon.",
                                    "text_span": "But in the shower...",
                                    "timestamp": 0.0,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "center_left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Text Overlay: Greek letter Alpha (α) displayed.",
                                    "text_span": "'alpha waves'",
                                    "timestamp": 3.0,
                                    "duration": 1.5,
                                    "visual_type": "text",
                                    "position": "bottom_center",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "Alpha waves are associated with being awake but relaxed, calm, and reflective.",
                            "start_time": 110,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Image: Icon of an open eye, but looking calm.",
                                    "text_span": "awake but relaxed...",
                                    "timestamp": 0.5,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Image: A simple icon representing calmness, like still water.",
                                    "text_span": "...calm...",
                                    "timestamp": 2.0,
                                    "duration": 1.0,
                                    "visual_type": "image",
                                    "position": "center",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Image: A thought bubble icon, suggesting reflection.",
                                    "text_span": "...and reflective.",
                                    "timestamp": 3.0,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "right",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "Think of it like daydreaming, or that pleasant state just before you fall asleep.",
                            "start_time": 115,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Animation: Simple cloud shapes drifting lazily across the screen.",
                                    "text_span": "Think of it like daydreaming...",
                                    "timestamp": 0.0,
                                    "duration": 2.5,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "slide_right"
                                },
                                {
                                    "description": "Image: Minimalist icon of a person in bed, eyes half-closed.",
                                    "text_span": "...state just before you fall asleep.",
                                    "timestamp": 2.5,
                                    "duration": 2.0,
                                    "visual_type": "image",
                                    "position": "center",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Text Overlay: 'Floaty Brain State'",
                                    "text_span": "pleasant state",
                                    "timestamp": 1.0,
                                    "duration": 3.0,
                                    "visual_type": "text",
                                    "position": "bottom_left",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "This alpha state is highly conducive to creativity and insight.",
                            "start_time": 120,
                            "duration": 4,
                            "visuals": [
                                {
                                    "description": "Diagram: Alpha wave symbol pointing towards a lightbulb icon (insight) and a painter's palette icon (creativity).",
                                    "text_span": "alpha state is highly conducive to creativity and insight.",
                                    "timestamp": 0.5,
                                    "duration": 3.0,
                                    "visual_type": "diagram",
                                    "position": "center",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Text Overlay: 'Alpha = Aha!'",
                                    "text_span": "Alpha state... insight.",
                                    "timestamp": 1.5,
                                    "duration": 2.0,
                                    "visual_type": "text",
                                    "position": "top_center",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Image: A simple '+' sign icon.",
                                    "text_span": "conducive",
                                    "timestamp": 1.0,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "center_left",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "Your mind isn't laser-focused, so it's free to wander and make unexpected connections.",
                            "start_time": 124,
                            "duration": 6,
                            "visuals": [
                                {
                                    "description": "Animation: A laser beam icon turning off or diffusing.",
                                    "text_span": "Your mind isn't laser-focused...",
                                    "timestamp": 0.0,
                                    "duration": 2.0,
                                    "visual_type": "animation",
                                    "position": "center_left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Animation: Dotted lines meandering and connecting between different simple icons (e.g., apple, chair, star).",
                                    "text_span": "...free to wander and make unexpected connections.",
                                    "timestamp": 2.0,
                                    "duration": 3.5,
                                    "visual_type": "animation",
                                    "position": "center_right",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Text Overlay: 'Wander & Wonder'",
                                    "text_span": "free to wander",
                                    "timestamp": 2.5,
                                    "duration": 2.5,
                                    "visual_type": "text",
                                    "position": "bottom_center",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "It's like loosening the reins on your thoughts, letting them roam.",
                            "start_time": 130,
                            "duration": 4,
                            "visuals": [
                                {
                                    "description": "Image: Simple illustration of hands loosening reins.",
                                    "text_span": "loosening the reins...",
                                    "timestamp": 0.5,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "center_left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Animation: Thought bubbles floating freely upwards and outwards.",
                                    "text_span": "...letting them roam.",
                                    "timestamp": 2.0,
                                    "duration": 2.0,
                                    "visual_type": "animation",
                                    "position": "center_right",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Text Overlay: 'Free Range Thoughts'",
                                    "text_span": "letting them roam.",
                                    "timestamp": 2.0,
                                    "duration": 1.5,
                                    "visual_type": "text",
                                    "position": "top_center",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "So, the relaxation helps switch off that intense focus...",
                            "start_time": 134,
                            "duration": 4,
                            "visuals": [
                                {
                                    "description": "Animation: A switch icon flipping to the 'OFF' position.",
                                    "text_span": "...switch off...",
                                    "timestamp": 1.0,
                                    "duration": 1.5,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Image: Icon representing intense focus (like a target) fading out.",
                                    "text_span": "...that intense focus...",
                                    "timestamp": 2.0,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "center_right",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Image: Simple 'Spa / Relax' icon (e.g., cucumber slices).",
                                    "text_span": "So, the relaxation helps...",
                                    "timestamp": 0.0,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "center_left",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "...which allows your brain to enter the creative alpha wave state.",
                            "start_time": 138,
                            "duration": 4,
                            "visuals": [
                                {
                                    "description": "Animation: An arrow pointing towards the Alpha wave symbol (α).",
                                    "text_span": "...enter the creative alpha wave state.",
                                    "timestamp": 1.0,
                                    "duration": 2.5,
                                    "visual_type": "animation",
                                    "position": "center_right",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Image: A simple brain icon.",
                                    "text_span": "your brain",
                                    "timestamp": 0.5,
                                    "duration": 1.0,
                                    "visual_type": "image",
                                    "position": "center_left",
                                    "transition": "none"
                                },
                                {
                                    "description": "Text Overlay: 'Creative Zone'",
                                    "text_span": "creative alpha wave state.",
                                    "timestamp": 1.5,
                                    "duration": 2.0,
                                    "visual_type": "text",
                                    "position": "bottom_center",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "But that's only part of the story! There's another key player...",
                            "start_time": 142,
                            "duration": 4,
                            "visuals": [
                                {
                                    "description": "Image: A puzzle piece icon, labeled 'Part 1'.",
                                    "text_span": "only part of the story!",
                                    "timestamp": 0.5,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "center_left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Animation: A question mark appearing, hinting at the next part.",
                                    "text_span": "There's another key player...",
                                    "timestamp": 2.0,
                                    "duration": 1.5,
                                    "visual_type": "animation",
                                    "position": "center_right",
                                    "transition": "pop"
                                },
                                {
                                    "description": "Text Overlay: 'Wait, there's more!'",
                                    "text_span": "But that's only part...",
                                    "timestamp": 0.0,
                                    "duration": 3.0,
                                    "visual_type": "text",
                                    "position": "top_center",
                                    "transition": "fade"
                                }
                            ]
                        }
                    ]
                },
                {
                    "title": "Key Point 2: The Default Mode Network & Dopamine",
                    "content": "Introducing the Default Mode Network (DMN) and its role in mind-wandering and connecting ideas, plus the dopamine boost.",
                    "total_duration": 75,
                    "segments": [
                        {
                            "narration_text": "Okay, let's talk about your brain's 'Default Mode Network', or DMN.",
                            "start_time": 150,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Diagram: Simple brain outline with specific regions highlighted, labeled 'DMN'.",
                                    "text_span": "...'Default Mode Network', or DMN.",
                                    "timestamp": 1.5,
                                    "duration": 3.0,
                                    "visual_type": "diagram",
                                    "position": "center",
                                    "transition": "zoom_in"
                                },
                                {
                                    "description": "Text Overlay: 'DMN: Your Brain's Background App'",
                                    "text_span": "Default Mode Network",
                                    "timestamp": 1.0,
                                    "duration": 3.0,
                                    "visual_type": "text",
                                    "position": "top_center",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Image: A simple toggle switch labeled 'Default'.",
                                    "text_span": "Default Mode",
                                    "timestamp": 2.0,
                                    "duration": 2.0,
                                    "visual_type": "image",
                                    "position": "bottom_left",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "Think of it as what your brain does when you're not focused on the outside world.",
                            "start_time": 155,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Animation: Icons representing external tasks (computer, phone) fading out, leaving a brain icon active.",
                                    "text_span": "...*not* focused on the outside world.",
                                    "timestamp": 1.0,
                                    "duration": 3.0,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Image: A person gazing out a window thoughtfully (minimalist).",
                                    "text_span": "Think of it as...",
                                    "timestamp": 0.0,
                                    "duration": 2.0,
                                    "visual_type": "image",
                                    "position": "center_left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Text Overlay: 'Idle Mode = Active Inside'",
                                    "text_span": "what your brain does when you're not focused",
                                    "timestamp": 1.5,
                                    "duration": 3.0,
                                    "visual_type": "text",
                                    "position": "bottom_center",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "It's active during daydreaming, mind-wandering... and yes, showering!",
                            "start_time": 160,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Image: Cloud icon for 'daydreaming'.",
                                    "text_span": "daydreaming...",
                                    "timestamp": 0.5,
                                    "duration": 1.0,
                                    "visual_type": "image",
                                    "position": "left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Animation: Wavy line icon for 'mind-wandering'.",
                                    "text_span": "mind-wandering...",
                                    "timestamp": 1.5,
                                    "duration": 1.5,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Image: Shower icon.",
                                    "text_span": "...and yes, showering!",
                                    "timestamp": 3.0,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "right",
                                    "transition": "pop"
                                }
                            ]
                        },
                        {
                            "narration_text": "While you're relaxed and distracted, your DMN gets busy.",
                            "start_time": 165,
                            "duration": 4,
                            "visuals": [
                                {
                                    "description": "Image: Person icon relaxing.",
                                    "text_span": "While you're relaxed...",
                                    "timestamp": 0.0,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "center_left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Animation: Brain icon with DMN areas lighting up and becoming active.",
                                    "text_span": "...your DMN gets busy.",
                                    "timestamp": 1.5,
                                    "duration": 2.0,
                                    "visual_type": "animation",
                                    "position": "center_right",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Text Overlay: 'DMN at Work'",
                                    "text_span": "DMN gets busy.",
                                    "timestamp": 2.0,
                                    "duration": 1.5,
                                    "visual_type": "text",
                                    "position": "top_center",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "It starts connecting different parts of your brain, accessing memories and knowledge.",
                            "start_time": 169,
                            "duration": 6,
                            "visuals": [
                                {
                                    "description": "Diagram: Simple brain map showing lines connecting disparate highlighted areas.",
                                    "text_span": "connecting different parts of your brain...",
                                    "timestamp": 0.5,
                                    "duration": 2.5,
                                    "visual_type": "diagram",
                                    "position": "center",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Image: Icon of a filing cabinet or folder (representing memories).",
                                    "text_span": "...accessing memories...",
                                    "timestamp": 3.0,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "center_left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Image: Icon of a book or lightbulb (representing knowledge).",
                                    "text_span": "...and knowledge.",
                                    "timestamp": 4.5,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "center_right",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "Crucially, it connects things that your focused brain might not link together.",
                            "start_time": 175,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Animation: Two unrelated icons (e.g., a key and a cloud) suddenly being linked by a dotted line.",
                                    "text_span": "...connects things that... might not link together.",
                                    "timestamp": 1.0,
                                    "duration": 3.0,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Image: Brain icon with 'Focused' label and blinders on.",
                                    "text_span": "your focused brain",
                                    "timestamp": 0.0,
                                    "duration": 2.0,
                                    "visual_type": "image",
                                    "position": "center_left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Text Overlay: 'Unexpected Links!'",
                                    "text_span": "might not link together.",
                                    "timestamp": 2.5,
                                    "duration": 2.0,
                                    "visual_type": "text",
                                    "position": "bottom_center",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "Think of your focused mind like using a search engine – you type in specific keywords.",
                            "start_time": 180,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Animation: A simple search bar UI with text being typed.",
                                    "text_span": "using a search engine...",
                                    "timestamp": 1.0,
                                    "duration": 2.5,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Image: Magnifying glass icon.",
                                    "text_span": "focused mind",
                                    "timestamp": 0.0,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "center_left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Text Overlay: Specific keywords like 'problem solution formula'.",
                                    "text_span": "type in specific keywords.",
                                    "timestamp": 3.0,
                                    "duration": 2.0,
                                    "visual_type": "text",
                                    "position": "center_right",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "Your DMN is more like browsing randomly, stumbling upon surprising connections.",
                            "start_time": 185,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Animation: Icons popping up randomly on screen, connected by meandering lines.",
                                    "text_span": "browsing randomly, stumbling upon surprising connections.",
                                    "timestamp": 1.0,
                                    "duration": 3.5,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Image: Icon of footprints wandering.",
                                    "text_span": "Your DMN is more like...",
                                    "timestamp": 0.0,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "center_left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Text Overlay: 'Serendipity Engine'",
                                    "text_span": "surprising connections.",
                                    "timestamp": 2.5,
                                    "duration": 2.0,
                                    "visual_type": "text",
                                    "position": "bottom_right",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "This is where insight often comes from – linking seemingly unrelated ideas.",
                            "start_time": 190,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Animation: Two puzzle pieces that don't look like they fit suddenly click together.",
                                    "text_span": "linking seemingly unrelated ideas.",
                                    "timestamp": 1.5,
                                    "duration": 3.0,
                                    "visual_type": "animation",
                                    "position": "center_right",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Image: Lightbulb icon turning on.",
                                    "text_span": "insight often comes from",
                                    "timestamp": 0.0,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "center_left",
                                    "transition": "pop"
                                },
                                {
                                    "description": "Text Overlay: 'Aha!' inside a DMN brain diagram.",
                                    "text_span": "insight",
                                    "timestamp": 1.0,
                                    "duration": 2.5,
                                    "visual_type": "text",
                                    "position": "top_center",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "And there's one more little boost: Dopamine!",
                            "start_time": 195,
                            "duration": 3,
                            "visuals": [
                                {
                                    "description": "Text Overlay: 'Dopamine!' in a bright, cheerful font with sparkles.",
                                    "text_span": "Dopamine!",
                                    "timestamp": 1.0,
                                    "duration": 1.5,
                                    "visual_type": "text",
                                    "position": "center",
                                    "transition": "zoom_in"
                                },
                                {
                                    "description": "Image: A simple '+' sign with an up arrow.",
                                    "text_span": "one more little boost:",
                                    "timestamp": 0.0,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "center_left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Animation: Small dots representing dopamine flowing in a brain icon.",
                                    "text_span": "Dopamine!",
                                    "timestamp": 1.0,
                                    "duration": 2.0,
                                    "visual_type": "animation",
                                    "position": "center_right",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "Showering, especially with warm water, can trigger a small release of this feel-good chemical.",
                            "start_time": 198,
                            "duration": 6,
                            "visuals": [
                                {
                                    "description": "Animation: Water drops turning into small smiley face icons as they fall.",
                                    "text_span": "Showering, especially with warm water...",
                                    "timestamp": 0.0,
                                    "duration": 2.5,
                                    "visual_type": "animation",
                                    "position": "center_left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Diagram: Dopamine chemical structure symbol with a small upward arrow.",
                                    "text_span": "...trigger a small release of this feel-good chemical.",
                                    "timestamp": 2.5,
                                    "duration": 3.0,
                                    "visual_type": "diagram",
                                    "position": "center_right",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Text Overlay: 'Feel Good Boost'",
                                    "text_span": "feel-good chemical.",
                                    "timestamp": 3.5,
                                    "duration": 2.0,
                                    "visual_type": "text",
                                    "position": "bottom_center",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "Dopamine not only improves mood but can also enhance creativity.",
                            "start_time": 204,
                            "duration": 4,
                            "visuals": [
                                {
                                    "description": "Image: Simple smiley face icon.",
                                    "text_span": "improves mood...",
                                    "timestamp": 0.5,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "center_left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Image: Icon representing creativity (palette, lightbulb, pen).",
                                    "text_span": "...enhance creativity.",
                                    "timestamp": 2.0,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "center_right",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Text Overlay: 'Dopamine = Mood + Creativity'",
                                    "text_span": "Dopamine... enhances creativity.",
                                    "timestamp": 1.0,
                                    "duration": 2.5,
                                    "visual_type": "text",
                                    "position": "top_center",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "So you have relaxation (alpha waves), a wandering mind (DMN), and a touch of dopamine.",
                            "start_time": 208,
                            "duration": 6,
                            "visuals": [
                                {
                                    "description": "Image: Alpha wave symbol.",
                                    "text_span": "relaxation (alpha waves)",
                                    "timestamp": 0.5,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Image: DMN brain icon.",
                                    "text_span": "wandering mind (DMN)",
                                    "timestamp": 2.0,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "center",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Image: Dopamine symbol or smiley face.",
                                    "text_span": "touch of dopamine.",
                                    "timestamp": 3.5,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "right",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "It's the perfect storm for those 'Aha!' moments!",
                            "start_time": 214,
                            "duration": 3,
                            "visuals": [
                                {
                                    "description": "Animation: A lightning bolt striking a brain icon, resulting in a lightbulb.",
                                    "text_span": "perfect storm for those 'Aha!' moments!",
                                    "timestamp": 0.5,
                                    "duration": 2.0,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "zoom_in"
                                },
                                {
                                    "description": "Text Overlay: 'Aha!'",
                                    "text_span": "'Aha!' moments!",
                                    "timestamp": 1.0,
                                    "duration": 1.5,
                                    "visual_type": "text",
                                    "position": "top_center",
                                    "transition": "pop"
                                },
                                {
                                    "description": "Image: A checkmark icon over the combined symbols from previous segment.",
                                    "text_span": "It's the perfect storm",
                                    "timestamp": 0.0,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "center_left",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "Pretty cool how your brain uses that downtime, right?",
                            "start_time": 217,
                            "duration": 4,
                            "visuals": [
                                {
                                    "description": "Image: Brain icon giving a thumbs-up.",
                                    "text_span": "Pretty cool how your brain...",
                                    "timestamp": 0.0,
                                    "duration": 2.0,
                                    "visual_type": "image",
                                    "position": "center_left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Image: A simple 'pause' or 'sleep mode' icon.",
                                    "text_span": "...uses that downtime...",
                                    "timestamp": 2.0,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "center_right",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Text Overlay: 'Smart Downtime!'",
                                    "text_span": "uses that downtime, right?",
                                    "timestamp": 1.5,
                                    "duration": 2.0,
                                    "visual_type": "text",
                                    "position": "bottom_center",
                                    "transition": "fade"
                                }
                            ]
                        }
                    ]
                },
                {
                    "title": "Conclusion: Embrace the Wander",
                    "content": "Summarizing the key factors and encouraging you to find similar moments for creativity.",
                    "total_duration": 75,
                    "segments": [
                        {
                            "narration_text": "So, there you have it! The mystery of the shower epiphany isn't so mysterious after all.",
                            "start_time": 225,
                            "duration": 6,
                            "visuals": [
                                {
                                    "description": "Animation: A question mark turning into an exclamation point.",
                                    "text_span": "...mystery... isn't so mysterious",
                                    "timestamp": 1.0,
                                    "duration": 2.5,
                                    "visual_type": "animation",
                                    "position": "center",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Image: Shower icon with a checkmark next to it.",
                                    "text_span": "shower epiphany",
                                    "timestamp": 0.0,
                                    "duration": 2.0,
                                    "visual_type": "image",
                                    "position": "center_left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Text Overlay: 'Mystery Solved!'",
                                    "text_span": "isn't so mysterious after all.",
                                    "timestamp": 3.5,
                                    "duration": 2.0,
                                    "visual_type": "text",
                                    "position": "bottom_center",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "It's a combination of being relaxed, letting your mind wander freely...",
                            "start_time": 231,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Image: Relaxed person icon.",
                                    "text_span": "being relaxed...",
                                    "timestamp": 0.5,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "center_left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Image: Wandering footprints icon.",
                                    "text_span": "...letting your mind wander freely...",
                                    "timestamp": 2.0,
                                    "duration": 2.0,
                                    "visual_type": "image",
                                    "position": "center_right",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Text Overlay: 'Relax + Wander'",
                                    "text_span": "combination of being relaxed, letting your mind wander",
                                    "timestamp": 1.0,
                                    "duration": 3.0,
                                    "visual_type": "text",
                                    "position": "top_center",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "...thanks to those alpha waves and your amazing Default Mode Network.",
                            "start_time": 236,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Image: Alpha wave symbol.",
                                    "text_span": "...alpha waves...",
                                    "timestamp": 1.0,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "center_left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Image: DMN brain icon.",
                                    "text_span": "...Default Mode Network.",
                                    "timestamp": 2.5,
                                    "duration": 2.0,
                                    "visual_type": "image",
                                    "position": "center_right",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Text Overlay: 'Your Brain's Secret Weapon'",
                                    "text_span": "amazing Default Mode Network.",
                                    "timestamp": 2.0,
                                    "duration": 2.5,
                                    "visual_type": "text",
                                    "position": "bottom_center",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "Plus that little dopamine kick doesn't hurt either!",
                            "start_time": 241,
                            "duration": 3,
                            "visuals": [
                                {
                                    "description": "Image: Dopamine symbol with a small sparkle.",
                                    "text_span": "dopamine kick...",
                                    "timestamp": 0.5,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "center",
                                    "transition": "pop"
                                },
                                {
                                    "description": "Image: Thumbs up icon.",
                                    "text_span": "...doesn't hurt either!",
                                    "timestamp": 1.5,
                                    "duration": 1.0,
                                    "visual_type": "image",
                                    "position": "center_right",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Text Overlay: '+Dopamine!'",
                                    "text_span": "dopamine kick",
                                    "timestamp": 0.5,
                                    "duration": 2.0,
                                    "visual_type": "text",
                                    "position": "top_left",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "The key ingredients are solitude, relaxation, and a lack of focused task.",
                            "start_time": 244,
                            "duration": 6,
                            "visuals": [
                                {
                                    "description": "Image: Icon for solitude (single person).",
                                    "text_span": "solitude,",
                                    "timestamp": 1.0,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Image: Icon for relaxation (zen symbol).",
                                    "text_span": "relaxation,",
                                    "timestamp": 2.5,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "center",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Image: Icon for 'no task' (crossed-out checklist).",
                                    "text_span": "lack of focused task.",
                                    "timestamp": 4.0,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "right",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "Think about it – you probably get good ideas in other similar situations too.",
                            "start_time": 250,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Animation: A thought bubble appearing above a simple head icon.",
                                    "text_span": "Think about it...",
                                    "timestamp": 0.0,
                                    "duration": 2.0,
                                    "visual_type": "animation",
                                    "position": "center_left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Text Overlay: 'Where Else?' followed by a question mark.",
                                    "text_span": "other similar situations too.",
                                    "timestamp": 2.0,
                                    "duration": 2.5,
                                    "visual_type": "text",
                                    "position": "center_right",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Image: Lightbulb icon appearing multiple times.",
                                    "text_span": "good ideas",
                                    "timestamp": 1.5,
                                    "duration": 2.0,
                                    "visual_type": "image",
                                    "position": "center",
                                    "transition": "pop"
                                }
                            ]
                        },
                        {
                            "narration_text": "Like when you're going for a walk, especially in nature?",
                            "start_time": 255,
                            "duration": 4,
                            "visuals": [
                                {
                                    "description": "Image: Minimalist icon of footprints on a path.",
                                    "text_span": "going for a walk...",
                                    "timestamp": 0.5,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "center_left",
                                    "transition": "slide_right"
                                },
                                {
                                    "description": "Image: Simple tree or leaf icon.",
                                    "text_span": "...especially in nature?",
                                    "timestamp": 2.0,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "center_right",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Text Overlay: 'Walking Thoughts'",
                                    "text_span": "going for a walk",
                                    "timestamp": 1.0,
                                    "duration": 2.0,
                                    "visual_type": "text",
                                    "position": "bottom_center",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "Or maybe while doing repetitive chores like washing dishes or folding laundry?",
                            "start_time": 259,
                            "duration": 6,
                            "visuals": [
                                {
                                    "description": "Image: Icon of hands washing a plate.",
                                    "text_span": "washing dishes...",
                                    "timestamp": 1.0,
                                    "duration": 2.0,
                                    "visual_type": "image",
                                    "position": "center_left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Image: Icon of neatly folded shirts.",
                                    "text_span": "...or folding laundry?",
                                    "timestamp": 3.0,
                                    "duration": 2.0,
                                    "visual_type": "image",
                                    "position": "center_right",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Animation: A circular arrow indicating repetition.",
                                    "text_span": "repetitive chores",
                                    "timestamp": 0.0,
                                    "duration": 2.0,
                                    "visual_type": "animation",
                                    "position": "top_center",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "Even just before drifting off to sleep sometimes, right?",
                            "start_time": 265,
                            "duration": 4,
                            "visuals": [
                                {
                                    "description": "Image: Icon of a person in bed, eyes closing.",
                                    "text_span": "drifting off to sleep...",
                                    "timestamp": 0.5,
                                    "duration": 2.0,
                                    "visual_type": "image",
                                    "position": "center",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Animation: Zzz symbols floating upwards.",
                                    "text_span": "drifting off to sleep",
                                    "timestamp": 1.0,
                                    "duration": 2.0,
                                    "visual_type": "animation",
                                    "position": "top_right",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Text Overlay: 'Bedtime Brainwaves'",
                                    "text_span": "drifting off to sleep",
                                    "timestamp": 1.5,
                                    "duration": 2.0,
                                    "visual_type": "text",
                                    "position": "bottom_center",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "These are all moments when your brain gets a chance to switch off the focus and turn on the DMN.",
                            "start_time": 269,
                            "duration": 6,
                            "visuals": [
                                {
                                    "description": "Animation: Focus icon (spotlight) switching off.",
                                    "text_span": "switch off the focus...",
                                    "timestamp": 1.0,
                                    "duration": 2.0,
                                    "visual_type": "animation",
                                    "position": "center_left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Animation: DMN brain icon lighting up.",
                                    "text_span": "...turn on the DMN.",
                                    "timestamp": 3.0,
                                    "duration": 2.0,
                                    "visual_type": "animation",
                                    "position": "center_right",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Diagram: Simple flow chart: Relax -> Focus OFF -> DMN ON.",
                                    "text_span": "switch off the focus and turn on the DMN.",
                                    "timestamp": 1.5,
                                    "duration": 3.0,
                                    "visual_type": "diagram",
                                    "position": "bottom_center",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "So, the takeaway? Don't underestimate the power of letting your mind wander.",
                            "start_time": 275,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Text Overlay: 'Takeaway:' in bold.",
                                    "text_span": "So, the takeaway?",
                                    "timestamp": 0.0,
                                    "duration": 1.5,
                                    "visual_type": "text",
                                    "position": "top_left",
                                    "transition": "slide_right"
                                },
                                {
                                    "description": "Image: A brain icon with little wandering paths coming out of it.",
                                    "text_span": "letting your mind wander.",
                                    "timestamp": 2.0,
                                    "duration": 2.5,
                                    "visual_type": "image",
                                    "position": "center",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Animation: A 'power' symbol (like on electronics) pulsing gently.",
                                    "text_span": "power of letting your mind wander.",
                                    "timestamp": 1.5,
                                    "duration": 3.0,
                                    "visual_type": "animation",
                                    "position": "center_right",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "Embrace those moments of quiet solitude, whether it's in the shower or elsewhere.",
                            "start_time": 280,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Image: Hands gently cupped, as if holding something precious.",
                                    "text_span": "Embrace those moments...",
                                    "timestamp": 0.0,
                                    "duration": 2.0,
                                    "visual_type": "image",
                                    "position": "center_left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Image: Icons representing shower, walking, relaxing.",
                                    "text_span": "...shower or elsewhere.",
                                    "timestamp": 2.0,
                                    "duration": 2.5,
                                    "visual_type": "image",
                                    "position": "center_right",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Text Overlay: 'Value Your Downtime'",
                                    "text_span": "moments of quiet solitude",
                                    "timestamp": 1.0,
                                    "duration": 3.0,
                                    "visual_type": "text",
                                    "position": "bottom_center",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "You're not just relaxing; you might be paving the way for your next great idea.",
                            "start_time": 285,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Image: Simple 'zen' icon.",
                                    "text_span": "You're not just relaxing...",
                                    "timestamp": 0.0,
                                    "duration": 1.5,
                                    "visual_type": "image",
                                    "position": "center_left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Animation: A simple path being drawn towards a bright lightbulb icon.",
                                    "text_span": "...paving the way for your next great idea.",
                                    "timestamp": 1.5,
                                    "duration": 3.0,
                                    "visual_type": "animation",
                                    "position": "center_right",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Text Overlay: 'Relax = Idea Prep'",
                                    "text_span": "paving the way",
                                    "timestamp": 2.0,
                                    "duration": 2.5,
                                    "visual_type": "text",
                                    "position": "top_center",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "So next time you're showering, enjoy the peace... and keep a mental notepad ready!",
                            "start_time": 290,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Image: Shower head with gentle water flow.",
                                    "text_span": "next time you're showering...",
                                    "timestamp": 0.0,
                                    "duration": 2.0,
                                    "visual_type": "image",
                                    "position": "center_left",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Animation: A simple notepad icon appearing next to a brain icon.",
                                    "text_span": "...keep a mental notepad ready!",
                                    "timestamp": 2.5,
                                    "duration": 2.0,
                                    "visual_type": "animation",
                                    "position": "center_right",
                                    "transition": "pop"
                                },
                                {
                                    "description": "Text Overlay: 'Happy Shower Thinking!'",
                                    "text_span": "enjoy the peace...",
                                    "timestamp": 1.5,
                                    "duration": 3.0,
                                    "visual_type": "text",
                                    "position": "bottom_center",
                                    "transition": "fade"
                                }
                            ]
                        },
                        {
                            "narration_text": "Thanks for watching! Hope you found that interesting. See you next time!",
                            "start_time": 295,
                            "duration": 5,
                            "visuals": [
                                {
                                    "description": "Text Overlay: 'Thanks for watching!' with a simple smiley face.",
                                    "text_span": "Thanks for watching!",
                                    "timestamp": 0.0,
                                    "duration": 2.0,
                                    "visual_type": "text",
                                    "position": "center",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Animation: A simple waving hand icon.",
                                    "text_span": "See you next time!",
                                    "timestamp": 3.0,
                                    "duration": 1.5,
                                    "visual_type": "animation",
                                    "position": "center_right",
                                    "transition": "fade"
                                },
                                {
                                    "description": "Image: A lightbulb icon that winks.",
                                    "text_span": "Hope you found that interesting.",
                                    "timestamp": 1.5,
                                    "duration": 2.0,
                                    "visual_type": "image",
                                    "position": "center_left",
                                    "transition": "fade"
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
