from typing import Dict
from transformers import pipeline


class EmotionTransformerAgent:
    """Emotion classifier using a transformer sentiment model.

    MVP choice:
    - Uses a lightweight sentiment model already compatible with your environment.
    - Maps sentiment labels into therapy-friendly emotional states.
    - Can later be upgraded to GoEmotions-style multi-label emotion models.
    """

    def __init__(self):
        self.classifier = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
        )

    def analyze(self, message: str) -> Dict:
        result = self.classifier(message,
                                 clean_up_tokenization_spaces = True,
                                 )[0]
        label = result["label"].lower()
        score = float(result["score"])

        if label == "negative":
            return {
                "emotion": "distress",
                "distress": round(max(0.6, score), 2),
            }

        return {
            "emotion": "calm",
            "distress": round(1 - score, 2),
        }


# singleton instance
emotion_agent = EmotionTransformerAgent()
