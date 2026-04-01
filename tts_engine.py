from gtts import gTTS

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
    params = get_voice_params(emotion, intensity)

    # Map rate (wpm) to speed multiplier (0.5–2.0)
    # Baseline 175 wpm → speed 1.0
    speed_multiplier = params["rate"] / BASE_RATE
    speed_multiplier = max(0.5, min(2.0, speed_multiplier))  # clamp to valid range

    tts = gTTS(text=text, lang='en', slow=(speed_multiplier < 0.9))
    tts.save(output_path)
    return output_path
