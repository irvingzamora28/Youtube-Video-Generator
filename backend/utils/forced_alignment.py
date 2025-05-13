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
    Finds the start and end time for the reference_text within word_segments (robust to punctuation, hyphens, and contractions).
    Returns a dict: {"start": float, "end": float, "found": bool, "fuzzy_found": bool, "matched_segments": List[Dict]}
    """
    import logging
    import re

    # --- Contraction map for expansion ---
    CONTRACTIONS = {
        "it's": ["it", "is"], "you're": ["you", "are"], "don't": ["do", "not"], "can't": ["can", "not"],
        "i'm": ["i", "am"], "they're": ["they", "are"], "we're": ["we", "are"], "isn't": ["is", "not"],
        "aren't": ["are", "not"], "wasn't": ["was", "not"], "weren't": ["were", "not"], "won't": ["will", "not"],
        "wouldn't": ["would", "not"], "shouldn't": ["should", "not"], "couldn't": ["could", "not"], "didn't": ["did", "not"],
        "hasn't": ["has", "not"], "haven't": ["have", "not"], "hadn't": ["had", "not"], "mustn't": ["must", "not"],
        "let's": ["let", "us"], "that's": ["that", "is"], "who's": ["who", "is"], "what's": ["what", "is"],
        "there's": ["there", "is"], "here's": ["here", "is"], "she's": ["she", "is"], "he's": ["he", "is"],
        "it'll": ["it", "will"], "we'll": ["we", "will"], "they'll": ["they", "will"], "i'll": ["i", "will"],
        "you'll": ["you", "will"], "she'll": ["she", "will"], "he'll": ["he", "will"], "that's": ["that", "is"],
        # Add more as needed
    }

    def normalize_and_expand(word):
        """
        Normalize, split hyphens, expand contractions.
        Returns a list of normalized words.
        """
        word = word.lower()
        # Remove punctuation except hyphens and apostrophes for now
        word = re.sub(r"[\.,!?;:\"()\[\]{}]", '', word)
        # Split hyphens
        parts = word.split('-')
        expanded = []
        for p in parts:
            p = p.strip()
            if p in CONTRACTIONS:
                expanded.extend(CONTRACTIONS[p])
            else:
                expanded.append(p)
        return expanded

    # --- Normalize and expand reference text ---
    ref_tokens = []
    for w in re.findall(r"\w+'?\w*", reference_text):
        ref_tokens.extend(normalize_and_expand(w))

    if not word_segments:
        logging.error(f"[forced_alignment] No word segments to search for reference: {reference_text}")
        return {"start": None, "end": None, "found": False, "fuzzy_found": False, "matched_segments": []}

    # --- Normalize and expand word_segments, keep mapping to original segments ---
    norm_words = []  # List of normalized words
    word_map = []    # For each normalized word, the index in word_segments it came from
    for idx, ws in enumerate(word_segments):
        seg_word = ws.get("word", ws.get("text", ""))
        expanded = normalize_and_expand(seg_word)
        norm_words.extend(expanded)
        word_map.extend([idx]*len(expanded))

    # --- Sliding window exact search ---
    logging.warning(f"[forced_alignment] Looking for reference: {ref_tokens} in {norm_words}")
    for i in range(len(norm_words) - len(ref_tokens) + 1):
        if norm_words[i:i+len(ref_tokens)] == ref_tokens:
            start_idx = word_map[i]
            end_idx = word_map[i+len(ref_tokens)-1]
            start = word_segments[start_idx]["start"]
            end = word_segments[end_idx]["end"]
            matched_segments = word_segments[start_idx:end_idx+1]
            logging.warning(f"[forced_alignment] Found reference '{reference_text}' at ({start}, {end})")
            return {"start": start, "end": end, "found": True, "fuzzy_found": False, "matched_segments": matched_segments}

    # --- Fuzzy search: best match by minimal edit distance ---
    def levenshtein(a, b):
        # Classic DP implementation
        dp = [[0]*(len(b)+1) for _ in range(len(a)+1)]
        for i in range(len(a)+1): dp[i][0] = i
        for j in range(len(b)+1): dp[0][j] = j
        for i in range(1, len(a)+1):
            for j in range(1, len(b)+1):
                cost = 0 if a[i-1] == b[j-1] else 1
                dp[i][j] = min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+cost)
        return dp[-1][-1]

    best_score = float('inf')
    best_range = (None, None)
    for i in range(len(norm_words) - len(ref_tokens) + 1):
        window = norm_words[i:i+len(ref_tokens)]
        score = levenshtein(window, ref_tokens)
        if score < best_score:
            best_score = score
            best_range = (i, i+len(ref_tokens)-1)
    # Accept only if sufficiently close (allow up to 2 edits or 20% of ref length)
    if best_score <= max(2, int(0.2*len(ref_tokens))):
        i, j = best_range
        start_idx = word_map[i]
        end_idx = word_map[j]
        start = word_segments[start_idx]["start"]
        end = word_segments[end_idx]["end"]
        matched_segments = word_segments[start_idx:end_idx+1]
        logging.warning(f"[forced_alignment] Fuzzy matched reference '{reference_text}' at ({start}, {end}) with score {best_score}")
        return {"start": start, "end": end, "found": True, "fuzzy_found": True, "matched_segments": matched_segments}

    logging.error(f"[forced_alignment] Reference text '{reference_text}' not found in word segments.")
    return {"start": None, "end": None, "found": False, "fuzzy_found": False, "matched_segments": []}


