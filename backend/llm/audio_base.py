"""
Base class definition for AI Audio Providers.
"""
from abc import ABC, abstractmethod
import json
import os
import time

class AIAudioProvider(ABC):
    """Base class for AI audio providers"""

    @abstractmethod
    def generate_audio(self, text: str, output_path: str, language_code: str = "en-US", voice_name: str | None = None) -> bool:
        """Generate audio file from text

        Args:
            text (str): Text to convert to speech
            output_path (str): Path to save the audio file
            language_code (str, optional): Language code. Defaults to "en-US".
            voice_name (str | None, optional): Specific voice name to use. Defaults to None (provider default).


        Returns:
            bool: True if successful, False otherwise
        """
        pass

    def generate_audio_from_json(self, json_file_path: str, output_directory: str, language_code: str = "en-US") -> bool:
        """Generate audio files from a JSON file containing text and audio file names

        Args:
            json_file_path (str): Path to the JSON file
            output_directory (str): Directory to save the audio files
            language_code (str, optional): Language code. Defaults to "en-US".

        Returns:
            bool: True if all files were generated successfully, False otherwise
        """
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f: # Specify encoding
                data = json.load(f)

            if not os.path.exists(output_directory):
                os.makedirs(output_directory)

            success = True
            # Determine the base directory name from the JSON file name
            lesson_dir_name = os.path.splitext(os.path.basename(json_file_path))[0]
            lesson_directory = os.path.join(output_directory, lesson_dir_name)

            if not os.path.exists(lesson_directory):
                 os.makedirs(lesson_directory)
                 print(f"Created directory: {lesson_directory}")

            for item in data.get('data', []):
                text = item.get('text')
                audio_file_name = item.get('audio_file_name')

                if not text or not audio_file_name:
                    print(f"Skipping invalid item: {item}")
                    success = False
                    continue

                # Generate audio file directly into the lesson directory
                output_path = os.path.join(lesson_directory, audio_file_name)
                print(f"Generating audio for '{text[:30]}...' -> {output_path}")
                if not self.generate_audio(text, output_path, language_code):
                    print(f"Failed to generate audio for: {audio_file_name}")
                    success = False

                # Add delay between requests to avoid rate limiting
                time.sleep(2) # Consider making delay configurable

            return success
        except FileNotFoundError:
             print(f"Error: JSON file not found at {json_file_path}")
             return False
        except json.JSONDecodeError:
             print(f"Error: Could not decode JSON from {json_file_path}")
             return False
        except Exception as e:
            print(f"Error generating audio files: {str(e)}")
            return False
