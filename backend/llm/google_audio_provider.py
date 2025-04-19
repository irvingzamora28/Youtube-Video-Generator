"""
Google Cloud Text-to-Speech provider implementation.
"""
import base64
import json
import os
import subprocess
import requests

from backend.llm.audio_base import AIAudioProvider

class GoogleTextToSpeech(AIAudioProvider):
    """Google Cloud Text-to-Speech implementation"""

    DEFAULT_VOICE = "en-US-Journey-F" # A recommended high-quality voice

    def __init__(self, default_voice_name: str = DEFAULT_VOICE, speaking_rate: float = 1.0):
        """
        Initializes the Google TTS provider.

        Args:
            default_voice_name (str): The default voice name to use if none is specified per request.
            speaking_rate (float): Default speaking rate (1.0 is normal).
        """
        self.default_voice_name = default_voice_name
        self.speaking_rate = speaking_rate
        print(f"Initialized GoogleTextToSpeech with default voice: {self.default_voice_name}")

    def _get_gcloud_token(self) -> tuple[str, str]:
        """Get access token and project ID using gcloud CLI"""
        try:
            # Get project ID
            project_cmd = "gcloud config list --format='value(core.project)'"
            project_id = subprocess.check_output(project_cmd, shell=True, text=True).strip()
            if not project_id:
                 raise ValueError("gcloud project ID not configured.")
            print(f"Using Google Cloud Project ID: {project_id}")

            # Get access token
            token_cmd = "gcloud auth print-access-token"
            token = subprocess.check_output(token_cmd, shell=True, text=True).strip()
            if not token:
                 raise ValueError("Failed to get gcloud access token.")
            # print(f"Using Google Cloud Token: {token[:10]}...") # Avoid logging full token

            return token, project_id
        except FileNotFoundError:
             raise EnvironmentError("gcloud CLI not found. Please install and configure the Google Cloud SDK.")
        except subprocess.CalledProcessError as e:
            raise ValueError(f"Failed to get Google Cloud credentials via gcloud: {str(e)}. Make sure gcloud CLI is installed, configured, and you're logged in.")
        except Exception as e:
             raise ValueError(f"An unexpected error occurred while getting gcloud credentials: {str(e)}")

    def generate_audio(self, text: str, output_path: str, language_code: str = "en-US", voice_name: str | None = None) -> bool:
        """
        Generates audio using Google Cloud Text-to-Speech API.

        Args:
            text (str): Text to synthesize.
            output_path (str): Path to save the generated MP3 file.
            language_code (str): Language code (e.g., "en-US").
            voice_name (str | None): Specific voice name. Uses provider default if None.

        Returns:
            bool: True if successful, False otherwise.
        """
        if not text:
            print("Error: No text provided for audio generation.")
            return False

        try:
            # Ensure output directory exists
            output_dir = os.path.dirname(output_path)
            if not os.path.exists(output_dir):
                print(f"Creating output directory: {output_dir}")
                os.makedirs(output_dir)

            # Get credentials using gcloud CLI
            token, project_id = self._get_gcloud_token()

            url = "https://texttospeech.googleapis.com/v1/text:synthesize"
            headers = {
                "Content-Type": "application/json",
                "X-Goog-User-Project": project_id,
                "Authorization": f"Bearer {token}"
            }

            selected_voice = voice_name or self.default_voice_name
            print(f"Using voice: {selected_voice}")

            data = {
                "input": {"text": text},
                "voice": {
                    "languageCode": language_code,
                    "name": selected_voice,
                    # "ssmlGender": "FEMALE" # Specifying gender might conflict with specific voice names
                },
                "audioConfig": {
                    "audioEncoding": "MP3",
                    "speakingRate": self.speaking_rate
                    # Add other config like pitch if needed
                }
            }

            print(f"Requesting TTS for text: '{text[:50]}...'")
            # print("Request URL:", url)
            # print("Request Headers:", headers) # Avoid logging headers with token
            # print("Request Data:", json.dumps(data, indent=2))

            response = requests.post(url, headers=headers, json=data, timeout=60) # Added timeout

            if not response.ok:
                print(f"Error Response Status: {response.status_code}")
                print(f"Error Response Body: {response.text}")
                response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

            # The response contains the audio content in base64
            response_json = response.json()
            audio_content = response_json.get("audioContent")
            if not audio_content:
                print(f"Error: No audio content received in response: {response_json}")
                raise ValueError("No audio content received from Google TTS API")

            # Decode the base64 audio content and write to file
            print(f"Decoding and writing audio to: {output_path}")
            with open(output_path, "wb") as f:
                f.write(base64.b64decode(audio_content))
            print(f"Successfully generated audio file: {output_path}")

            return True
        except requests.exceptions.RequestException as e:
             print(f"Network error during TTS request: {str(e)}")
             return False
        except ValueError as e: # Catch specific errors like missing credentials or audio content
             print(f"Configuration or response error: {str(e)}")
             return False
        except Exception as e:
            print(f"Unexpected error generating audio for text '{text[:30]}...': {str(e)}")
            import traceback
            print(traceback.format_exc())
            return False
