# AI KHEMRA BRO

> Khmer-first AI dubbing, subtitle translation, and speech tools.

AI KHEMRA BRO is a Khmer-focused Streamlit workstation for video transcription, subtitle translation, multilingual voice generation, and dubbing workflows.

## Features

- **Video → SRT:** transcribe uploaded video with Gemini and preserve timestamps.
- **AI Subtitle Translator:** translate SRT content while preserving cue timing and review the result before download.
- **SRT → Speech:** synthesize tagged subtitle dialogue into MP3 with Edge TTS and optional audio filters.
- **Text → Speech:** generate a single voice track from Khmer or multilingual text.
- **Mobile UI:** responsive four-tab layout, compact upload controls, and settings popover.
- **Owner tools:** optional license/session administration and encrypted backup workflows.

Supported subtitle formats include `.srt`, `.ass`, and `.vtt` where applicable. Video and audio processing uses FFmpeg.

## Streamlit Cloud setup

Add the following secrets in **App settings → Secrets**. The application supports multiple Gemini keys through a newline-separated value and rotates between valid keys when needed.

```toml
GEMINI_API_KEYS = "AIza..."
COOKIE_SECRET = "replace-with-a-long-random-secret"
```

For local development, the same values can be set in `.streamlit/secrets.toml` or supplied through the application settings. Never commit API keys, cookie secrets, customer access codes, or database backups to GitHub.

## Run locally

Install FFmpeg first, then install Python dependencies:

```bash
sudo apt-get update && sudo apt-get install -y ffmpeg
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit. The first transcription or speech-generation request may download model data and take longer than subsequent requests.

## Repository

- GitHub: [@kmr64681-create](https://github.com/kmr64681-create)
- Repository: [AI-KHEMRA-BRO](https://github.com/kmr64681-create/AI-KHEMRA-BRO)

> Built with a Khmer-first mindset.
