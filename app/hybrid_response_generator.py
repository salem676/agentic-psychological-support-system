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
            model="google/flan-t5-large",
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
        User message:
        {message}

        Relevant prior memory:
        {memory_context}

        Support strategy:
        {strategy}

        Helpful intervention:
        {prompt}

        Write a short warm supportive therapeutic response.
        Only write the final response.
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
            max_new_tokens=80,
            do_sample=True,
            temperature=0.7,
        )
        
        full_output = result[0]["generated_text"]

        response = full_output.replace(prompt, "").strip()

        #if not response:
            #response = ("It sounds like this situation is weighing heavily on you." "Let's take a small step together and focus on what feels most difficult right now.")
        
        return response


response_generator = HybridResponseGenerator()
