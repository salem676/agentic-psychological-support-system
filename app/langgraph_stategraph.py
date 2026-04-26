from typing import TypedDict, List, Dict

from langgraph.graph import StateGraph, END

from hybrid_response_generator import response_generator
from agents.emotion_agent_transformer import emotion_agent
from agents.crisis_agent_transformer import crisis_agent
from agents.memory_agent_sentence_transformer_faiss import memory_agent
from agents.planner_agent_smart import planner_agent


class TherapyState(TypedDict, total=False):
    user_id: str
    message: str

    emotion_result: Dict
    crisis_result: Dict
    memories: List[str]

    strategy: str
    intervention: Dict
    response: str



# Graph nodes

def emotion_node(state: TherapyState):
    state["emotion_result"] = emotion_agent.analyze(state["message"])
    return state



def crisis_node(state: TherapyState):
    state["crisis_result"] = crisis_agent.analyze(state["message"])
    return state



def route_after_crisis(state: TherapyState):
    if state["crisis_result"]["risk"]:
        return "crisis_response"
    return "memory"



def memory_node(state: TherapyState):
    state["memories"] = memory_agent.search(
        state["user_id"],
        state["message"],
    )
    return state



def planner_node(state: TherapyState):
    plan = planner_agent.plan(
        emotion=state["emotion_result"]["emotion"],
        distress=state["emotion_result"]["distress"],
        risk=state["crisis_result"]["risk"],
        memories=state.get("memories", []),
    )

    state["strategy"] = plan["strategy"]
    state["intervention"] = plan["intervention"]
    return state



def response_node(state: TherapyState):
    state["response"] = response_generator.generate(
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



def crisis_response_node(state: TherapyState):
    state["strategy"] = "crisis_escalation"
    state["intervention"] = {
        "steps": [
            "Please contact a trusted person immediately.",
            "Reach out to local emergency mental health services.",
            "You do not have to handle this alone."
        ],
        "prompt": ""
    }

    state["response"] = therapy_agent(
        state["message"],
        state["strategy"],
        state.get("memories", []),
        state["intervention"],
    )

    memory_agent.add_memory(
        state["user_id"],
        state["message"],
    )

    return state

# True LangGraph StateGraph

def build_therapy_graph():
    workflow = StateGraph(TherapyState)

    workflow.add_node("emotion", emotion_node)
    workflow.add_node("crisis", crisis_node)
    workflow.add_node("memory", memory_node)
    workflow.add_node("planner", planner_node)
    workflow.add_node("response", response_node)
    workflow.add_node("crisis_response", crisis_response_node)

    workflow.set_entry_point("emotion")

    workflow.add_edge("emotion", "crisis")

    workflow.add_conditional_edges(
        "crisis",
        route_after_crisis,
        {
            "crisis_response": "crisis_response",
            "memory": "memory",
        },
    )

    workflow.add_edge("memory", "planner")
    workflow.add_edge("planner", "response")

    workflow.add_edge("response", END)
    workflow.add_edge("crisis_response", END)

    return workflow.compile()


therapy_graph = build_therapy_graph()


def run_therapy_graph(user_id: str, message: str):
    return therapy_graph.invoke(
        {
            "user_id": user_id,
            "message": message,
        }
    )
