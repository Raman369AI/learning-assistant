"""Learning Assistant — FastAPI application entry point."""

from __future__ import annotations

import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from routers import capture, research, clarify, digest, items, connect, resurface


@asynccontextmanager
async def lifespan(app: FastAPI):
    from seed_roadmap import seed_roadmap
    print("🚀 Learning Assistant API starting up…")
    await seed_roadmap()
    yield
    print("🛑 Learning Assistant API shutting down…")


app = FastAPI(
    title="Learning Assistant API",
    version="0.1.0",
    description=(
        "Personal learning assistant with 6 ADK agents: "
        "Triage, Deep Research, Digest, Clarification, Connection, Resurfacing."
    ),
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(capture.router)
app.include_router(research.router)
app.include_router(clarify.router)
app.include_router(digest.router)
app.include_router(items.router)
app.include_router(connect.router)
app.include_router(resurface.router)


@app.get("/", tags=["health"])
async def root() -> dict:
    return {
        "status": "ok",
        "service": "learning-assistant",
        "endpoints": [
            "POST /capture",
            "POST /research",
            "GET  /research/{job_id}",
            "POST /clarify",
            "POST /digest/trigger",
            "GET  /digest/{user_id}",
            "GET  /items/{user_id}",
            "POST /connect",
            "GET  /connect/{user_id}",
            "POST /resurface",
        ],
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
