# 🎙 Empathy Engine

> AI-powered emotional text-to-speech — detects the emotion in any sentence and speaks it back with a voice tuned to match.

Empathy Engine combines a fine-tuned transformer emotion classifier with offline speech synthesis to produce expressive, emotionally aware audio from plain text. Paste a sentence, hit **Analyze & Speak**, and hear the difference between a joyful announcement and an angry complaint — without any API keys or cloud services.

---

## Demo

| Input | Detected Emotion | Rate | Volume |
|---|---|---|---|
| *"I just got promoted!"* | joy (94%) | 231 wpm | 1.00 |
| *"This is unacceptable."* | anger (87%) | 200 wpm | 1.00 |
| *"I don't think I can handle this."* | fear (79%) | 159 wpm | 0.89 |
| *"Meeting at 3pm tomorrow."* | neutral (96%) | 175 wpm | 1.00 |

---

## Features

- **7-class emotion detection** — joy, surprise, anger, sadness, fear, disgust, neutral
- **Intensity-scaled voice params** — rate and volume shift continuously with model confidence
- **Two UIs** — FastAPI + Jinja2 web app **and** a Streamlit app (pick your preferred stack)
- **100% offline after first run** — pyttsx3 uses the OS-native TTS engine (no API keys)
- **Instant audio playback** — browser audio player auto-plays the synthesised WAV

---

## Tech Stack

| Layer | Library |
|---|---|
| Emotion model | `j-hartmann/emotion-english-distilroberta-base` via HuggingFace Transformers |
| Speech synthesis | `pyttsx3` (SAPI5 / espeak / NSSpeechSynthesizer) |
| Web backend | FastAPI + Uvicorn |
| Web frontend | Vanilla HTML/CSS/JS (Jinja2 template) |
| Alternative UI | Streamlit |

---

## Prerequisites

- Python 3.9+
- **Linux only** — install espeak before running:
  ```bash
  sudo apt-get install espeak espeak-data libespeak1 libespeak-dev
  ```
- Windows and macOS work out of the box.

---

## Installation

```bash
git clone https://github.com/saagr3214/empathy-engine.git
cd empathy-engine

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

> The HuggingFace model (~300 MB) downloads automatically on first run.
> The terminal will print `Loading emotion model…` while this happens.

---

## Running

### FastAPI (web app)
```bash
uvicorn main:app --reload
```
Open **http://localhost:8000**

### Streamlit
```bash
streamlit run streamlit_app.py
```
Open **http://localhost:8501**

---

## Project Structure

```
empathy_engine/
├── main.py            # FastAPI app — routes, request validation
├── streamlit_app.py   # Streamlit UI
├── emotion.py         # Emotion classifier (HuggingFace pipeline)
├── tts_engine.py      # pyttsx3 synthesis + voice parameter mapping
├── templates/
│   └── index.html     # Single-page UI for FastAPI
├── static/            # Runtime WAV output directory
└── requirements.txt
```

---

## Emotion → Voice Mapping

| Emotion  | Rate delta (wpm)   | Volume delta                        |
|----------|--------------------|-------------------------------------|
| joy      | +60 × intensity    | capped at 1.0                       |
| surprise | +40 × intensity    | 1.0 (fixed)                         |
| anger    | +30 × intensity    | capped at 1.0                       |
| sadness  | −50 × intensity    | max(0.75 + 0.1×(1−intensity), 0.6)  |
| fear     | −20 × intensity    | max(0.85, 0.7 + 0.15×intensity)     |
| disgust  | −10 × intensity    | 0.9 (fixed)                         |
| neutral  | 0 (base = 175)     | 1.0 (fixed)                         |

Base rate: **175 wpm** — all deltas scale with the model's confidence score (`intensity`).

---

## Design Choices

**Why `j-hartmann/emotion-english-distilroberta-base`?**
Fine-tuned on a diverse mix of emotion datasets for exactly 7 classes. Fast enough for real-time web use (~100 ms inference on CPU) while being meaningfully more nuanced than a simple positive/negative sentiment classifier.

**Why intensity scaling instead of fixed presets?**
A barely-angry sentence shouldn't sound as intense as a furious one. Scaling voice parameters continuously by the model's confidence score creates a natural expressive range rather than binary switches.

**Why pyttsx3?**
Zero cloud dependency — synthesis works offline using the OS-native engine. `engine.stop()` is called after every synthesis to cleanly tear down the background thread and prevent resource leaks across HTTP requests.

---

## License

MIT
