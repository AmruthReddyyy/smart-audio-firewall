from faster_whisper import WhisperModel
from whisper.audio import load_audio  # required to load waveform

model = WhisperModel("base", compute_type="int8")

# Load audio and detect language
waveform = load_audio("input/audio_from_mic.wav")
language, _ = model.detect_language(waveform)
print(f"Detected language: {language}")

# Transcribe
segments = model.transcribe("input/audio_from_mic.wav")
print("\nTranscript:")
for segment in segments:
    print(f"[{segment.start:.2f}s - {segment.end:.2f}s] {segment.text}")
