from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from langgraph_orchestration import run_therapy_graph

app = FastAPI(title = "Agentic Pyschological Support MVP")

class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    emotion: str
    distress: float
    strategy: str
    risk: bool
    response: str
    memories: List[str]



# Main Agentic Endpoint
@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    result = run_therapy_graph(
            request.user_id,
            request.message
    )

    return ChatResponse(
        emotion=result["emotion_result"]["emotion"],
        distress=result["emotion_result"]["distress"],
        strategy=result["strategy"],
        risk=result["crisis_result"]["risk"],
        response=result["response"],
        memories=result.get("memories" ,[]),
    )


@app.get("/")
def healthcheck():
    return {"status": "running", "service": "agentic-psych-support-mvp"}
