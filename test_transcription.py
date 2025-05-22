from transcription import transcribe_audio

# Replace with a real 16kHz mono .wav file path
filepath = "input/sample.wav"

result = transcribe_audio(
    filepath=filepath,
    save_txt="outputs/sample_transcript.txt",
    save_json="outputs/sample_segments.json"
)

print("Full Transcript:")
print(result["transcript"])
print("\nFirst 3 Segments:")
for seg in result["segments"][:3]:
    print(seg)

