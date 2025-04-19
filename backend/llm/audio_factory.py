"""
Factory for creating AI Audio Provider instances.
"""
from backend.llm.audio_base import AIAudioProvider
from backend.llm.google_audio_provider import GoogleTextToSpeech
from backend.config.settings import Settings

def get_audio_provider(provider_name: str | None = None) -> AIAudioProvider:
    """
    Returns an instance of the specified AI Audio Provider.

    Args:
        provider_name (str | None): The name of the provider (e.g., "google").
                                    If None, uses the default from settings.

    Returns:
        AIAudioProvider: An instance of the audio provider.

    Raises:
        ValueError: If the specified provider is not supported or configured.
    """
    settings = Settings()
    selected_provider = provider_name or settings.default_audio_provider

    print(f"Attempting to get audio provider: {selected_provider}")

    if selected_provider == "google":
        # You might want to load specific configurations for Google here
        # e.g., voice name, speaking rate from settings if needed
        print("Instantiating GoogleTextToSpeech provider.")
        return GoogleTextToSpeech()
    # Add other providers here with elif selected_provider == "other_provider":
    else:
        raise ValueError(f"Unsupported or unconfigured audio provider: {selected_provider}")
