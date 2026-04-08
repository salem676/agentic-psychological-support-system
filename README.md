Agentic Pyschological LLM-Based Support System

This is a agentic AI system intended for a structured psychological support, that combines transformer based emotional analysis, crisis detection,
FAISS semantic memory, DBT intervention retrieval, smart planning and a benchmark evaluation.

This project was designed as non-trivial multi-agent architecture that goes beyond a single LLM prompt by integrating multiple tools, databases and decision layers.

Its features:

\-Transformer Emotion Agent: it performs a semantic emotional state analysis.
-Transformer Crisis Agent: detects risk of self harm or suicide.
-FAISS Memory Agent: semantic retrieval over prior conversations.
-DBT Intervention Library: structured therapeutic tools database.
-Smart Planner Agent: orchestrates memory, emotion and safety.
-Therapy Agent: intervention execution and response generation.
Evaluation Harness: it has empathetic dialogues and safety benchmarks.
-Results dashboards: it has React metrics evaluation.



Architecture schema:



┌──────────────────────┐

│     User Message     │

└──────────┬───────────┘

&#x20;          │

&#x20;          ▼

┌──────────────────────┐

│ Emotion Transformer  │

│  - emotion label     │

│  - distress score    │

└──────────┬───────────┘

&#x20;          │

&#x20;          ▼

┌──────────────────────┐

│ Crisis Transformer   │

│  - suicide risk      │

│  - escalation flag   │

└──────────┬───────────┘

&#x20;          │

&#x20;          ▼

┌──────────────────────┐

│  FAISS Memory Agent  │◄──────────────┐

│ semantic retrieval   │               │

└──────────┬───────────┘               │

&#x20;          │                           │

&#x20;          ▼                           │

┌──────────────────────┐               │

│ Smart Planner Agent  │               │

│ strategy selection   │               │

└──────────┬───────────┘               │

&#x20;          │                           │

&#x20;          ▼                           │

┌──────────────────────┐               │

│ DBT Tool Library     │               │

│ intervention steps   │               │

└──────────┬───────────┘               │

&#x20;          │                           │

&#x20;          ▼                           │

┌──────────────────────┐               │

│   Therapy Agent      │               │

│ response generation  │               │

└──────────┬───────────┘               │

&#x20;          │                           │

&#x20;          ▼                           │

┌──────────────────────┐               │

│  Response to User    │               │

└──────────┬───────────┘               │

&#x20;          │                           │

&#x20;          └──── write back memory ────┘



Project structure:



agentic-therapy-system/

│

├── app/

│   ├── main.py

│   ├── agents/

│   │   ├── emotion\_agent\_transformer.py

│   │   ├── crisis\_agent\_transformer.py

│   │   ├── memory\_agent\_faiss.py

│   │   └── planner\_agent\_smart.py

│   │

│   └── services/

│       └── dbt\_library.py

│

├── tests/

│   └── evaluation\_harness.py

│

├── frontend/

│   └── src/components/

│       └── ResultsDashboard.jsx

│

└── requirements.txt





How to run:

cd app

python -m uvicorn main:app --reload



To open UI:

http://127.0.0.1:8000/docs

