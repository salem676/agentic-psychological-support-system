from typing import TypedDict, List, Dict

from agents.emotion_agent_transformer import emotion_agent
from agents.crisis_agent_transformer import crisis_agent
from agents.memory_agent_sentence_transformer_faiss import memory_agent
from agents.planner_agent_smart import planner_agent
from services.dbt_library import DBT_LIBRARY


class TherapyState(TypedDict, total=False):
    user_id: str
    message: str

    emotion_result: Dict
    crisis_result: Dict
    memories: List[str]

    strategy: str
    intervention: Dict
    response: str


def therapy_agent(message: str, strategy: str, memories: List[str], intervention: Dict) -> str:
    memory_context = f" I also remember: {memories[0]}" if memories else ""

    steps = intervention.get("steps", []) if intervention else []
    prompt = intervention.get("prompt", "") if intervention else ""

    if strategy == "crisis_escalation":
        return (
            "I’m really sorry you’re going through this right now. "
            "Your safety matters most. "
            + " ".join(steps)
            + memory_context
        )

    if strategy == "breathing_exercise":
        return (
            "It makes sense to feel overwhelmed. "
            + "Let’s try this: "
            + ", ".join(steps)
            + ". "
            + memory_context
        )

    if strategy == "emotional_validation":
        return (
            "Your feelings are valid. "
            + prompt
            + memory_context
        )

    return (
        "Thank you for sharing that with me. "
        + prompt
        + memory_context
    )


# Graph Nodes

def emotion_node(state: TherapyState) -> TherapyState:
    state["emotion_result"] = emotion_agent.analyze(state["message"])
    return state


def crisis_node(state: TherapyState) -> TherapyState:
    state["crisis_result"] = crisis_agent.analyze(state["message"])
    return state


def memory_node(state: TherapyState) -> TherapyState:
    state["memories"] = memory_agent.search(
        state["user_id"],
        state["message"],
    )
    return state


def planner_node(state: TherapyState) -> TherapyState:
    plan = planner_agent.plan(
        emotion=state["emotion_result"]["emotion"],
        distress=state["emotion_result"]["distress"],
        risk=state["crisis_result"]["risk"],
        memories=state.get("memories", []),
    )

    state["strategy"] = plan["strategy"]
    state["intervention"] = plan["intervention"]
    return state


def response_node(state: TherapyState) -> TherapyState:
    state["response"] = therapy_agent(
        state["message"],
        state["strategy"],
        state.get("memories", []),
        state.get("intervention", {}),
    )

    memory_agent.add_memory(
        state["user_id"],
        state["message"],
    )

    return state


# Simple Orchestrator (LangGraph-ready structure)

def run_therapy_graph(user_id: str, message: str) -> TherapyState:
    """
    MVP orchestration layer.

    This mirrors LangGraph node execution order and can be swapped
    later for a true langgraph.StateGraph implementation.
    """

    state: TherapyState = {
        "user_id": user_id,
        "message": message,
    }

    for node in [
        emotion_node,
        crisis_node,
        memory_node,
        planner_node,
        response_node,
    ]:
        state = node(state)

    return state
