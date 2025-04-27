"""
Utility for forced alignment of narration text to audio using WhisperX.
"""
import whisperx
import os
from typing import List, Dict

def get_word_timestamps(audio_path: str, model_size: str = "large-v2") -> list:
    """
    Transcribe and align audio, returning a list of words with their start and end times using WhisperX (forced alignment pipeline).
    Each word is a dict: {"word": str, "start": float, "end": float}
    """
    import whisperx
    import logging
    # Step 1: Transcribe
    model = whisperx.load_model(model_size, "cpu", compute_type="float32")
    result = model.transcribe(audio_path)
    language = result["language"]
    # Step 2: Load alignment model
    align_model, metadata = whisperx.load_align_model(language_code=language, device="cpu")
    # Step 3: Align for word-level timing
    aligned = whisperx.align(result["segments"], align_model, metadata, audio_path, device="cpu")
    words = aligned.get("word_segments", [])
    logging.warning(f"[forced_alignment] Word-level timestamps: {words}")
    return words



import re

def normalize_word(word):
    # Lowercase and strip punctuation
    return re.sub(r"[^\w']+", '', word.lower())

def get_reference_text_timing(reference_text: str, word_segments: List[Dict]) -> dict:
    """
    Finds the start and end time for the reference_text within word_segments (robust to punctuation).
    Returns a dict: {"start": float, "end": float, "found": bool}
    """
    import logging
    # Tokenize and normalize reference text
    ref_words = [normalize_word(w) for w in re.findall(r"\w+'?\w*", reference_text)]
    if not word_segments:
        logging.error(f"[forced_alignment] No word segments to search for reference: {reference_text}")
        return {"start": None, "end": None, "found": False}
    # Normalize aligned words
    words = [normalize_word(ws.get("word", ws.get("text", ""))) for ws in word_segments]
    logging.warning(f"[forced_alignment] Looking for reference: {ref_words} in {words}")
    # Sliding window search
    for i in range(len(words) - len(ref_words) + 1):
        if words[i:i+len(ref_words)] == ref_words:
            start = word_segments[i]["start"]
            end = word_segments[i+len(ref_words)-1]["end"]
            logging.warning(f"[forced_alignment] Found reference '{reference_text}' at ({start}, {end})")
            return {"start": start, "end": end, "found": True}
    logging.error(f"[forced_alignment] Reference text '{reference_text}' not found in word segments.")
    return {"start": None, "end": None, "found": False}

