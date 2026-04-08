from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from agents.memory_agent_faiss import memory_agent
from agents.emotion_agent_transformer import emotion_agent
from agents.crisis_agent_transformer import crisis_agent
from agents.planner_agent_smart import planner_agent
from services.dbt_library import DBT_LIBRARY

app = FastAPI(title = "Agentic Pyschological Support MVP")

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    emotion: str
    distress: float
    strategy: str
    risk: bool
    response: str
    memories: List[str]



def therapy_agent(
    message: str,
    strategy: str,
    memories: List[str],
    intervention: Dict,
) -> str:
    memory_context = f" I also remember: {memories[0]}" if memories else ""

    steps = intervention.get("steps", [])
    prompt = intervention.get("prompt", "")

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
            + " Let’s try this: "
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

# Main Agentic Endpoint
@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    emotion_result = emotion_agent.analyze(request.message)

    crisis_result = crisis_agent.analyze(request.message)

    memories = memory_agent.search(request.message)

    plan = planner_agent.plan(
        emotion=emotion_result["emotion"],
        distress=emotion_result["distress"],
        risk=crisis_result["risk"],
        memories = memories,
    )

    strategy = plan["strategy"]
    intervention = plan["intervention"]

    response = therapy_agent(request.message, strategy, memories, intervention)

    # write latest memory
    memory_agent.add_memory(request.message)

    return ChatResponse(
        emotion=emotion_result["emotion"],
        distress=emotion_result["distress"],
        strategy=strategy,
        risk=crisis_result["risk"],
        response=response,
        memories=memories,
    )


@app.get("/")
def healthcheck():
    return {"status": "running", "service": "agentic-psych-support-mvp"}
