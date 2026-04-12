from typing import Dict
from transformers import pipeline


class CrisisTransformerAgent:
    """High-recall crisis risk detector for MVP.

    Uses zero-shot classification so we can detect self-harm / suicide intent
    beyond exact keyword matching.
    """

    def __init__(self):
        self.classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli",
        )
        self.labels = [
            "self-harm or suicide risk",
            "emotional distress only",
            "neutral conversation",
        ]

    def analyze(self, message: str) -> Dict:
        result = self.classifier(message,
                                 self.labels,
                                 clean_up_tokenization_spaces = True)

        top_label = result["labels"][0]
        top_score = float(result["scores"][0])

        risk = top_label == "self-harm or suicide risk" and top_score > 0.55

        level = "high" if risk and top_score > 0.8 else "medium" if risk else "low"

        return {
            "risk": risk,
            "level": level,
            "confidence": round(top_score, 2),
        }


# singleton instance
crisis_agent = CrisisTransformerAgent()
