Agentic Pyschological LLM-Based Support System



This is an agentic AI system intended for structured psychological support that combines transformer-based emotional analysis, crisis detection, semantic FAISS memory, DBT intervention retrieval, smart planning, LangGraph orchestration, and hybrid response generation.



This project was designed as a non-trivial multi-agent architecture that goes beyond a single LLM prompt by integrating multiple tools, databases, retrieval systems, and decision layers.



Unlike a standard chatbot, this system uses persistent memory, crisis routing, therapeutic planning, and controlled LLM generation to provide safer and more personalized support.



Its features:

\-Transformer Emotion Agent: performs semantic emotional state analysis.

\-Transformer Crisis Agent: detects risk of self-harm or suicide using graded escalation levels (low, medium, high).

\-Semantic FAISS Memory Agent: performs semantic retrieval over prior conversations using sentence-transformer embeddings.

\-Multi-User Persistent Memory: each user has isolated long-term memory across sessions.

\-DBT Intervention Library: structured therapeutic tools database for safer intervention planning.

\-Smart Planner Agent: orchestrates memory, emotion, crisis detection, and strategy selection.

\-True LangGraph StateGraph: handles explicit graph-based orchestration and conditional crisis routing.

\-Hybrid Response Generator: combines planner guidance + memory + DBT + controlled LLM generation.

\-Evaluation Harness: includes EmpatheticDialogues, CounselChat, and crisis safety benchmarks.

\-Human Evaluation Protocol: evaluates empathy, helpfulness, safety, and personalization.

\-Results Dashboard: React-based metrics evaluation and visualization.



Models used:



\-distilbert-base-uncased-finetuned-sst-2-english -> emotion analysis

\-facebook/bart-large-mnli -> crisis detection

\-all-MiniLM-L6-v2 -> semantic memory embeddings

\-google/flan-t5-base -> hybrid response generation


Architecture Schema:

┌──────────────────────────────┐
│        User Message          │
└────────────┬─────────────────┘
             │
             ▼
┌──────────────────────────────┐
│   Emotion Transformer        │
│   - emotion label            │
│   - distress score           │
└────────────┬─────────────────┘
             │
             ▼
┌──────────────────────────────┐
│   Crisis Transformer         │
│   - suicide risk             │
│   - escalation level         │
└────────────┬─────────────────┘
             │
             ▼

        Conditional Routing

   HIGH RISK:
   ┌──────────────────────────┐
   │   Crisis Response        │
   │   - emergency support    │
   │   - immediate escalation │
   └────────────┬─────────────┘
                │
                ▼
               END

   NORMAL PATH:
             │
             ▼
┌──────────────────────────────┐◄──────────────┐
│ Semantic FAISS Memory Agent  │               │
│ - semantic retrieval         │               │
│ - persistent user memory     │               │
└────────────┬─────────────────┘               │
             │                                 │
             ▼                                 │
┌──────────────────────────────┐               │
│ Smart Planner Agent          │               │
│ - strategy selection         │               │
└────────────┬─────────────────┘               │
             │                                 │
             ▼                                 │
┌──────────────────────────────┐               │
│ DBT Tool Library             │               │
│ - intervention steps         │               │
└────────────┬─────────────────┘               │
             │                                 │
             ▼                                 │
┌──────────────────────────────┐               │
│ Hybrid Response Generator    │               │
│ - planner-guided LLM reply   │               │
└────────────┬─────────────────┘               │
             │                                 │
             ▼                                 │
┌──────────────────────────────┐               │
│ Response to User             │               │
└────────────┬─────────────────┘               │
             │                                 │
             └──── write back memory ──────────┘

Project Structure



agentic-therapy-system/



├── app/

│ ├── main.py

│ ├── langgraph\_stategraph.py

│ ├── hybrid\_response\_generator.py

│ │

│ ├── agents/

│ │ ├── emotion\_agent\_transformer.py

│ │ ├── crisis\_agent\_transformer.py

│ │ ├── memory\_agent\_sentence\_transformer\_faiss.py

│ │ └── planner\_agent\_smart.py

│ │

│ └── services/

│ └── dbt\_library.py

│

├── tests/

│ └── evaluation\_harness.py

│

├── frontend/

│ └── src/components/

│ └── ResultsDashboard.jsx

│

├── human\_evaluation\_protocol.md

│

└── requirements.txt



How to run:

cd app

python -m uvicorn main:app --reload



To open UI:

http://127.0.0.1:8000/docs

This opens the FastAPI Swagger UI for testing the /chat endpoint and validating the full agentic workflow.

