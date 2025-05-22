import os
import json
from typing import Dict, List
from faster_whisper import WhisperModel

# Initialize the model once (you can load larger models like "medium" if needed)
MODEL_SIZE = "base"
MODEL_DEVICE = "auto"   # options: "cpu", "cuda", "auto"

model = WhisperModel(MODEL_SIZE, compute_type="int8", device=MODEL_DEVICE)


def transcribe_audio(filepath: str, save_txt: str = None, save_json: str = None) -> Dict:
    """
    Transcribes a .wav audio file using faster-whisper.
    
    Args:
        filepath (str): Path to 16kHz mono .wav file
        save_txt (str): Optional path to save plain text transcript
        save_json (str): Optional path to save timestamped segments as JSON
    
    Returns:
        Dict: {
            "segments": List[Dict],
            "transcript": str
        }
    """
    segments, _ = model.transcribe(filepath)
    
    transcript_segments: List[Dict] = []
    full_text = ""

    for segment in segments:
        entry = {
            "start": segment.start,
            "end": segment.end,
            "text": segment.text.strip()
        }
        transcript_segments.append(entry)
        full_text += segment.text.strip() + " "

    result = {
        "segments": transcript_segments,
        "transcript": full_text.strip()
    }

    if save_txt:
        with open(save_txt, "w") as f:
            f.write(result["transcript"])
        print(f"Transcript saved to {save_txt}")

    if save_json:
        with open(save_json, "w") as f:
            json.dump(result["segments"], f, indent=2)
        print(f"Timestamped segments saved to {save_json}")

    return result

