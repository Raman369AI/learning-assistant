"""POST /capture — Triage Agent endpoint."""

from __future__ import annotations

import json

from fastapi import APIRouter, HTTPException
from google.adk.runners import InMemoryRunner
from google.adk.sessions import InMemorySessionService
from google.genai import types as genai_types

from agents.triage_agent import triage_agent
from models import CaptureRequest, Item, ItemState, ItemType
from services.firestore_repo import save_item, get_user_profile

router = APIRouter(prefix="/capture", tags=["capture"])


@router.post("", response_model=Item)
async def capture(req: CaptureRequest) -> Item:
    """Brain-dump a URL or raw text. Returns a structured, tagged Item."""
    if not req.raw_text and not req.url:
        raise HTTPException(status_code=422, detail="Provide raw_text or url.")

    profile = await get_user_profile(req.user_id)
    existing_topics = (
        [t for g in profile.goals for t in g.topics] if profile else []
    )

    raw_input = req.raw_text or req.url or ""
    prompt = (
        f"User's existing topics: {existing_topics}\n\n"
        f"Captured content:\n{raw_input}"
    )

    runner = InMemoryRunner(agent=triage_agent, app_name="triage")
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="triage", user_id=req.user_id
    )

    result_text = ""
    async for event in runner.run_async(
        user_id=req.user_id,
        session_id=session.id,
        new_message=genai_types.Content(
            role="user", parts=[genai_types.Part(text=prompt)]
        ),
    ):
        if event.is_final_response() and event.content:
            result_text = event.content.parts[0].text

    try:
        data = json.loads(result_text)
    except json.JSONDecodeError:
        raise HTTPException(status_code=502, detail="Triage agent returned invalid JSON.")

    item = Item(
        user_id=req.user_id,
        type=ItemType(data.get("type", "topic")),
        state=ItemState(data.get("suggested_state", "brain_dump")),
        title=data.get("title", raw_input[:80]),
        tags=data.get("tags", []),
        source_url=req.url,
        effort_estimate=data.get("effort_estimate"),
        goal_id=data.get("goal_id"),
    )

    return await save_item(item)
