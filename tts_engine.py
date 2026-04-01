import pyttsx3
import os

BASE_RATE = 175
BASE_VOLUME = 1.0


def get_voice_params(emotion: str, intensity: float) -> dict:
    if emotion == "joy":
        rate = BASE_RATE + int(60 * intensity)
        volume = min(1.0 + 0.1 * intensity, 1.0)
    elif emotion == "surprise":
        rate = BASE_RATE + int(40 * intensity)
        volume = 1.0
    elif emotion == "anger":
        rate = BASE_RATE + int(30 * intensity)
        volume = min(1.0 + 0.15 * intensity, 1.0)
    elif emotion == "sadness":
        rate = BASE_RATE - int(50 * intensity)
        volume = max(0.75 + 0.1 * (1 - intensity), 0.6)
    elif emotion == "fear":
        rate = BASE_RATE - int(20 * intensity)
        volume = max(0.85, 0.7 + 0.15 * intensity)
    elif emotion == "disgust":
        rate = BASE_RATE - int(10 * intensity)
        volume = 0.9
    else:  # neutral
        rate = BASE_RATE
        volume = 1.0

    return {"rate": rate, "volume": round(volume, 4)}


def synthesize(text: str, emotion: str, intensity: float, output_path: str) -> str:
    engine = pyttsx3.init()
    params = get_voice_params(emotion, intensity)
    engine.setProperty("rate", params["rate"])
    engine.setProperty("volume", params["volume"])
    engine.save_to_file(text, output_path)
    engine.runAndWait()
    engine.stop()
    return output_path
