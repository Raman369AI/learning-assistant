"""POST /connect — weekly connection discovery job.
GET  /connect/{user_id} — read saved connections.
"""

from __future__ import annotations

import json

from fastapi import APIRouter, BackgroundTasks
from google.adk.runners import InMemoryRunner
from google.adk.sessions import InMemorySessionService
from google.genai import types as genai_types

from agents.connection_agent import connection_agent
from models import Connection, ConnectionStrength
from services.firestore_repo import (
    list_items,
    list_connections,
    save_connection,
    list_users_with_monitoring,
)

router = APIRouter(prefix="/connect", tags=["connect"])


async def _run_connections_for_user(user_id: str) -> None:
    items = await list_items(user_id, state="done")
    items += await list_items(user_id, state="in_progress")
    if len(items) < 2:
        return

    items_summary = "\n".join(
        f"- id={it.item_id} title={it.title} tags={it.tags}" for it in items
    )
    prompt = f"User items:\n{items_summary}"

    runner = InMemoryRunner(agent=connection_agent, app_name="connect")
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="connect", user_id=user_id
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
        connections_data = json.loads(result_text)
        for c in connections_data:
            conn = Connection(
                user_id=user_id,
                item_id_a=c["item_id_a"],
                item_id_b=c["item_id_b"],
                rationale=c["rationale"],
                strength=ConnectionStrength(c.get("strength", "moderate")),
            )
            await save_connection(conn)
    except Exception as exc:
        print(f"[connect] failed for user={user_id}: {exc}")


@router.post("", status_code=202)
async def trigger_connections(background_tasks: BackgroundTasks) -> dict:
    """Cloud Scheduler calls this weekly to discover new connections."""
    users = await list_users_with_monitoring()
    for user in users:
        background_tasks.add_task(_run_connections_for_user, user.user_id)
    return {"queued_users": len(users)}


@router.get("/{user_id}", response_model=list[Connection])
async def get_connections(user_id: str) -> list[Connection]:
    return await list_connections(user_id)
