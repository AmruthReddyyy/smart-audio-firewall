import pyttsx3
engine = pyttsx3.init()
engine.save_to_file("This is a test audio file for transcription.", "example.wav")
engine.runAndWait()

