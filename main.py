import os
import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from emotion import detect_emotion
from tts_engine import synthesize, get_voice_params

os.makedirs("static", exist_ok=True)

app = FastAPI(title="Empathy Engine")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class AnalyzeRequest(BaseModel):
    text: str


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/analyze")
async def analyze(body: AnalyzeRequest):
    text = body.text.strip()
    if not text:
        return JSONResponse(status_code=400, content={"error": "Text must not be empty."})

    result = detect_emotion(text)
    emotion = result["emotion"]
    intensity = result["intensity"]

    output_path = "static/output.wav"
    synthesize(text, emotion, intensity, output_path)

    audio_url = f"/static/output.wav?t={int(time.time())}"
    voice_params = get_voice_params(emotion, intensity)

    return {
        "emotion": emotion,
        "intensity": round(intensity, 3),
        "audio_url": audio_url,
        "voice_params": voice_params,
    }
