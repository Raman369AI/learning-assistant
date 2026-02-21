"""POST /resurface — daily spaced-repetition nudge job."""

from __future__ import annotations

import json
from datetime import datetime, timezone

from fastapi import APIRouter, BackgroundTasks
from google.adk.runners import InMemoryRunner
from google.adk.sessions import InMemorySessionService
from google.genai import types as genai_types

from agents.resurfacing_agent import resurfacing_agent
from models import ItemState
from services.firestore_repo import list_items, list_users_with_monitoring, get_db

router = APIRouter(prefix="/resurface", tags=["resurface"])


def _decay_score(completed_at: str, mood: str | None) -> int:
    """Higher score = more urgently needs review."""
    try:
        completed = datetime.fromisoformat(completed_at)
    except ValueError:
        return 50
    days_ago = (datetime.now(timezone.utc) - completed.replace(tzinfo=timezone.utc)).days
    base = min(days_ago * 3, 80)
    mood_bonus = {"hard": 15, "confusing": 20}.get(mood or "", 0)
    return min(base + mood_bonus, 100)


async def _run_resurface_for_user(user_id: str) -> None:
    done_items = await list_items(user_id, state=ItemState.done)
    if not done_items:
        return

    # Pull latest session mood per item from Firestore
    db = get_db()
    item_data = []
    for item in done_items:
        session_docs = (
            db.collection("sessions")
            .where("user_id", "==", user_id)
            .where("item_id", "==", item.item_id)
            .order_by("started_at", direction="DESCENDING")
            .limit(1)
            .stream()
        )
        mood = None
        async for s in session_docs:
            mood = s.to_dict().get("mood")

        decay = _decay_score(item.updated_at, mood)
        item_data.append({
            "item_id": item.item_id,
            "title": item.title,
            "completed_at": item.updated_at,
            "mood": mood,
            "decay_score": decay,
        })

    prompt = f"Items to evaluate:\n{json.dumps(item_data, indent=2)}"

    runner = InMemoryRunner(agent=resurfacing_agent, app_name="resurface")
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="resurface", user_id=user_id
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
        cards = json.loads(result_text)
        for card in cards:
            await db.collection("resurfacing_cards").add({
                **card,
                "user_id": user_id,
                "created_at": datetime.utcnow().isoformat(),
                "seen": False,
            })
    except Exception as exc:
        print(f"[resurface] failed for user={user_id}: {exc}")


@router.post("", status_code=202)
async def trigger_resurface(background_tasks: BackgroundTasks) -> dict:
    """Cloud Scheduler calls this daily to push spaced-repetition cards."""
    users = await list_users_with_monitoring()
    for user in users:
        background_tasks.add_task(_run_resurface_for_user, user.user_id)
    return {"queued_users": len(users)}
