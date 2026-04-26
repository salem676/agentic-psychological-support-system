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
        result = self.classifier(message, self.labels)

        top_label = result["labels"][0]
        top_score = float(result["scores"][0])
        #modified from 0.55 to 0.80 to ensure not every case is a risk and created new logic schema
        if top_label == "self-harm or suicide risk":
            if top_score > 0.80:
                risk = True
                level = "high"
            elif top_score > 0.60:
                risk = False
                level = "medium"
            else:
                risk = False
                level = "low"
        else:
            risk = False
            level = "low"
        

        return {
            "risk": risk,
            "level": level,
            "confidence": round(top_score, 2),
        }


# singleton instance
crisis_agent = CrisisTransformerAgent()
