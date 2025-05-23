# Smart Audio Firewall

An offline AI system that listens to ambient audio, transcribes it locally, and flags sensitive content based on user-defined topics. Built using only open-source tools — no closed APIs.

---

## Description

Smart Audio Firewall is designed to act as a privacy-preserving filter for spoken content. It captures live or pre-recorded audio, converts it to text using Whisper (ASR), then semantically analyzes the content using transformer-based NLP models to flag sensitive topics like finance, health, or confidential projects.

---

## Features

- **Live Mic or File Input**: Record from your mic or load `.mp3` / `.wav` files
-  **Transcription**: Fast, local speech-to-text using `faster-whisper`
-  **Semantic Flagging**: Detects exact and similar phrases using `SentenceTransformers`
-  **Severity Classification**: Classifies segments as `Safe`, `Warning`, or `Critical`
-  **Redacted Output**: Masks sensitive content as `[REDACTED]`
-  **Natural Language Summary**: Outputs a simple summary of all flagged content
-  **Offline-First**: Runs 100% locally using open-source models only

---

##  Setup Instructions

### 1.  Prerequisites

- macOS or Linux
- Python **3.10+**
- [ffmpeg](https://ffmpeg.org/download.html)

### 2.  Installation

```bash
# Clone the repo
git clone https://github.com/yourname/smart-audio-firewall.git
cd smart-audio-firewall

# Create and activate virtual environment
python3.10 -m venv env
source env/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Install ffmpeg (for pydub to handle mp3)
brew install ffmpeg

