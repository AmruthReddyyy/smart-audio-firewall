import argparse
import os
import json
from datetime import datetime

from audio_utils import record_microphone, load_audio_file
from topic_loader import load_sensitive_topics
from flagger import embed_topics, flag_transcript
from output_utils import redact_transcript, generate_summary

from faster_whisper import WhisperModel


def transcribe_audio(audio_path):
    model = WhisperModel("base", compute_type="int8")
    segments, _ = model.transcribe(audio_path)
    return [{"text": seg.text, "start": seg.start, "end": seg.end} for seg in segments]


def main():
    parser = argparse.ArgumentParser(description="Smart Audio Firewall")
    parser.add_argument("--mic", action="store_true", help="Record from microphone")
    parser.add_argument("--file", type=str, help="Path to existing audio file")
    args = parser.parse_args()

    # Step 1: Get Audio
    if args.mic:
        audio_path = record_microphone(duration=10)
    elif args.file:
        audio_path = load_audio_file(args.file)
    else:
        print("Error: Please provide either --mic or --file <path>")
        return

    # Step 2: Transcribe
    print("\n🔊 Transcribing...")
    transcript_segments = transcribe_audio(audio_path)

    # Step 3: Load Sensitive Topics
    topic_dict = load_sensitive_topics("sensitive_topics.json")

    # Step 4: Semantic Flagging
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
    topic_embeddings = embed_topics(topic_dict, model)
    flagged_segments = flag_transcript(transcript_segments, topic_embeddings)

    # Step 5: Output
    original, redacted = redact_transcript(flagged_segments)
    summary = generate_summary(flagged_segments)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join("outputs", f"run_{timestamp}")
    os.makedirs(output_dir, exist_ok=True)

    with open(os.path.join(output_dir, "transcript.json"), "w") as f:
        json.dump(flagged_segments, f, indent=2)

    with open(os.path.join(output_dir, "redacted.txt"), "w") as f:
        for ts, txt in redacted:
            f.write(f"{ts} {txt}\n")

    with open(os.path.join(output_dir, "summary.txt"), "w") as f:
        f.write(summary)

    # Display to console
    print("\n Original Transcript:")
    for ts, txt in original:
        print(f"{ts} {txt}")

    print("\n Redacted Transcript:")
    for ts, txt in redacted:
        print(f"{ts} {txt}")

    print("\n Summary:")
    print(summary)

    print(f"\n Outputs saved to: {output_dir}")


if __name__ == "__main__":
    main()

