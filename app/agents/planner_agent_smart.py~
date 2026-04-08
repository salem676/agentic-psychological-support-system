from typing import List, Dict
from services.dbt_library import DBT_LIBRARY


class SmartPlannerAgent:
    """Decision-making planner that combines emotion, risk, and memory context.

    This is the orchestration brain of the agentic system.
    """

    def plan(
        self,
        emotion: str,
        distress: float,
        risk: bool,
        memories: List[str],
    ) -> Dict:
        # 1) Safety first
        if risk:
            strategy = "crisis_escalation"
            return {
                "strategy": strategy,
                "intervention": DBT_LIBRARY.get(strategy),
                "reason": "Crisis risk detected",
            }

        # 2) Memory-informed planning
        memory_blob = " ".join(memories).lower() if memories else ""

        if "exam" in memory_blob or "final" in memory_blob:
            strategy = "cognitive_reframing"
            reason = "Recurring academic stress detected from memory"
        elif distress >= 0.8:
            strategy = "breathing_exercise"
            reason = "High distress requires immediate regulation"
        elif emotion in ["distress", "sadness"]:
            strategy = "emotional_validation"
            reason = "Negative emotional state requires validation"
        else:
            strategy = "grounding_5_4_3_2_1"
            reason = "Default mindfulness grounding"

        return {
            "strategy": strategy,
            "intervention": DBT_LIBRARY.get(strategy),
            "reason": reason,
        }


# singleton instance
planner_agent = SmartPlannerAgent()
