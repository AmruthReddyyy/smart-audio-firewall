from audio_utils import record_microphone, load_audio_file

# Record from mic
mic_path = record_microphone(duration=5)

# OR load an existing file
converted_path = load_audio_file("input/sample.mp3")

