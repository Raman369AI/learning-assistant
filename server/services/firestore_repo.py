"""Firestore repository helpers.

Uses the Firestore emulator when FIRESTORE_EMULATOR_HOST is set,
otherwise connects to the real GCP project.
"""

from __future__ import annotations

import os
from typing import Optional

from google.cloud import firestore  # type: ignore[import-untyped]

from models import (
    Item, Session, Digest, Connection, ResearchJob, UserProfile
)

_client: Optional[firestore.AsyncClient] = None


def get_db() -> firestore.AsyncClient:
    global _client
    if _client is None:
        project = os.getenv("GCP_PROJECT_ID", "demo-project")
        _client = firestore.AsyncClient(project=project)
    return _client


# ── Helpers ───────────────────────────────────────────────────────────────────

async def save_item(item: Item) -> Item:
    db = get_db()
    await db.collection("items").document(item.item_id).set(item.model_dump())
    return item


async def get_item(item_id: str) -> Optional[Item]:
    db = get_db()
    doc = await db.collection("items").document(item_id).get()
    if doc.exists:
        return Item(**doc.to_dict())
    return None


async def list_items(user_id: str, state: Optional[str] = None) -> list[Item]:
    db = get_db()
    query = db.collection("items").where("user_id", "==", user_id)
    if state:
        query = query.where("state", "==", state)
    docs = query.stream()
    return [Item(**d.to_dict()) async for d in docs]


async def save_research_job(job: ResearchJob) -> ResearchJob:
    db = get_db()
    await db.collection("research_jobs").document(job.job_id).set(job.model_dump())
    return job


async def get_research_job(job_id: str) -> Optional[ResearchJob]:
    db = get_db()
    doc = await db.collection("research_jobs").document(job_id).get()
    if doc.exists:
        return ResearchJob(**doc.to_dict())
    return None


async def update_research_job(job_id: str, **fields) -> None:
    db = get_db()
    await db.collection("research_jobs").document(job_id).update(fields)


async def save_digest(digest: Digest) -> Digest:
    db = get_db()
    await db.collection("digests").document(digest.digest_id).set(digest.model_dump())
    return digest


async def save_connection(conn: Connection) -> Connection:
    db = get_db()
    await db.collection("connections").document(conn.connection_id).set(conn.model_dump())
    return conn


async def list_connections(user_id: str) -> list[Connection]:
    db = get_db()
    docs = db.collection("connections").where("user_id", "==", user_id).stream()
    return [Connection(**d.to_dict()) async for d in docs]


async def list_users_with_monitoring() -> list[UserProfile]:
    """Fetch all user profiles that have at least one monitored topic."""
    db = get_db()
    docs = db.collection("users").stream()
    users = []
    async for d in docs:
        data = d.to_dict()
        prefs = data.get("preferences", {})
        if prefs.get("monitored_topics"):
            users.append(UserProfile(**data))
    return users


async def get_user_profile(user_id: str) -> Optional[UserProfile]:
    db = get_db()
    doc = await db.collection("users").document(user_id).get()
    if doc.exists:
        return UserProfile(**doc.to_dict())
    return None
