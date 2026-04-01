from transformers import pipeline

print("Loading emotion model...")
classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=1
)


def detect_emotion(text: str) -> dict:
    results = classifier(text)
    # top_k=1 returns a list of lists: [[{"label": ..., "score": ...}]]
    top = results[0][0]
    return {"emotion": top["label"].lower(), "intensity": top["score"]}
