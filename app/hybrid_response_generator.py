from typing import List, Dict
from transformers import pipeline


class HybridResponseGenerator:
    """Planner-guided + memory-aware response generation.

    Flow:
    1. Planner selects strategy
    2. Memory retrieves prior context
    3. Controlled prompt is built
    4. Local LLM generates the final empathetic response

    This keeps safety + structure while improving natural language quality.
    """

    def __init__(self):
        # Lightweight local generation model for MVP
        self.generator = pipeline(
            "text2text-generation",
            model="google/flan-t5-base",
        )

    def _build_prompt(
        self,
        message: str,
        strategy: str,
        memories: List[str],
        intervention: Dict,
    ) -> str:
        memory_context = memories[0] if memories else "No prior memory available."
        steps = intervention.get("steps", []) if intervention else []
        prompt = intervention.get("prompt", "") if intervention else ""

        return f"""
You are a safe and empathetic psychological support assistant.

User current message:
{message}

Retrieved memory from previous conversations:
{memory_context}

Chosen therapeutic strategy:
{strategy}

Recommended DBT intervention steps:
{steps}

Reflection prompt:
{prompt}

Instructions:
- Respond with empathy and emotional validation.
- Be supportive, calm, and safe.
- Use the prior memory naturally if relevant.
- Do not sound robotic.
- Do not diagnose.
- If crisis strategy is selected, prioritize immediate safety.
- Keep response concise but warm.

Final response:
"""

    def generate(
        self,
        message: str,
        strategy: str,
        memories: List[str],
        intervention: Dict,
    ) -> str:
        if strategy == "crisis_escalation":
            return (
                "I'm really sorry you're going through this right now. "
                "Your safety matters most. Please reach out to a trusted person "
                "or local emergency mental health support immediately. "
                "You do not have to handle this alone."
            )

        prompt = self._build_prompt(
            message,
            strategy,
            memories,
            intervention,
        )

        result = self.generator(
            prompt,
            max_length=180,
            do_sample=True,
            temperature=0.7,
        )

        return result[0]["generated_text"].strip()


response_generator = HybridResponseGenerator()
