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
        "title": "Is AI Making You Dumber? (And How to Keep Your Brain Sharp!)",
        "description": "A friendly, personal chat about how relying too much on AI might be dulling your thinking skills, with practical tips inspired by real research and examples (like GPS brain drain!) on how you can use AI smartly without losing your edge.",
        "total_duration": 616,
        "sections": [
            {
            "title": "Introduction: Hey, Is This Thing On... Your Brain?",
            "content": "Setting the stage, personally addressing you, the viewer. Introducing the core question: Is the AI you use daily subtly making your thinking a bit... lazy? We'll explore this, drawing inspiration from how technology has always changed us, and offer ways to stay sharp.",
            "total_duration": 68,
            "segments": [
                {
                "narration_text": "Hey there. Yeah, you! Leaning into the screen. Ever feel like your phone knows what you want before you do?",
                "start_time": 0,
                "duration": 6,
                "visuals": [
                    {
                    "description": "Friendly host (animated or real) looking directly at the camera, waving slightly.",
                    "timestamp": 0,
                    "duration": 2,
                    "visual_type": "image",
                    "position": "full",
                    "transition": "fade",
                    "text_span": "Hey there. Yeah, you!"
                    },
                    {
                    "description": "Close-up on a smartphone screen showing a personalized notification popping up.",
                    "timestamp": 2,
                    "duration": 2,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "zoom",
                    "text_span": "knows what you want"
                    },
                    {
                    "description": "Animation of a question mark appearing over a stylized human head.",
                    "timestamp": 4,
                    "duration": 2,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "before you do?"
                    }
                ]
                },
                {
                "narration_text": "Or maybe you've asked an AI to whip up an email, and thought... 'Wow, that was easy. Maybe too easy?'",
                "start_time": 6,
                "duration": 6,
                "visuals": [
                    {
                    "description": "Split screen: Left shows someone typing an email manually (looking stressed). Right shows an AI interface generating an email instantly (looking effortless).",
                    "timestamp": 0,
                    "duration": 3,
                    "visual_type": "image",
                    "position": "full",
                    "transition": "slide",
                    "text_span": "asked an AI to whip up an email"
                    },
                    {
                    "description": "Close-up on the generated email text, looking perfectly formatted.",
                    "timestamp": 3,
                    "duration": 1.5,
                    "visual_type": "text",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "'Wow, that was easy.'"
                    },
                    {
                    "description": "Thought bubble appearing next to the AI-generated email with slightly suspicious eyes looking at it.",
                    "timestamp": 4.5,
                    "duration": 1.5,
                    "visual_type": "animation",
                    "position": "right",
                    "transition": "fade",
                    "text_span": "Maybe too easy?'"
                    }
                ]
                },
                {
                "narration_text": "It's everywhere now, right? AI is baked into search, your writing tools, maybe even your fridge!",
                "start_time": 12,
                "duration": 5,
                "visuals": [
                    {
                    "description": "Montage of quick cuts showing AI icons integrated into familiar apps (search bar, word processor, social media).",
                    "timestamp": 0,
                    "duration": 3,
                    "visual_type": "animation",
                    "position": "full",
                    "transition": "slide",
                    "text_span": "It's everywhere now, right?"
                    },
                    {
                    "description": "Humorous image of a smart fridge displaying a complex AI-generated grocery list.",
                    "timestamp": 3,
                    "duration": 2,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "zoom",
                    "text_span": "maybe even your fridge!"
                    }
                ]
                },
                {
                "narration_text": "It’s doing amazing things, no doubt. Curing diseases, solving complex problems... seriously cool stuff.",
                "start_time": 17,
                "duration": 6,
                "visuals": [
                    {
                    "description": "Visual of scientists looking excitedly at complex molecular models on a screen, with an AI icon subtly present.",
                    "timestamp": 0,
                    "duration": 3,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "Curing diseases, solving complex problems"
                    },
                    {
                    "description": "Animated graphic showing interconnected nodes representing complex problem-solving.",
                    "timestamp": 3,
                    "duration": 1.5,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade"
                    },
                    {
                    "description": "Text overlay: 'Seriously Cool Stuff!' in a futuristic font.",
                    "timestamp": 4.5,
                    "duration": 1.5,
                    "visual_type": "text",
                    "position": "center",
                    "transition": "pop"
                    }
                ]
                },
                {
                "narration_text": "But we're talking about the everyday AI. The stuff you and I use constantly. The 'AI slop', some call it.",
                "start_time": 23,
                "duration": 6,
                "visuals": [
                    {
                    "description": "Shift in tone: Visual contrasts the 'cool science AI' with everyday AI use - someone casually asking a chatbot a simple question.",
                    "timestamp": 0,
                    "duration": 3,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "wipe",
                    "text_span": "the everyday AI"
                    },
                    {
                    "description": "Close up on a phone screen showing a generic chatbot interface.",
                    "timestamp": 3,
                    "duration": 1.5,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "zoom"
                    },
                    {
                    "description": "Text overlay: 'AI Slop?' appearing with a slightly messy, 'glitchy' effect.",
                    "timestamp": 4.5,
                    "duration": 1.5,
                    "visual_type": "text",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "The 'AI slop', some call it."
                    }
                ]
                },
                {
                "narration_text": "Could overusing this convenience actually be... well, making us a bit duller? Less reliant on our own smarts?",
                "start_time": 29,
                "duration": 6,
                "visuals": [
                    {
                    "description": "Animation of a brain character looking relaxed, maybe lounging in a chair while a small robot does its work.",
                    "timestamp": 0,
                    "duration": 3,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "overusing this convenience"
                    },
                    {
                    "description": "Stylized graphic showing a 'brain power' meter decreasing.",
                    "timestamp": 3,
                    "duration": 1.5,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "making us a bit duller?"
                    },
                    {
                    "description": "A hand hesitantly reaching for its own head, as if checking if the brain is still there.",
                    "timestamp": 4.5,
                    "duration": 1.5,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "Less reliant on our own smarts?"
                    }
                ]
                },
                {
                "narration_text": "That's the big question we're tackling today. Think of it like a friendly chat about your brain on AI.",
                "start_time": 35,
                "duration": 5,
                "visuals": [
                    {
                    "description": "Main title card reappears briefly: 'Is AI Making You Dumber?'",
                    "timestamp": 0,
                    "duration": 2,
                    "visual_type": "text",
                    "position": "center",
                    "transition": "fade"
                    },
                    {
                    "description": "Graphic of a human brain with digital circuits subtly overlaid.",
                    "timestamp": 2,
                    "duration": 3,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "zoom",
                    "text_span": "your brain on AI."
                    }
                ]
                },
                {
                "narration_text": "We'll look at some surprising ways tech affects your thinking – ways you might not even notice.",
                "start_time": 40,
                "duration": 5,
                "visuals": [
                    {
                    "description": "Animation of subtle digital waves emanating from a phone towards a person's head.",
                    "timestamp": 0,
                    "duration": 2.5,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "surprising ways tech affects your thinking"
                    },
                    {
                    "description": "Close up of a person's eyes, looking slightly unfocused or glazed over while scrolling.",
                    "timestamp": 2.5,
                    "duration": 2.5,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "ways you might not even notice."
                    }
                ]
                },
                {
                "narration_text": "Think GPS messing with your sense of direction, but potentially on a much bigger scale.",
                "start_time": 45,
                "duration": 5,
                "visuals": [
                    {
                    "description": "Iconic GPS map interface shown on a phone screen.",
                    "timestamp": 0,
                    "duration": 2,
                    "visual_type": "image",
                    "position": "left",
                    "transition": "slide"
                    },
                    {
                    "description": "Animation showing a brain's 'navigation center' dimming or shrinking slightly.",
                    "timestamp": 2,
                    "duration": 3,
                    "visual_type": "animation",
                    "position": "right",
                    "transition": "fade",
                    "text_span": "GPS messing with your sense of direction"
                    }
                ]
                },
                {
                "narration_text": "We'll dig into why relying too much on AI for answers might weaken your critical thinking muscles.",
                "start_time": 50,
                "duration": 6,
                "visuals": [
                    {
                    "description": "Stylized image of someone spoon-feeding information from a tablet into a passive-looking brain.",
                    "timestamp": 0,
                    "duration": 3,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "relying too much on AI for answers"
                    },
                    {
                    "description": "Animation of a muscular brain flexing, then slowly deflating like a balloon.",
                    "timestamp": 3,
                    "duration": 3,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "weaken your critical thinking muscles."
                    }
                ]
                },
                {
                "narration_text": "And don't worry, this isn't all doom and gloom! I promise.",
                "start_time": 56,
                "duration": 3,
                "visuals": [
                    {
                    "description": "Split screen: Left side shows dark, stormy clouds. Right side shows sunshine breaking through.",
                    "timestamp": 0,
                    "duration": 1.5,
                    "visual_type": "image",
                    "position": "full",
                    "transition": "wipe"
                    },
                    {
                    "description": "Host smiling reassuringly at the camera.",
                    "timestamp": 1.5,
                    "duration": 1.5,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "isn't all doom and gloom! I promise."
                    }
                ]
                },
                {
                "narration_text": "Stick around, because at the end, we'll talk about practical ways you can fight back.",
                "start_time": 59,
                "duration": 4,
                "visuals": [
                    {
                    "description": "Graphic of a toolbox opening, revealing tools labeled 'Critical Thinking', 'Fact-Checking', 'Mindful Use'.",
                    "timestamp": 0,
                    "duration": 2.5,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "zoom",
                    "text_span": "practical ways you can fight back."
                    },
                    {
                    "description": "Text overlay: 'Stay Sharp!'",
                    "timestamp": 2.5,
                    "duration": 1.5,
                    "visual_type": "text",
                    "position": "center",
                    "transition": "pop"
                    }
                ]
                },
                {
                "narration_text": "How to use AI as the amazing tool it can be, without letting it turn your brain to mush.",
                "start_time": 63,
                "duration": 5,
                "visuals": [
                    {
                    "description": "Animation of AI depicted as a helpful co-pilot or assistant, handing tools to a person who is actively working.",
                    "timestamp": 0,
                    "duration": 3,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "use AI as the amazing tool it can be"
                    },
                    {
                    "description": "Humorous image of a brain represented as a bowl of oatmeal.",
                    "timestamp": 3,
                    "duration": 2,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "without letting it turn your brain to mush."
                    }
                ]
                }
            ]
            },
            {
            "title": "The Convenience Trap: Remember Maps?",
            "content": "Using the familiar example of GPS, we explore how convenience technologies can subtly weaken specific cognitive skills, like spatial memory. This sets the groundwork for understanding AI's potentially broader impact.",
            "total_duration": 92,
            "segments": [
                {
                "narration_text": "Okay, let's start with something familiar. Remember life before smartphones? Specifically, before GPS?",
                "start_time": 68,
                "duration": 6,
                "visuals": [
                    {
                    "description": "Sepia-toned image of someone unfolding a large, complicated paper map.",
                    "timestamp": 0,
                    "duration": 3,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "Remember life before smartphones?"
                    },
                    {
                    "description": "Split screen: Paper map on left, modern GPS interface on right.",
                    "timestamp": 3,
                    "duration": 3,
                    "visual_type": "image",
                    "position": "full",
                    "transition": "slide",
                    "text_span": "Specifically, before GPS?"
                    }
                ]
                },
                {
                "narration_text": "You had to actually look at street signs, maybe even ask for directions! Wild, I know.",
                "start_time": 74,
                "duration": 5,
                "visuals": [
                    {
                    "description": "Close-up shot of classic green street signs at an intersection.",
                    "timestamp": 0,
                    "duration": 2,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "zoom"
                    },
                    {
                    "description": "Simple animation of a person politely asking another person for directions on a street corner.",
                    "timestamp": 2,
                    "duration": 2,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "ask for directions!"
                    },
                    {
                    "description": "Host making a comical 'mind blown' gesture.",
                    "timestamp": 4,
                    "duration": 1,
                    "visual_type": "image",
                    "position": "right",
                    "transition": "pop",
                    "text_span": "Wild, I know."
                    }
                ]
                },
                {
                "narration_text": "Well, studies, like one from 2020, found something interesting about relying heavily on GPS.",
                "start_time": 79,
                "duration": 5,
                "visuals": [
                    {
                    "description": "Text graphic: 'Study: 2020' with a magnifying glass icon.",
                    "timestamp": 0,
                    "duration": 2.5,
                    "visual_type": "text",
                    "position": "left",
                    "transition": "slide"
                    },
                    {
                    "description": "Image of a person blindly following GPS directions on their phone, oblivious to surroundings.",
                    "timestamp": 2.5,
                    "duration": 2.5,
                    "visual_type": "image",
                    "position": "right",
                    "transition": "fade",
                    "text_span": "relying heavily on GPS."
                    }
                ]
                },
                {
                "narration_text": "It seems that constant use can actually weaken your spatial memory. Your internal compass gets a bit rusty.",
                "start_time": 84,
                "duration": 6,
                "visuals": [
                    {
                    "description": "Animation showing a brain map, with the 'spatial navigation' area highlighted and then slightly fading or shrinking.",
                    "timestamp": 0,
                    "duration": 3,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "weaken your spatial memory."
                    },
                    {
                    "description": "Visual of a compass needle spinning erratically or looking rusty.",
                    "timestamp": 3,
                    "duration": 3,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "zoom",
                    "text_span": "Your internal compass gets a bit rusty."
                    }
                ]
                },
                {
                "narration_text": "Funny thing is, the people in the study whose navigation skills did decline often didn't even realize it.",
                "start_time": 90,
                "duration": 6,
                "visuals": [
                    {
                    "description": "Image of a person looking confidently in the wrong direction, despite a GPS clearly pointing the other way.",
                    "timestamp": 0,
                    "duration": 3,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "navigation skills did decline"
                    },
                    {
                    "description": "Thought bubble above the person with a shrug emoji or 'I'm great at directions!' text.",
                    "timestamp": 3,
                    "duration": 3,
                    "visual_type": "animation",
                    "position": "right",
                    "transition": "pop",
                    "text_span": "often didn't even realize it."
                    }
                ]
                },
                {
                "narration_text": "They still thought they had a great sense of direction, even when the data showed otherwise.",
                "start_time": 96,
                "duration": 5,
                "visuals": [
                    {
                    "description": "Graphic showing a 'Self-Perception' meter (High) next to an 'Actual Skill' meter (Low).",
                    "timestamp": 0,
                    "duration": 3,
                    "visual_type": "diagram",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "great sense of direction... data showed otherwise."
                    },
                    {
                    "description": "Simple chart showing a declining line graph labeled 'Spatial Memory Test Scores'.",
                    "timestamp": 3,
                    "duration": 2,
                    "visual_type": "diagram",
                    "position": "center",
                    "transition": "fade"
                    }
                ]
                },
                {
                "narration_text": "It's that classic trade-off, isn't it? Convenience often comes with a hidden cost.",
                "start_time": 101,
                "duration": 5,
                "visuals": [
                    {
                    "description": "Image of a scale balancing 'Convenience' (high) and 'Cognitive Skill' (low).",
                    "timestamp": 0,
                    "duration": 2.5,
                    "visual_type": "diagram",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "classic trade-off"
                    },
                    {
                    "description": "Visual of a price tag hanging off a smartphone displaying a map.",
                    "timestamp": 2.5,
                    "duration": 2.5,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "zoom",
                    "text_span": "hidden cost."
                    }
                ]
                },
                {
                "narration_text": "And remember, GPS is relatively simple tech. It just follows instructions.",
                "start_time": 106,
                "duration": 4,
                "visuals": [
                    {
                    "description": "Close-up of a GPS screen showing a simple route line.",
                    "timestamp": 0,
                    "duration": 2,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "fade"
                    },
                    {
                    "description": "Animation of simple directional arrows moving along a path.",
                    "timestamp": 2,
                    "duration": 2,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "just follows instructions."
                    }
                ]
                },
                {
                "narration_text": "It's not really 'thinking' or generating new information like the AI we're talking about.",
                "start_time": 110,
                "duration": 5,
                "visuals": [
                    {
                    "description": "Comparison visual: Left side shows simple GPS arrow. Right side shows complex AI neural network graphic.",
                    "timestamp": 0,
                    "duration": 2.5,
                    "visual_type": "image",
                    "position": "full",
                    "transition": "slide"
                    },
                    {
                    "description": "Animation of an AI icon with a thinking gear animation inside it.",
                    "timestamp": 2.5,
                    "duration": 2.5,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "generating new information"
                    }
                ]
                },
                {
                "narration_text": "So, if simple GPS can subtly change how your brain works...",
                "start_time": 115,
                "duration": 4,
                "visuals": [
                    {
                    "description": "Recap visual: GPS icon pointing towards a brain with a small question mark.",
                    "timestamp": 0,
                    "duration": 2,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "fade"
                    },
                    {
                    "description": "Ellipsis (...) animation suggesting anticipation.",
                    "timestamp": 2,
                    "duration": 2,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade"
                    }
                ]
                },
                {
                "narration_text": "What might happen when you start outsourcing actual thinking tasks to AI?",
                "start_time": 119,
                "duration": 5,
                "visuals": [
                    {
                    "description": "Animation of a brain handing over tasks like 'Problem Solving', 'Writing', 'Decision Making' to an AI robot.",
                    "timestamp": 0,
                    "duration": 3,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "outsourcing actual thinking tasks"
                    },
                    {
                    "description": "Close up on the AI robot juggling these complex tasks.",
                    "timestamp": 3,
                    "duration": 2,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "zoom"
                    }
                ]
                },
                {
                "narration_text": "Things like writing, summarizing information, even generating creative ideas?",
                "start_time": 124,
                "duration": 5,
                "visuals": [
                    {
                    "description": "Icons representing Writing (pen), Summarizing (document with arrow), Ideas (lightbulb) being processed by an AI.",
                    "timestamp": 0,
                    "duration": 2.5,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade"
                    },
                    {
                    "description": "Quick cuts showing AI generating text, a summary, and maybe some abstract art.",
                    "timestamp": 2.5,
                    "duration": 2.5,
                    "visual_type": "image",
                    "position": "full",
                    "transition": "slide"
                    }
                ]
                },
                {
                "narration_text": "This isn't just about finding your way around town anymore. This feels... different.",
                "start_time": 129,
                "duration": 5,
                "visuals": [
                    {
                    "description": "Split screen fades: GPS navigation vs. AI writing an essay.",
                    "timestamp": 0,
                    "duration": 3,
                    "visual_type": "image",
                    "position": "full",
                    "transition": "fade"
                    },
                    {
                    "description": "Visual of a brain looking slightly concerned, gears turning slowly.",
                    "timestamp": 3,
                    "duration": 2,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "This feels... different."
                    }
                ]
                },
                {
                "narration_text": "Let's look at what happens when AI steps in to 'help' with tasks that normally build your skills.",
                "start_time": 134,
                "duration": 6,
                "visuals": [
                    {
                    "description": "Animation of building blocks labeled 'Writing', 'Analysis', 'Problem Solving' being constructed by a brain.",
                    "timestamp": 0,
                    "duration": 3,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "tasks that normally build your skills."
                    },
                    {
                    "description": "An AI hand comes in and swiftly builds the tower, pushing the brain character aside.",
                    "timestamp": 3,
                    "duration": 3,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "slide",
                    "text_span": "when AI steps in to 'help'"
                    }
                ]
                }
            ]
            },
            {
            "title": "AI Doing the Homework: Skills vs. Tools",
            "content": "Exploring the impact of AI writing tools on skill development, using the professor's anecdote. Discussing the concept of 'mental atrophy' – if you don't use your cognitive muscles, they might weaken.",
            "total_duration": 120,
            "segments": [
                {
                "narration_text": "Think back to school, or maybe your job now. Remember learning to write well? It takes practice, right?",
                "start_time": 160,
                "duration": 6,
                "visuals": [
                    {
                    "description": "Image of a student chewing on a pen, struggling with a blank page.",
                    "timestamp": 0,
                    "duration": 2,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "fade"
                    },
                    {
                    "description": "Time-lapse animation showing messy drafts turning into a polished essay.",
                    "timestamp": 2,
                    "duration": 2.5,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "learning to write well?"
                    },
                    {
                    "description": "Graphic of a 'Practice Makes Perfect' sign.",
                    "timestamp": 4.5,
                    "duration": 1.5,
                    "visual_type": "text",
                    "position": "center",
                    "transition": "pop",
                    "text_span": "It takes practice, right?"
                    }
                ]
                },
                {
                "narration_text": "There's this story about a professor, David Rafo. A few years back, he noticed something weird.",
                "start_time": 166,
                "duration": 5,
                "visuals": [
                    {
                    "description": "Stylized portrait of a thoughtful-looking professor (generic).",
                    "timestamp": 0,
                    "duration": 2.5,
                    "visual_type": "image",
                    "position": "left",
                    "transition": "slide",
                    "text_span": "professor, David Rafo"
                    },
                    {
                    "description": "Animation of the professor looking puzzled at a stack of student papers.",
                    "timestamp": 2.5,
                    "duration": 2.5,
                    "visual_type": "animation",
                    "position": "right",
                    "transition": "fade",
                    "text_span": "noticed something weird."
                    }
                ]
                },
                {
                "narration_text": "His students' writing, which hadn't been great, suddenly got way better. Almost... unnaturally good.",
                "start_time": 171,
                "duration": 6,
                "visuals": [
                    {
                    "description": "Split screen: Left shows a poorly written paper with red marks. Right shows a perfectly typed, eloquent paper.",
                    "timestamp": 0,
                    "duration": 3,
                    "visual_type": "image",
                    "position": "full",
                    "transition": "wipe",
                    "text_span": "suddenly got way better."
                    },
                    {
                    "description": "Close-up on the 'unnaturally good' paper, maybe with a faint digital glow.",
                    "timestamp": 3,
                    "duration": 1.5,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "zoom"
                    },
                    {
                    "description": "Professor character raising an eyebrow suspiciously.",
                    "timestamp": 4.5,
                    "duration": 1.5,
                    "visual_type": "animation",
                    "position": "right",
                    "transition": "fade",
                    "text_span": "unnaturally good."
                    }
                ]
                },
                {
                "narration_text": "He smelled a rat, as they say. He asked them, and yep - they were using AI writing tools.",
                "start_time": 177,
                "duration": 5,
                "visuals": [
                    {
                    "description": "Humorous animation of a cartoon rat holding a tiny laptop, sneaking away from the papers.",
                    "timestamp": 0,
                    "duration": 2.5,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "smelled a rat"
                    },
                    {
                    "description": "Visual representation of students admitting (perhaps sheepishly) with AI icons floating near them.",
                    "timestamp": 2.5,
                    "duration": 2.5,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "using AI writing tools."
                    }
                ]
                },
                {
                "narration_text": "His realization was key: 'It was the tools that improved their writing, not their writing skills.'",
                "start_time": 182,
                "duration": 6,
                "visuals": [
                    {
                    "description": "Text overlay emphasizing the quote: 'It was the TOOLS... not their SKILLS.'",
                    "timestamp": 0,
                    "duration": 3,
                    "visual_type": "text",
                    "position": "center",
                    "transition": "fade"
                    },
                    {
                    "description": "Split screen: Left shows AI tool icon. Right shows a brain icon with 'Writing Skill' below it, looking less developed.",
                    "timestamp": 3,
                    "duration": 3,
                    "visual_type": "diagram",
                    "position": "full",
                    "transition": "slide"
                    }
                ]
                },
                {
                "narration_text": "See the difference? The AI could produce good text, but the students weren't learning how to do it themselves.",
                "start_time": 188,
                "duration": 6,
                "visuals": [
                    {
                    "description": "Animation of AI generating text like a factory production line.",
                    "timestamp": 0,
                    "duration": 3,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "AI could produce good text"
                    },
                    {
                    "description": "Visual of a student passively watching the AI work, not engaging.",
                    "timestamp": 3,
                    "duration": 3,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "students weren't learning"
                    }
                ]
                },
                {
                "narration_text": "Professor Rafo wasn't totally against AI, he saw its efficiency. But he had a warning.",
                "start_time": 194,
                "duration": 5,
                "visuals": [
                    {
                    "description": "Professor character nodding thoughtfully, acknowledging AI's speed.",
                    "timestamp": 0,
                    "duration": 2.5,
                    "visual_type": "animation",
                    "position": "left",
                    "transition": "fade",
                    "text_span": "saw its efficiency."
                    },
                    {
                    "description": "A yellow warning sign icon appearing next to the professor.",
                    "timestamp": 2.5,
                    "duration": 2.5,
                    "visual_type": "image",
                    "position": "right",
                    "transition": "pop",
                    "text_span": "But he had a warning."
                    }
                ]
                },
                {
                "narration_text": "He said our mental abilities are like muscles – they need regular use to stay strong.",
                "start_time": 199,
                "duration": 5,
                "visuals": [
                    {
                    "description": "Animation comparing a brain to a bicep muscle.",
                    "timestamp": 0,
                    "duration": 2.5,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "mental abilities are like muscles"
                    },
                    {
                    "description": "Visual of the brain/muscle character lifting 'cognitive weights'.",
                    "timestamp": 2.5,
                    "duration": 2.5,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "need regular use to stay strong."
                    }
                ]
                },
                {
                "narration_text": "If AI does all the heavy lifting, do your cognitive 'muscles' start to atrophy? To weaken?",
                "start_time": 204,
                "duration": 6,
                "visuals": [
                    {
                    "description": "Animation: AI robot easily lifting the heavy cognitive weights while the brain/muscle character sits idly by.",
                    "timestamp": 0,
                    "duration": 3,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "If AI does all the heavy lifting"
                    },
                    {
                    "description": "The brain/muscle character is shown slowly shrinking or becoming flabby.",
                    "timestamp": 3,
                    "duration": 3,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "start to atrophy? To weaken?"
                    }
                ]
                },
                {
                "narration_text": "Think about it: It takes discipline to choose the harder path, to exercise your brain when an easy AI shortcut is available.",
                "start_time": 210,
                "duration": 7,
                "visuals": [
                    {
                    "description": "Visual of a crossroads: One path is steep and rocky ('Brain Workout'), the other is a smooth, easy downhill slide ('AI Shortcut').",
                    "timestamp": 0,
                    "duration": 3.5,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "choose* the harder path"
                    },
                    {
                    "description": "A finger hovering over the 'AI Shortcut' button, hesitating.",
                    "timestamp": 3.5,
                    "duration": 3.5,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "zoom",
                    "text_span": "easy AI shortcut is available."
                    }
                ]
                },
                {
                "narration_text": "It's like choosing stairs over the elevator. Sometimes you just... take the elevator, right?",
                "start_time": 217,
                "duration": 5,
                "visuals": [
                    {
                    "description": "Split screen: Left shows someone effortfully climbing stairs. Right shows someone relaxing in an elevator.",
                    "timestamp": 0,
                    "duration": 2.5,
                    "visual_type": "image",
                    "position": "full",
                    "transition": "slide"
                    },
                    {
                    "description": "Close-up on someone pressing the elevator button with a slight smile of relief.",
                    "timestamp": 2.5,
                    "duration": 2.5,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "zoom",
                    "text_span": "take the elevator, right?"
                    }
                ]
                },
                {
                "narration_text": "This isn't just about grades anymore. These students graduate, enter the workforce...",
                "start_time": 222,
                "duration": 5,
                "visuals": [
                    {
                    "description": "Animation showing graduation caps being thrown in the air.",
                    "timestamp": 0,
                    "duration": 2,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade"
                    },
                    {
                    "description": "Transition to visual of young professionals entering an office building.",
                    "timestamp": 2,
                    "duration": 3,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "slide",
                    "text_span": "enter the workforce..."
                    }
                ]
                },
                {
                "narration_text": "...carrying those AI-reliant habits with them. Using tools to fill gaps where skills should be.",
                "start_time": 227,
                "duration": 6,
                "visuals": [
                    {
                    "description": "Visual of a young employee secretly using an AI tool on their computer during a meeting.",
                    "timestamp": 0,
                    "duration": 3,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "AI-reliant habits"
                    },
                    {
                    "description": "Animation of puzzle pieces representing skills, with an AI icon filling in a missing piece.",
                    "timestamp": 3,
                    "duration": 3,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "Using tools to fill gaps"
                    }
                ]
                },
                {
                "narration_text": "Is this 'working smarter'? Or are you slowly letting your own abilities fade by leaning too heavily on the tech?",
                "start_time": 233,
                "duration": 7,
                "visuals": [
                    {
                    "description": "Text graphic: 'Working Smarter?' vs 'Losing Skills?' with question marks.",
                    "timestamp": 0,
                    "duration": 3.5,
                    "visual_type": "text",
                    "position": "center",
                    "transition": "fade"
                    },
                    {
                    "description": "Visual of a dimmer switch labeled 'Your Abilities' being slowly turned down.",
                    "timestamp": 3.5,
                    "duration": 3.5,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "letting your own abilities fade"
                    }
                ]
                },
                {
                "narration_text": "It's a tricky balance. Efficiency is great, but not if the long-term cost is your own brainpower.",
                "start_time": 240,
                "duration": 5,
                "visuals": [
                    {
                    "description": "Return to the scale visual: 'Efficiency' on one side, 'Brainpower' on the other, trying to find balance.",
                    "timestamp": 0,
                    "duration": 2.5,
                    "visual_type": "diagram",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "tricky balance."
                    },
                    {
                    "description": "Close up on the 'Brainpower' side of the scale, looking precarious.",
                    "timestamp": 2.5,
                    "duration": 2.5,
                    "visual_type": "diagram",
                    "position": "center",
                    "transition": "zoom"
                    }
                ]
                },
                {
                "narration_text": "This leads us to something called 'cognitive offloading' - basically, letting tech do the thinking for you.",
                "start_time": 245,
                "duration": 6,
                "visuals": [
                    {
                    "description": "Text graphic: 'Cognitive Offloading'",
                    "timestamp": 0,
                    "duration": 2,
                    "visual_type": "text",
                    "position": "center",
                    "transition": "fade"
                    },
                    {
                    "description": "Simple animation: Brain character literally handing over a thought bubble (containing a problem) to a robot/AI.",
                    "timestamp": 2,
                    "duration": 4,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "letting tech do the thinking for you."
                    }
                ]
                },
                {
                "narration_text": "And sometimes, the tech you're trusting gets it spectacularly wrong.",
                "start_time": 251,
                "duration": 4,
                "visuals": [
                    {
                    "description": "Animation of the robot/AI confidently providing a nonsensical or clearly wrong answer.",
                    "timestamp": 0,
                    "duration": 2,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade"
                    },
                    {
                    "description": "Explosion graphic or 'ERROR' message overlaying the wrong answer.",
                    "timestamp": 2,
                    "duration": 2,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "pop",
                    "text_span": "gets it spectacularly wrong."
                    }
                ]
                }
            ]
            },
            {
            "title": "Cognitive Offloading: Trust Me, I'm an AI?",
            "content": "Defining 'cognitive offloading' and illustrating its dangers with real-world examples, like the flawed facial recognition case. Highlighting the issue of misplaced trust in AI, even when it's unreliable.",
            "total_duration": 115,
            "segments": [
                {
                "narration_text": "So, 'cognitive offloading'. Fancy term, simple idea: You use tech to reduce your own mental effort.",
                "start_time": 280,
                "duration": 6,
                "visuals": [
                    {
                    "description": "Animated definition: 'Cognitive Offloading = Less Brain Strain (Thanks, Tech!)'.",
                    "timestamp": 0,
                    "duration": 3,
                    "visual_type": "text",
                    "position": "center",
                    "transition": "fade"
                    },
                    {
                    "description": "Brain character sighing with relief as a smartphone takes over a task.",
                    "timestamp": 3,
                    "duration": 3,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "reduce your own mental effort."
                    }
                ]
                },
                {
                "narration_text": "Think using a calculator for basic math you could do in your head, or letting autocorrect handle all your spelling.",
                "start_time": 286,
                "duration": 6,
                "visuals": [
                    {
                    "description": "Split screen: Left, someone using a calculator for '2+2'. Right, someone struggling to spell a simple word without autocorrect.",
                    "timestamp": 0,
                    "duration": 3,
                    "visual_type": "image",
                    "position": "full",
                    "transition": "slide"
                    },
                    {
                    "description": "Close-up on a phone screen aggressively correcting a misspelled word.",
                    "timestamp": 3,
                    "duration": 1.5,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "zoom"
                    },
                    {
                    "description": "Iconic red squiggly underline appearing under text.",
                    "timestamp": 4.5,
                    "duration": 1.5,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade"
                    }
                ]
                },
                {
                "narration_text": "AI takes this way further. You're not just offloading calculation or spelling, but problem-solving, decision-making, critical evaluation.",
                "start_time": 292,
                "duration": 7,
                "visuals": [
                    {
                    "description": "Escalation graphic: Calculator -> Autocorrect -> AI icon handling complex tasks (puzzle piece, scales of justice, magnifying glass).",
                    "timestamp": 0,
                    "duration": 4,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "AI takes this way further."
                    },
                    {
                    "description": "Close up on the AI icon juggling these complex task symbols.",
                    "timestamp": 4,
                    "duration": 3,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "zoom"
                    }
                ]
                },
                {
                "narration_text": "One study found frequent AI users were more likely to just... let the tech decide, rather than thinking critically themselves.",
                "start_time": 299,
                "duration": 7,
                "visuals": [
                    {
                    "description": "Text graphic: 'Study Finding: Frequent AI Use -> More Offloading'.",
                    "timestamp": 0,
                    "duration": 2,
                    "visual_type": "text",
                    "position": "left",
                    "transition": "slide"
                    },
                    {
                    "description": "Animation: Person shrugging and pointing towards an AI, letting it make a decision represented by choosing a path.",
                    "timestamp": 2,
                    "duration": 3,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "let the tech decide"
                    },
                    {
                    "description": "Visual of a brain character putting its feet up, looking disengaged.",
                    "timestamp": 5,
                    "duration": 2,
                    "visual_type": "animation",
                    "position": "right",
                    "transition": "fade",
                    "text_span": "rather than thinking critically"
                    }
                ]
                },
                {
                "narration_text": "Over time, this heavy reliance seemed to reduce their ability to evaluate info or form nuanced conclusions.",
                "start_time": 306,
                "duration": 6,
                "visuals": [
                    {
                    "description": "Animation: 'Critical Thinking' skill bar decreasing over time for the AI-reliant person.",
                    "timestamp": 0,
                    "duration": 3,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "reduce their ability to evaluate info"
                    },
                    {
                    "description": "Visual: Complex issue represented by tangled lines, AI user sees only simple 'yes/no' output, missing the nuance.",
                    "timestamp": 3,
                    "duration": 3,
                    "visual_type": "diagram",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "form nuanced conclusions."
                    }
                ]
                },
                {
                "narration_text": "Now, here's where it gets really worrying. Remember that police facial recognition story from Detroit?",
                "start_time": 312,
                "duration": 5,
                "visuals": [
                    {
                    "description": "Transition to a more serious tone. Image: Grainy surveillance footage still.",
                    "timestamp": 0,
                    "duration": 2.5,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "fade"
                    },
                    {
                    "description": "Map pinpointing Detroit, Michigan.",
                    "timestamp": 2.5,
                    "duration": 2.5,
                    "visual_type": "image",
                    "position": "left",
                    "transition": "zoom",
                    "text_span": "Detroit"
                    }
                ]
                },
                {
                "narration_text": "Poor quality footage of a robbery. The department used an AI facial recognition tool.",
                "start_time": 317,
                "duration": 5,
                "visuals": [
                    {
                    "description": "Visual: Police officer looking at the grainy footage, then turning to a computer screen showing facial recognition software.",
                    "timestamp": 0,
                    "duration": 2.5,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "Poor quality footage"
                    },
                    {
                    "description": "Close-up on the software interface, showing scanning lines over a blurry face.",
                    "timestamp": 2.5,
                    "duration": 2.5,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "zoom",
                    "text_span": "AI facial recognition tool."
                    }
                ]
                },
                {
                "narration_text": "The AI pinged a match: Porcha Woodruff, based on an old mugshot. Problem? She was 8 months pregnant and clearly not the suspect.",
                "start_time": 322,
                "duration": 8,
                "visuals": [
                    {
                    "description": "Animation: AI shows a 'MATCH FOUND' notification with Woodruff's photo.",
                    "timestamp": 0,
                    "duration": 2.5,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "pop",
                    "text_span": "AI pinged a match"
                    },
                    {
                    "description": "Side-by-side images: The old mugshot vs. a photo/representation of Woodruff visibly pregnant.",
                    "timestamp": 2.5,
                    "duration": 3,
                    "visual_type": "image",
                    "position": "full",
                    "transition": "slide"
                    },
                    {
                    "description": "Graphic showing a large red 'X' over the incorrect match.",
                    "timestamp": 5.5,
                    "duration": 2.5,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "clearly not the suspect."
                    }
                ]
                },
                {
                "narration_text": "But the police, relying solely on the AI's flawed output, arrested her anyway. A classic case of cognitive offloading gone wrong.",
                "start_time": 330,
                "duration": 8,
                "visuals": [
                    {
                    "description": "Visual representation: Police officers looking only at the AI report, ignoring the obvious visual evidence (pregnancy).",
                    "timestamp": 0,
                    "duration": 3,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "relying solely on the AI's flawed output"
                    },
                    {
                    "description": "Stylized image of handcuffs.",
                    "timestamp": 3,
                    "duration": 2,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "zoom"
                    },
                    {
                    "description": "Text overlay: 'Cognitive Offloading -> Wrongful Arrest'.",
                    "timestamp": 5,
                    "duration": 3,
                    "visual_type": "text",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "cognitive offloading gone wrong."
                    }
                ]
                },
                {
                "narration_text": "It sounds crazy, right? Why would they ignore the obvious? Because the tech was presented as reliable, easy, objective.",
                "start_time": 338,
                "duration": 7,
                "visuals": [
                    {
                    "description": "Question mark overlaying the scene of the arrest.",
                    "timestamp": 0,
                    "duration": 2,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade"
                    },
                    {
                    "description": "Marketing buzzwords flashing on screen: 'Reliable', 'Easy', 'Accurate', 'Objective' next to an AI icon.",
                    "timestamp": 2,
                    "duration": 3,
                    "visual_type": "text",
                    "position": "center",
                    "transition": "slide",
                    "text_span": "presented as reliable, easy, objective."
                    },
                    {
                    "description": "Visual of a 'Trust Me' badge pinned onto the AI icon.",
                    "timestamp": 5,
                    "duration": 2,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "pop"
                    }
                ]
                },
                {
                "narration_text": "People trust AI, especially when it makes their jobs easier. That convenience factor is incredibly tempting.",
                "start_time": 345,
                "duration": 6,
                "visuals": [
                    {
                    "description": "Graph showing high public trust levels in AI (generic representation).",
                    "timestamp": 0,
                    "duration": 3,
                    "visual_type": "diagram",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "People trust AI"
                    },
                    {
                    "description": "Animation: Person happily handing over a difficult task (represented by a heavy box) to an AI.",
                    "timestamp": 3,
                    "duration": 3,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "makes their jobs easier."
                    }
                ]
                },
                {
                "narration_text": "You don't even need high-stakes police work to see this. Look at social media!",
                "start_time": 351,
                "duration": 4,
                "visuals": [
                    {
                    "description": "Transition from serious police visuals to a lighthearted social media feed (like X/Twitter).",
                    "timestamp": 0,
                    "duration": 2,
                    "visual_type": "image",
                    "position": "full",
                    "transition": "wipe"
                    },
                    {
                    "description": "Scrolling animation through a generic social media feed.",
                    "timestamp": 2,
                    "duration": 2,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade"
                    }
                ]
                },
                {
                "narration_text": "You see people asking AI bots like Grok to explain even simple posts. Why bother thinking when the AI can do it?",
                "start_time": 355,
                "duration": 7,
                "visuals": [
                    {
                    "description": "Screenshot (stylized/generic) of a social media reply: '@Grok explain this tweet'.",
                    "timestamp": 0,
                    "duration": 3.5,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "asking AI bots like Grok"
                    },
                    {
                    "description": "Animation: Brain character literally outsourcing the task of reading/understanding a simple sentence to a bot.",
                    "timestamp": 3.5,
                    "duration": 3.5,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "Why bother thinking"
                    }
                ]
                },
                {
                "narration_text": "Okay, maybe asking for a quick summary saves time sometimes. But overusing it for stuff you could easily figure out?",
                "start_time": 362,
                "duration": 6,
                "visuals": [
                    {
                    "description": "Visual of a clock speeding up, representing 'saving time'.",
                    "timestamp": 0,
                    "duration": 2,
                    "visual_type": "animation",
                    "position": "left",
                    "transition": "fade"
                    },
                    {
                    "description": "Question mark hovering over a simple, easy-to-understand statement.",
                    "timestamp": 2,
                    "duration": 2,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "fade"
                    },
                    {
                    "description": "A hand repeatedly clicking an 'Ask AI' button for increasingly simple things.",
                    "timestamp": 4,
                    "duration": 2,
                    "visual_type": "animation",
                    "position": "right",
                    "transition": "fade",
                    "text_span": "overusing it"
                    }
                ]
                },
                {
                "narration_text": "It's a slippery slope towards letting something else handle the basic mental work your brain is built for.",
                "start_time": 368,
                "duration": 6,
                "visuals": [
                    {
                    "description": "Animation of a person sliding down a slippery slope labeled 'Cognitive Laziness'.",
                    "timestamp": 0,
                    "duration": 3,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "slippery slope"
                    },
                    {
                    "description": "Visual of a brain with cobwebs growing on it.",
                    "timestamp": 3,
                    "duration": 3,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "basic mental work your brain is built for."
                    }
                ]
                },
                {
                "narration_text": "And this blends into another subtle issue: how algorithms are constantly making choices for you.",
                "start_time": 374,
                "duration": 5,
                "visuals": [
                    {
                    "description": "Visual transition: Fading from cognitive offloading graphics to algorithmic recommendation feeds.",
                    "timestamp": 0,
                    "duration": 2.5,
                    "visual_type": "transition",
                    "position": "full",
                    "transition": "fade"
                    },
                    {
                    "description": "Stylized graphic of abstract algorithm lines influencing a person's choices (what to watch, read, buy).",
                    "timestamp": 2.5,
                    "duration": 2.5,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "algorithms are constantly making choices for you."
                    }
                ]
                }
            ]
            },
            {
            "title": "Algorithmic Complacency: Who's Really Choosing?",
            "content": "Inspired by Technology Connections, this section explores how we passively accept algorithmic recommendations, potentially losing touch with our own preferences and decision-making agency.",
            "total_duration": 93,
            "segments": [
                {
                "narration_text": "Think about how you find stuff online these days. YouTube, TikTok, Instagram... even how you found this video, maybe!",
                "start_time": 395,
                "duration": 7,
                "visuals": [
                    {
                    "description": "Montage of logos: YouTube, TikTok, Instagram, Facebook.",
                    "timestamp": 0,
                    "duration": 2.5,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "slide"
                    },
                    {
                    "description": "Visual of a phone screen showing an endless scrolling feed of recommended content.",
                    "timestamp": 2.5,
                    "duration": 2.5,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "find stuff online"
                    },
                    {
                    "description": "Arrow pointing from a YouTube recommendations sidebar towards the current video frame.",
                    "timestamp": 5,
                    "duration": 2,
                    "visual_type": "animation",
                    "position": "right",
                    "transition": "pop",
                    "text_span": "how you found this video"
                    }
                ]
                },
                {
                "narration_text": "How often are you actively deciding what to watch or read, versus just... clicking what the algorithm serves up?",
                "start_time": 402,
                "duration": 7,
                "visuals": [
                    {
                    "description": "Split screen: Left shows someone actively typing a search query. Right shows someone passively scrolling recommended videos.",
                    "timestamp": 0,
                    "duration": 3.5,
                    "visual_type": "image",
                    "position": "full",
                    "transition": "slide",
                    "text_span": "you actively deciding vs clicking what's served"
                    },
                    {
                    "description": "Animation of an 'algorithm' character spoon-feeding content to a passive viewer.",
                    "timestamp": 3.5,
                    "duration": 3.5,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "clicking what the algorithm serves up?"
                    }
                ]
                },
                {
                "narration_text": "Alec Watson from 'Technology Connections' calls this 'algorithmic complacency'. Love that term.",
                "start_time": 409,
                "duration": 5,
                "visuals": [
                    {
                    "description": "Text graphic: 'Algorithmic Complacency' (credit: Technology Connections).",
                    "timestamp": 0,
                    "duration": 3,
                    "visual_type": "text",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "'algorithmic complacency'"
                    },
                    {
                    "description": "Host nodding in appreciation.",
                    "timestamp": 3,
                    "duration": 2,
                    "visual_type": "image",
                    "position": "right",
                    "transition": "fade",
                    "text_span": "Love that term."
                    }
                ]
                },
                {
                "narration_text": "It's this subtle shift where you start letting the computer program decide what you see, even if you could choose differently.",
                "start_time": 414,
                "duration": 7,
                "visuals": [
                    {
                    "description": "Animation: Person at a fork in the road (representing choices), an algorithm gently pushes them down one path.",
                    "timestamp": 0,
                    "duration": 3.5,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "letting the computer program decide"
                    },
                    {
                    "description": "Visual of other paths fading or becoming obscured, representing missed choices.",
                    "timestamp": 3.5,
                    "duration": 3.5,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "even if you could choose differently."
                    }
                ]
                },
                {
                "narration_text": "Remember the 'old internet'? Clicking bookmarks, actively searching for sites you liked?",
                "start_time": 421,
                "duration": 5,
                "visuals": [
                    {
                    "description": "Retro computer screen showing a simple browser with bookmarks visible.",
                    "timestamp": 0,
                    "duration": 2.5,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "'old internet'?"
                    },
                    {
                    "description": "Animation of a mouse cursor actively clicking on bookmarked links.",
                    "timestamp": 2.5,
                    "duration": 2.5,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "Clicking bookmarks, actively searching"
                    }
                ]
                },
                {
                "narration_text": "It was more manual, sure, but you were largely in charge of curating your experience.",
                "start_time": 426,
                "duration": 5,
                "visuals": [
                    {
                    "description": "Visual of hands carefully arranging items (representing websites/content) into a personal collection.",
                    "timestamp": 0,
                    "duration": 2.5,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "curating your experience."
                    },
                    {
                    "description": "A captain's wheel graphic with 'YOU' in the center.",
                    "timestamp": 2.5,
                    "duration": 2.5,
                    "visual_type": "diagram",
                    "position": "center",
                    "transition": "pop",
                    "text_span": "you were largely in charge"
                    }
                ]
                },
                {
                "narration_text": "Now, it often feels like you're just floating down the algorithm's river, letting it take you wherever.",
                "start_time": 431,
                "duration": 6,
                "visuals": [
                    {
                    "description": "Animation of a person passively floating on an inner tube down a river labeled 'Algorithm Feed'.",
                    "timestamp": 0,
                    "duration": 3,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "floating down the algorithm's river"
                    },
                    {
                    "description": "The river branches off in many directions, but the person stays on the main current.",
                    "timestamp": 3,
                    "duration": 3,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "letting it take you wherever."
                    }
                ]
                },
                {
                "narration_text": "The more you rely on these recommendations, the less you might ask yourself: 'What do I actually want?'",
                "start_time": 437,
                "duration": 7,
                "visuals": [
                    {
                    "description": "Close up on the passive person's face in the river animation, looking slightly bored or vacant.",
                    "timestamp": 0,
                    "duration": 3,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "zoom"
                    },
                    {
                    "description": "Thought bubble appears: 'What do I want?' - but it's faint or transparent.",
                    "timestamp": 3,
                    "duration": 4,
                    "visual_type": "animation",
                    "position": "right",
                    "transition": "fade",
                    "text_span": "'What do I actually want?'"
                    }
                ]
                },
                {
                "narration_text": "Your agency, your ability to choose, gets subtly eroded without you even noticing.",
                "start_time": 444,
                "duration": 5,
                "visuals": [
                    {
                    "description": "Animation: A statue representing 'Personal Agency' slowly eroding or crumbling away.",
                    "timestamp": 0,
                    "duration": 3,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "Your agency... gets subtly eroded"
                    },
                    {
                    "description": "Visual similar to the GPS study: Person looking unaware of the erosion happening.",
                    "timestamp": 3,
                    "duration": 2,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "fade"
                    }
                ]
                },
                {
                "narration_text": "For younger generations especially, who grew up with this, trusting the algorithm might feel more natural than trusting human curation.",
                "start_time": 449,
                "duration": 8,
                "visuals": [
                    {
                    "description": "Visual: Young person comfortably interacting with algorithmic feeds on multiple devices.",
                    "timestamp": 0,
                    "duration": 4,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "younger generations... grew up with this"
                    },
                    {
                    "description": "Split screen: Left shows algorithm icon with a checkmark. Right shows a group of people (representing human curation) with a question mark.",
                    "timestamp": 4,
                    "duration": 4,
                    "visual_type": "diagram",
                    "position": "full",
                    "transition": "slide",
                    "text_span": "trusting the algorithm... more natural"
                    }
                ]
                },
                {
                "narration_text": "Combine this algorithmic complacency with AI that generates answers...",
                "start_time": 457,
                "duration": 4,
                "visuals": [
                    {
                    "description": "Visual combination: Algorithmic river flowing towards an AI 'answer machine'.",
                    "timestamp": 0,
                    "duration": 2,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade"
                    },
                    {
                    "description": "Plus sign graphic connecting the two concepts.",
                    "timestamp": 2,
                    "duration": 2,
                    "visual_type": "diagram",
                    "position": "center",
                    "transition": "fade"
                    }
                ]
                },
                {
                "narration_text": "...and you've got a recipe for potentially accepting flawed information without much critical thought.",
                "start_time": 461,
                "duration": 6,
                "visuals": [
                    {
                    "description": "Animation: The AI answer machine produces a slightly wrong or nonsensical answer.",
                    "timestamp": 0,
                    "duration": 3,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "accepting flawed information"
                    },
                    {
                    "description": "The person floating down the algorithm river passively accepts the flawed answer without questioning.",
                    "timestamp": 3,
                    "duration": 3,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "without much critical thought."
                    }
                ]
                },
                {
                "narration_text": "Which brings us to another snag: AI doesn't always know what's true.",
                "start_time": 467,
                "duration": 4,
                "visuals": [
                    {
                    "description": "Transition visual: Glitchy effect over the AI answer machine.",
                    "timestamp": 0,
                    "duration": 2,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade"
                    },
                    {
                    "description": "AI icon with a question mark over its 'head' and shrugging.",
                    "timestamp": 2,
                    "duration": 2,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "AI doesn't always know what's true."
                    }
                ]
                },
                {
                "narration_text": "Sometimes, it confidently makes stuff up. They call these 'hallucinations'.",
                "start_time": 471,
                "duration": 5,
                "visuals": [
                    {
                    "description": "Animation: AI confidently stating something absurd (e.g., '2+2=5' or 'Pigs can fly').",
                    "timestamp": 0,
                    "duration": 2.5,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "confidently makes stuff up."
                    },
                    {
                    "description": "Text graphic: 'AI Hallucinations' with a dreamy/wavy effect.",
                    "timestamp": 2.5,
                    "duration": 2.5,
                    "visual_type": "text",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "'hallucinations'."
                    }
                ]
                },
                {
                "narration_text": "And if you're already used to just accepting what tech tells you... you might believe it.",
                "start_time": 476,
                "duration": 5,
                "visuals": [
                    {
                    "description": "Return to the visual of the person passively accepting the AI's answer, this time the answer is clearly wrong but accepted.",
                    "timestamp": 0,
                    "duration": 3,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "accepting what tech tells you"
                    },
                    {
                    "description": "A checkmark appearing next to the wrong information in the person's thought bubble.",
                    "timestamp": 3,
                    "duration": 2,
                    "visual_type": "animation",
                    "position": "right",
                    "transition": "pop",
                    "text_span": "you might believe it."
                    }
                ]
                }
            ]
            },
            {
            "title": "The Knowledge Problem: Hallucinations & Model Collapse",
            "content": "Focusing on AI's limitations in discerning truth, using examples like Google's AI Overviews issues and the concept of 'model collapse' where AI pollutes its own training data.",
            "total_duration": 60,
            "segments": [
                {
                "narration_text": "Remember when Google launched its AI Overviews? Those little AI summaries at the top of search results?",
                "start_time": 488,
                "duration": 6,
                "visuals": [
                    {
                    "description": "Screenshot of a Google search results page highlighting the AI Overview box.",
                    "timestamp": 0,
                    "duration": 3,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "Google launched its AI Overviews"
                    },
                    {
                    "description": "Zoom in on the AI-generated summary text.",
                    "timestamp": 3,
                    "duration": 3,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "zoom"
                    }
                ]
                },
                {
                "narration_text": "Yeah... that had some teething problems. Telling people to eat rocks, that snakes are mammals...",
                "start_time": 494,
                "duration": 6,
                "visuals": [
                    {
                    "description": "Montage of humorous but concerning headlines/screenshots of AI Overview errors (stylized).",
                    "timestamp": 0,
                    "duration": 3,
                    "visual_type": "image",
                    "position": "full",
                    "transition": "slide",
                    "text_span": "teething problems."
                    },
                    {
                    "description": "Specific examples visualized: Icon of a person eating a rock with a green checkmark (wrong), icon of a snake labeled 'Mammal'.",
                    "timestamp": 3,
                    "duration": 3,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "eat rocks... snakes are mammals..."
                    }
                ]
                },
                {
                "narration_text": "It highlighted a core issue: current AI, especially Large Language Models like ChatGPT, struggle with factual accuracy.",
                "start_time": 500,
                "duration": 7,
                "visuals": [
                    {
                    "description": "Graphic showing 'Truth' and 'Fiction' blurred together within an AI model.",
                    "timestamp": 0,
                    "duration": 3.5,
                    "visual_type": "diagram",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "struggle with factual accuracy."
                    },
                    {
                    "description": "Logos of major LLMs (ChatGPT, Gemini, etc.) with question marks over them.",
                    "timestamp": 3.5,
                    "duration": 3.5,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "fade"
                    }
                ]
                },
                {
                "narration_text": "As AI pioneer Geoffrey Hinton put it, they don't really understand 'truth'. They're just predicting the next word based on vast, often inconsistent data.",
                "start_time": 507,
                "duration": 8,
                "visuals": [
                    {
                    "description": "Quote card: 'Doesn't really understand truth' - Geoffrey Hinton.",
                    "timestamp": 0,
                    "duration": 3,
                    "visual_type": "text",
                    "position": "center",
                    "transition": "fade"
                    },
                    {
                    "description": "Animation: AI model shown as a complex text prediction engine, piecing words together.",
                    "timestamp": 3,
                    "duration": 3,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "predicting the next word"
                    },
                    {
                    "description": "Visual representation of the vast, messy internet data AI trains on (mix of facts, opinions, errors).",
                    "timestamp": 6,
                    "duration": 2,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "zoom",
                    "text_span": "often inconsistent data."
                    }
                ]
                },
                {
                "narration_text": "And here's a scary thought: What happens when AI starts learning from otherAI-generated content*?",
                "start_time": 515,
                "duration": 6,
                "visuals": [
                    {
                    "description": "Animation: AI model looking at its own reflection, which is slightly distorted.",
                    "timestamp": 0,
                    "duration": 3,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "learning from otherAI-generated content*?"
                    },
                    {
                    "description": "Circular diagram: AI creates content -> Content goes online -> AI trains on that content -> Creates more content...",
                    "timestamp": 3,
                    "duration": 3,
                    "visual_type": "diagram",
                    "position": "center",
                    "transition": "fade"
                    }
                ]
                },
                {
                "narration_text": "Researchers call it 'model collapse'. If AI keeps training on its own output, errors can compound.",
                "start_time": 521,
                "duration": 6,
                "visuals": [
                    {
                    "description": "Text graphic: 'Model Collapse'.",
                    "timestamp": 0,
                    "duration": 2,
                    "visual_type": "text",
                    "position": "center",
                    "transition": "fade"
                    },
                    {
                    "description": "Animation: Like a photocopy of a photocopy, the AI output gets progressively worse, more distorted with each cycle.",
                    "timestamp": 2,
                    "duration": 4,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "errors can compound."
                    }
                ]
                },
                {
                "narration_text": "One study showed after just a few cycles, the quality dropped fast. By the ninth, it was nonsense.",
                "start_time": 527,
                "duration": 6,
                "visuals": [
                    {
                    "description": "Simplified graph showing 'Output Quality' dramatically decreasing over 'Training Cycles'.",
                    "timestamp": 0,
                    "duration": 3,
                    "visual_type": "diagram",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "quality dropped fast."
                    },
                    {
                    "description": "Visual of the final output being completely garbled text or nonsensical images.",
                    "timestamp": 3,
                    "duration": 3,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "zoom",
                    "text_span": "By the ninth, it was nonsense."
                    }
                ]
                },
                {
                "narration_text": "With estimates suggesting a huge chunk of internet content might already be AI-generated...",
                "start_time": 533,
                "duration": 5,
                "visuals": [
                    {
                    "description": "Graphic: Pie chart showing a large percentage (e.g., 60%) of the internet labeled 'AI-Generated'.",
                    "timestamp": 0,
                    "duration": 2.5,
                    "visual_type": "diagram",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "huge chunk of internet content"
                    },
                    {
                    "description": "Visual of the internet represented as a vast library, with many books subtly glowing or marked as AI.",
                    "timestamp": 2.5,
                    "duration": 2.5,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "fade"
                    }
                ]
                },
                {
                "narration_text": "...you can see how the internet might start 'eating itself', polluting the very data AI needs.",
                "start_time": 538,
                "duration": 5,
                "visuals": [
                    {
                    "description": "Animation of the Ouroboros (snake eating its tail) labeled 'Internet Data'.",
                    "timestamp": 0,
                    "duration": 2.5,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "internet might start 'eating itself'"
                    },
                    {
                    "description": "Visual of data streams becoming murky or polluted.",
                    "timestamp": 2.5,
                    "duration": 2.5,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "polluting the very data AI needs."
                    }
                ]
                },
                {
                "narration_text": "So, you're relying on a tool that might be getting dumber itself, or at least, less reliable.",
                "start_time": 543,
                "duration": 5,
                "visuals": [
                    {
                    "description": "Return to the AI icon, now looking confused or glitchy.",
                    "timestamp": 0,
                    "duration": 2.5,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "getting dumber itself"
                    },
                    {
                    "description": "Reliability meter pointing towards 'Low'.",
                    "timestamp": 2.5,
                    "duration": 2.5,
                    "visual_type": "diagram",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "less reliable."
                    }
                ]
                }
            ]
            },
            {
            "title": "Fighting Back: Keeping Your Brain Sharp",
            "content": "Shifting to solutions. Offering practical, actionable advice on how you can use AI as a helpful tool without letting it erode your critical thinking and skills. Emphasizing mindful usage and the irreplaceable value of human thought.",
            "total_duration": 76,
            "segments": [
                {
                "narration_text": "Okay, deep breaths. It's not hopeless! You don't need to throw your phone in a river.",
                "start_time": 548,
                "duration": 5,
                "visuals": [
                    {
                    "description": "Host taking a calming breath, smiling reassuringly.",
                    "timestamp": 0,
                    "duration": 2,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "fade"
                    },
                    {
                    "description": "Humorous animation of someone about to throw a smartphone into water, then pausing.",
                    "timestamp": 2,
                    "duration": 3,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "don't need to throw your phone in a river."
                    }
                ]
                },
                {
                "narration_text": "Remember, AI, like GPS or calculators or spreadsheets, is fundamentally a TOOL.",
                "start_time": 553,
                "duration": 5,
                "visuals": [
                    {
                    "description": "Icons side-by-side: GPS, Calculator, Spreadsheet (VisiCalc-style), AI.",
                    "timestamp": 0,
                    "duration": 2.5,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "slide"
                    },
                    {
                    "description": "A large wrench or hammer graphic labeled 'TOOL'.",
                    "timestamp": 2.5,
                    "duration": 2.5,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "pop",
                    "text_span": "fundamentally a TOOL."
                    }
                ]
                },
                {
                "narration_text": "The key is how you use it. Are you letting it replace your thinking, or augment it?",
                "start_time": 558,
                "duration": 5,
                "visuals": [
                    {
                    "description": "Split screen: Left shows AI pushing brain aside ('Replace'). Right shows AI handing a tool to the brain ('Augment').",
                    "timestamp": 0,
                    "duration": 3,
                    "visual_type": "diagram",
                    "position": "full",
                    "transition": "slide"
                    },
                    {
                    "description": "Focus on the 'Augment' side, showing collaboration.",
                    "timestamp": 3,
                    "duration": 2,
                    "visual_type": "diagram",
                    "position": "center",
                    "transition": "zoom"
                    }
                ]
                },
                {
                "narration_text": "Tip 1: Be the Boss, Not the Intern. Use AI for specific tasks, but you guide the strategy.",
                "start_time": 563,
                "duration": 6,
                "visuals": [
                    {
                    "description": "Text graphic: 'Tip 1: Be the Boss'.",
                    "timestamp": 0,
                    "duration": 2,
                    "visual_type": "text",
                    "position": "left",
                    "transition": "slide"
                    },
                    {
                    "description": "Animation: Person (Boss) giving instructions to an AI (Intern) which then carries out a specific, defined task.",
                    "timestamp": 2,
                    "duration": 4,
                    "visual_type": "animation",
                    "position": "right",
                    "transition": "fade",
                    "text_span": "you guide the strategy."
                    }
                ]
                },
                {
                "narration_text": "Let it draft that email, sure, but you review, edit, and ensure it sounds like you and makes sense.",
                "start_time": 569,
                "duration": 6,
                "visuals": [
                    {
                    "description": "Visual: AI generates email draft.",
                    "timestamp": 0,
                    "duration": 1.5,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "fade"
                    },
                    {
                    "description": "Then, a human hand uses a red pen (digital or real) to edit and refine the draft.",
                    "timestamp": 1.5,
                    "duration": 3,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "you review, edit"
                    },
                    {
                    "description": "Final email shown with personal touches.",
                    "timestamp": 4.5,
                    "duration": 1.5,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "fade"
                    }
                ]
                },
                {
                "narration_text": "Tip 2: Question Everything (Kindly). Treat AI answers like a starting point, not the final word.",
                "start_time": 575,
                "duration": 6,
                "visuals": [
                    {
                    "description": "Text graphic: 'Tip 2: Question Everything'.",
                    "timestamp": 0,
                    "duration": 2,
                    "visual_type": "text",
                    "position": "left",
                    "transition": "slide"
                    },
                    {
                    "description": "AI provides an answer. A magnifying glass appears over it, representing scrutiny.",
                    "timestamp": 2,
                    "duration": 2.5,
                    "visual_type": "animation",
                    "position": "right",
                    "transition": "fade",
                    "text_span": "Treat AI answers like a starting point"
                    },
                    {
                    "description": "Text 'Final Word' is crossed out.",
                    "timestamp": 4.5,
                    "duration": 1.5,
                    "visual_type": "text",
                    "position": "center",
                    "transition": "fade"
                    }
                ]
                },
                {
                "narration_text": "Does it seem right? Does it match what you already know? Can you quickly verify it elsewhere?",
                "start_time": 581,
                "duration": 5,
                "visuals": [
                    {
                    "description": "Checklist animation: 'Seem Right?', 'Match Knowledge?', 'Verify Elsewhere?'.",
                    "timestamp": 0,
                    "duration": 3,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade"
                    },
                    {
                    "description": "Person quickly checking another source (book, different website) to confirm AI's info.",
                    "timestamp": 3,
                    "duration": 2,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "verify it elsewhere?"
                    }
                ]
                },
                {
                "narration_text": "Tip 3: Exercise Your Brain! Deliberately do some tasks manually sometimes. Write from scratch. Solve a problem without AI help.",
                "start_time": 586,
                "duration": 8,
                "visuals": [
                    {
                    "description": "Text graphic: 'Tip 3: Exercise Your Brain!'.",
                    "timestamp": 0,
                    "duration": 2,
                    "visual_type": "text",
                    "position": "left",
                    "transition": "slide"
                    },
                    {
                    "description": "Return to the brain/muscle character lifting cognitive weights or running on a treadmill.",
                    "timestamp": 2,
                    "duration": 3,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "Exercise Your Brain!"
                    },
                    {
                    "description": "Quick cuts: Someone writing on paper, someone working out a math problem on a whiteboard.",
                    "timestamp": 5,
                    "duration": 3,
                    "visual_type": "image",
                    "position": "right",
                    "transition": "slide",
                    "text_span": "do some tasks manually"
                    }
                ]
                },
                {
                "narration_text": "It's like taking the stairs – builds strength over time, even if it feels harder in the moment.",
                "start_time": 594,
                "duration": 5,
                "visuals": [
                    {
                    "description": "Return to the stairs vs elevator visual, highlighting the stairs.",
                    "timestamp": 0,
                    "duration": 2.5,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "like taking the stairs"
                    },
                    {
                    "description": "Graph showing 'Cognitive Strength' increasing gradually over time with effort.",
                    "timestamp": 2.5,
                    "duration": 2.5,
                    "visual_type": "diagram",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "builds strength over time"
                    }
                ]
                },
                {
                "narration_text": "Think of VisiCalc, the first spreadsheet program. Accountants freaked out! 'That's my job!'",
                "start_time": 599,
                "duration": 6,
                "visuals": [
                    {
                    "description": "Retro image/animation of VisiCalc software running on an old computer.",
                    "timestamp": 0,
                    "duration": 3,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "VisiCalc, the first spreadsheet program."
                    },
                    {
                    "description": "Cartoon accountant character looking panicked at the VisiCalc screen.",
                    "timestamp": 3,
                    "duration": 3,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "Accountants freaked out!"
                    }
                ]
                },
                {
                "narration_text": "But it didn't replace accountants. It freed them up for higher-level thinking. AI can do the same, if you let it.",
                "start_time": 605,
                "duration": 7,
                "visuals": [
                    {
                    "description": "Visual: Accountant character now using VisiCalc efficiently, focusing on analysis graphs instead of manual calculation.",
                    "timestamp": 0,
                    "duration": 3.5,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "freed them up for higher-level thinking."
                    },
                    {
                    "description": "AI icon shown assisting a person who is clearly thinking and strategizing.",
                    "timestamp": 3.5,
                    "duration": 3.5,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "AI can do the same, if you let it."
                    }
                ]
                },
                {
                "narration_text": "Ultimately, your brain, your experiences, your critical thinking – that's unique. AI can't replicate that (yet!).",
                "start_time": 612,
                "duration": 6,
                "visuals": [
                    {
                    "description": "Highlight graphic around a human brain, emphasizing 'Unique Human Thought'.",
                    "timestamp": 0,
                    "duration": 3,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "your brain... that's unique."
                    },
                    {
                    "description": "AI icon looking slightly less capable or complex compared to the human brain graphic.",
                    "timestamp": 3,
                    "duration": 3,
                    "visual_type": "image",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "AI can't replicate that"
                    }
                ]
                },
                {
                "narration_text": "Don't let convenience dull your greatest asset. Think for yourself.",
                "start_time": 618,
                "duration": 4,
                "visuals": [
                    {
                    "description": "Visual of a brain sparkling or shining brightly.",
                    "timestamp": 0,
                    "duration": 2,
                    "visual_type": "animation",
                    "position": "center",
                    "transition": "fade",
                    "text_span": "dull your greatest asset."
                    },
                    {
                    "description": "Final text graphic: 'Think For Yourself.'",
                    "timestamp": 2,
                    "duration": 2,
                    "visual_type": "text",
                    "position": "center",
                    "transition": "zoom"
                    }
                ]
                },
                {
                "narration_text": "Thanks for hanging out and thinking about this with me. Stay sharp out there!",
                "start_time": 622,
                "duration": 4,
                "visuals": [
                    {
                    "description": "Host smiling warmly at the camera, perhaps giving a small wave or thumbs up.",
                    "timestamp": 0,
                    "duration": 2,
                    "visual_type": "image",
                    "position": "full",
                    "transition": "fade"
                    },
                    {
                    "description": "End screen with video title, channel name, and call to action (like/subscribe).",
                    "timestamp": 2,
                    "duration": 2,
                    "visual_type": "image",
                    "position": "full",
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
