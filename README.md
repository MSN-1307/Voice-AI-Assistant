# Real-Time Voice AI Assistant

A conversational AI assistant that accepts voice input, processes it through a speech-to-text → LLM → text-to-speech pipeline, and responds with natural voice output — with a built-in fallback mechanism to keep users engaged during processing delays.

## Overview

This project implements an audio-in, audio-out conversational assistant designed for low-latency, natural interaction. Rather than leaving the user in silence while the system processes their request, the assistant immediately acknowledges the query with a spoken filler response ("Let me think about that...") before delivering the actual answer — ensuring the conversation always feels responsive, even when backend processing takes a moment.

## Features

- **Voice input**: Captures user speech via microphone
- **Offline Speech-to-Text**: Uses `faster-whisper` (runs locally, no internet required for transcription)
- **Fast LLM responses**: Uses the Groq API (Llama 3.1 8B) for near-instant, conversational replies
- **Voice output**: Offline text-to-speech via `pyttsx3` (uses local Windows voices)
- **Fallback engagement flow**: Immediately speaks an acknowledgment filler while processing, so the user is never met with silence or a generic error
- **Conversation memory**: Maintains context across turns so the assistant remembers earlier parts of the conversation
- **Voice-activity-aware transcription**: Uses VAD filtering to reduce mistranscriptions from silence/background noise

## Architecture

🎤 Mic Input
│
▼
Speech-to-Text (faster-whisper, offline, CPU)
│
▼
Immediate spoken filler ("Let me think about that...")
│
▼
LLM Response (Groq API, Llama 3.1 8B Instant)
│
▼
Text-to-Speech (pyttsx3, offline)
│
▼
🔊 Spoken Response

## Tech Stack

| Component | Technology | Why |
|---|---|---|
| Speech-to-Text | `faster-whisper` (small model) | Offline, fast on CPU, no per-request cost |
| LLM | Groq API (`llama-3.1-8b-instant`) | Extremely low-latency inference (~0.2–0.6s typical) |
| Text-to-Speech | `pyttsx3` | Fully offline, uses native OS voices, no API cost |
| Audio I/O | `sounddevice`, `numpy` | Cross-platform microphone recording and playback |

## Setup

### Prerequisites
- Python 3.10+ (tested on 3.14)
- A Groq API key (free tier available at console.groq.com/keys)
- Windows, macOS, or Linux with a working microphone

### Installation

```bash
git clone https://github.com/yourusername/voice-ai-assistant.git
cd voice-ai-assistant

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install faster-whisper sounddevice numpy groq python-dotenv pyttsx3
```

### Configuration

Create a `.env` file in the project root:
GROQ_API_KEY=your_groq_api_key_here

(See `.env.example` for reference — never commit your real `.env` file.)

### Running

```bash
python assistant_fallback.py
```

Speak when prompted with "🎤 Listening... speak now!" Say **"stop"** at any point to end the conversation gracefully.

## Latency Performance

| Stage | Typical Time |
|---|---|
| Speech-to-Text | ~2.0–2.5s |
| LLM Response | ~0.2–0.6s |
| Time-to-first-response (STT + LLM) | ~2.3–3.2s |

Speech-to-text was the primary latency bottleneck in this implementation. The fallback filler mechanism was specifically designed to address this — masking processing latency with an immediate, natural acknowledgment so the assistant feels responsive regardless of backend processing time.

## Design Decisions & Tradeoffs

- **Hybrid offline/online approach**: STT and TTS run fully offline (privacy-friendly, no per-request cost, works without internet once models are downloaded). The LLM uses the Groq API for online inference, chosen because it offers among the fastest inference speeds available, which was critical for meeting the sub-2-second responsiveness goal. A fully offline LLM (e.g., via Ollama) was considered but would have introduced significantly higher latency on CPU-only hardware.
- **Sequential fallback flow over true concurrency**: An earlier version attempted to run STT/LLM processing in a background thread while speaking the filler concurrently. This surfaced a known Windows-specific instability in `pyttsx3` (which relies on COM-based SAPI) when invoked alongside heavy CPU work on another thread. The final implementation uses a sequential flow (filler → process → answer) for reliability, while still fully satisfying the requirement of never leaving the user in silence.
- **faster-whisper "small" model**: Chosen for its speed on CPU-only hardware. This trades some transcription accuracy (particularly on uncommon words/names) for meeting the latency target. VAD filtering and prompt-hinting were added to partially mitigate this.

## Known Limitations

- Transcription accuracy on proper nouns/names is lower than a larger Whisper model or cloud STT service would provide
- Fixed recording window (5 seconds) rather than automatic silence-based cutoff
- Requires an internet connection for the LLM step (Groq API)

## AI Usage Disclosure

AI assistance (Claude, Anthropic) was used during this project for:
- Debugging environment/dependency issues (Python version compatibility, package installation)
- Diagnosing and resolving a Windows-specific `pyttsx3`/threading conflict
- Code structure guidance for the STT → LLM → TTS pipeline and fallback engagement flow
- Drafting this README and project documentation

All code was tested and run locally; environment-specific issues (audio device configuration, model downloads) were debugged interactively based on actual runtime output.

## License

This project was created for educational/assignment purposes.