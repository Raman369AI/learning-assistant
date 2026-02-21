"""POST /digest/trigger — batch digest run (called by Cloud Scheduler).
GET  /digest/{user_id} — retrieve latest digests for a user.
"""

from __future__ import annotations

import json

from fastapi import APIRouter, BackgroundTasks, HTTPException
from google.adk.runners import InMemoryRunner
from google.adk.sessions import InMemorySessionService
from google.genai import types as genai_types

from agents.digest_agent import digest_agent
from models import Digest, DigestEntry
from services.firestore_repo import (
    list_users_with_monitoring,
    save_digest,
    get_db,
)

router = APIRouter(prefix="/digest", tags=["digest"])


async def _run_digest_for_user(user_id: str, topic: str) -> None:
    """Background coroutine: runs Digest Agent for one user × topic."""
    prompt = f"User ID: {user_id}\nMonitored topic: {topic}"

    runner = InMemoryRunner(agent=digest_agent, app_name="digest")
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="digest", user_id=user_id
    )

    result_text = ""
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session.id,
        new_message=genai_types.Content(
            role="user", parts=[genai_types.Part(text=prompt)]
        ),
    ):
        if event.is_final_response() and event.content:
            result_text = event.content.parts[0].text

    try:
        data = json.loads(result_text)
        entries = [DigestEntry(**e) for e in data.get("entries", [])]
        if entries:
            digest = Digest(user_id=user_id, topic=topic, papers=entries)
            await save_digest(digest)
    except Exception as exc:
        print(f"[digest] failed for user={user_id} topic={topic}: {exc}")


@router.post("/trigger", status_code=202)
async def trigger_digest(background_tasks: BackgroundTasks) -> dict:
    """Cloud Scheduler calls this daily. Fans out to all monitored users."""
    users = await list_users_with_monitoring()
    count = 0
    for user in users:
        for topic in user.preferences.monitored_topics:
            background_tasks.add_task(_run_digest_for_user, user.user_id, topic)
            count += 1
    return {"queued_jobs": count}


@router.get("/{user_id}")
async def get_digests(user_id: str, limit: int = 10) -> list[dict]:
    """Return recent digests for a user."""
    db = get_db()
    docs = (
        db.collection("digests")
        .where("user_id", "==", user_id)
        .order_by("generated_at", direction="DESCENDING")
        .limit(limit)
        .stream()
    )
    return [d.to_dict() async for d in docs]
