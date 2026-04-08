from typing import Dict, List


class DBTLibrary:
    """Structured DBT intervention library for planner retrieval.

    This acts as an external therapeutic tools database that the planner
    can query instead of inventing interventions from scratch.
    """

    def __init__(self):
        self.interventions: Dict[str, Dict] = {
            "breathing_exercise": {
                "category": "distress_tolerance",
                "steps": [
                    "Inhale slowly for 4 seconds",
                    "Hold for 4 seconds",
                    "Exhale gently for 6 seconds",
                    "Repeat 5 times",
                ],
                "prompt": "Guide the user through paced breathing and then explore the stressor.",
            },
            "grounding_5_4_3_2_1": {
                "category": "mindfulness",
                "steps": [
                    "Name 5 things you can see",
                    "Name 4 things you can touch",
                    "Name 3 things you can hear",
                    "Name 2 things you can smell",
                    "Name 1 thing you can taste",
                ],
                "prompt": "Use sensory grounding to reduce anxiety and panic.",
            },
            "cognitive_reframing": {
                "category": "emotion_regulation",
                "steps": [
                    "Identify the distressing thought",
                    "Ask what evidence supports it",
                    "Ask what evidence challenges it",
                    "Rewrite the thought in a balanced way",
                ],
                "prompt": "Help the user challenge catastrophic thinking.",
            },
            "emotional_validation": {
                "category": "interpersonal_effectiveness",
                "steps": [
                    "Acknowledge the emotion",
                    "Normalize the experience",
                    "Invite the user to elaborate",
                ],
                "prompt": "Validate the feeling before moving to problem-solving.",
            },
            "crisis_escalation": {
                "category": "safety",
                "steps": [
                    "Acknowledge immediate pain",
                    "Encourage contacting a trusted person now",
                    "Provide crisis hotline / emergency resources",
                    "Ask if they are in immediate danger",
                ],
                "prompt": "Prioritize safety and immediate human support.",
            },
        }

    def get(self, strategy: str) -> Dict:
        return self.interventions.get(
            strategy,
            {
                "category": "support",
                "steps": ["Listen reflectively", "Ask an open-ended follow-up"],
                "prompt": "Provide reflective listening.",
            },
        )

    def list_strategies(self) -> List[str]:
        return list(self.interventions.keys())


# singleton instance
DBT_LIBRARY = DBTLibrary()
