# Learning Assistant

A personal AI-powered learning assistant built with:
- **FastAPI** backend (Cloud Run ready)
- **Google ADK** — 6 specialised LlmAgents
- **Firestore** — stateless agent memory layer
- **Gemini 2.0 Flash** (most agents) + **Gemini 2.5 Pro** (Deep Research)

## Quick Start

```bash
cd server
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp ../.env.example .env   # fill in your GOOGLE_API_KEY + GCP_PROJECT_ID
uvicorn main:app --reload
```

API docs → http://localhost:8000/docs

## Agents

| Agent | Model | Trigger |
|---|---|---|
| Triage | Flash | `POST /capture` |
| Deep Research | Pro | `POST /research` (async) |
| Digest | Flash | `POST /digest/trigger` (scheduled) |
| Clarification | Flash | `POST /clarify` |
| Connection | Flash | `POST /connect` (scheduled) |
| Resurfacing | Flash | `POST /resurface` (scheduled) |

## Environment Variables

See `.env.example`.
