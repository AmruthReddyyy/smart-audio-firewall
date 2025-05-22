import os
import sounddevice as sd
from scipy.io.wavfile import write as write_wav
from pydub import AudioSegment
import ffmpeg
import uuid

SAMPLE_RATE = 16000
CHANNELS = 1


def record_microphone(duration=10, output_path="input/audio_from_mic.wav"):
    """Record audio from mic and save as 16kHz mono .wav file"""
    print(f"Recording from microphone for {duration} seconds...")
    audio = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=CHANNELS)
    sd.wait()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    write_wav(output_path, SAMPLE_RATE, audio)
    print(f"Saved mic recording to {output_path}")
    return output_path


def load_audio_file(filepath, output_path=None):
    """
    Load a pre-recorded audio file (.mp3 or .wav),
    convert to 16kHz mono WAV for Whisper compatibility.
    """
    print(f"Loading audio file: {filepath}")
    audio = AudioSegment.from_file(filepath)
    audio = audio.set_channels(CHANNELS).set_frame_rate(SAMPLE_RATE)

    if not output_path:
        filename = f"{uuid.uuid4().hex}.wav"
        output_path = os.path.join("input", filename)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    audio.export(output_path, format="wav")
    print(f"Converted and saved to {output_path}")
    return output_path

