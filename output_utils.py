# output_utils.py

from typing import List, Tuple
from datetime import datetime

def redact_transcript(flagged_segments: List[dict]) -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]]]:
    original = []
    redacted = []

    for seg in flagged_segments:
        ts = f"{seg['start']:.2f}s - {seg['end']:.2f}s"
        original.append((ts, seg["text"]))

        if seg["flag_level"] == "Safe":
            redacted.append((ts, seg["text"]))
        else:
            redacted.append((ts, "[REDACTED]"))

    return original, redacted


def generate_summary(flagged_segments: List[dict]) -> str:
    if not flagged_segments:
        return "✅ No flagged content detected."

    summary_lines = []
    for seg in flagged_segments:
        if seg["flag_level"] != "Safe":
            summary_lines.append(
                f"- [{seg['flag_level']}] {seg['matched_category']} → \"{seg['matched_phrase']}\" "
                f"(score: {seg['similarity_score']}, time: {seg['start']}s - {seg['end']}s)"
            )

    return "⚠️ Flagged Content Summary:\n" + "\n".join(summary_lines)

