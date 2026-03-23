"""SQLite repository for Learning Assistant local persistence."""

import json
from datetime import datetime
from typing import Optional

import aiosqlite
from models import (
    Item, Session, Digest, Connection, ResearchJob, UserProfile
)

DB_PATH = "store.db"

# Ensure table exists synchronously at module load time (conceptually) or rely on lazy init.
# Using a lazy init approach to match what was done with Firestore.
_db_initialized = False

async def _init_db():
    global _db_initialized
    if _db_initialized:
        return
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS store (
                collection TEXT,
                doc_id TEXT,
                data TEXT,
                PRIMARY KEY(collection, doc_id)
            )
        """)
        await db.commit()
    _db_initialized = True

async def _fs_set(collection: str, doc_id: str, data: dict) -> None:
    await _init_db()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR REPLACE INTO store (collection, doc_id, data) VALUES (?, ?, ?)",
            (collection, doc_id, json.dumps(data))
        )
        await db.commit()

async def _fs_get(collection: str, doc_id: str) -> dict | None:
    await _init_db()
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT data FROM store WHERE collection = ? AND doc_id = ?", 
            (collection, doc_id)
        ) as cursor:
            row = await cursor.fetchone()
            if row:
                return json.loads(row[0])
            return None

async def _fs_list(collection: str, filters: dict | None = None) -> list[dict]:
    await _init_db()
    async with aiosqlite.connect(DB_PATH) as db:
        # SQLite json1 extension: json_extract(data, '$.field')
        query = "SELECT data FROM store WHERE collection = ?"
        params = [collection]
        
        if filters:
            for k, v in filters.items():
                query += f" AND json_extract(data, '$.{k}') = ?"
                params.append(v)
                
        async with db.execute(query, params) as cursor:
            rows = await cursor.fetchall()
            return [json.loads(row[0]) for row in rows]

async def _fs_update(collection: str, doc_id: str, **fields) -> None:
    await _init_db()
    async with aiosqlite.connect(DB_PATH) as db:
        # Fetch current
        async with db.execute(
            "SELECT data FROM store WHERE collection = ? AND doc_id = ?", 
            (collection, doc_id)
        ) as cursor:
            row = await cursor.fetchone()
            if row:
                data = json.loads(row[0])
                data.update(fields)
                await db.execute(
                    "UPDATE store SET data = ? WHERE collection = ? AND doc_id = ?",
                    (json.dumps(data), collection, doc_id)
                )
                await db.commit()

# ── Public API (identical to firestore_repo.py) ──────────────────────────────

async def save_item(item: Item) -> Item:
    await _fs_set("items", item.item_id, item.model_dump())
    return item

async def delete_item(item_id: str) -> bool:
    await _init_db()
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "DELETE FROM store WHERE collection = 'items' AND doc_id = ?", (item_id,)
        )
        await db.commit()
        return cursor.rowcount > 0

async def get_item(item_id: str) -> Optional[Item]:
    data = await _fs_get("items", item_id)
    return Item(**data) if data else None

async def list_items(user_id: str, state: Optional[str] = None) -> list[Item]:
    filters: dict = {"user_id": user_id}
    if state:
        filters["state"] = state
    docs = await _fs_list("items", filters)
    return [Item(**d) for d in docs]

async def save_research_job(job: ResearchJob) -> ResearchJob:
    await _fs_set("research_jobs", job.job_id, job.model_dump())
    return job

async def get_research_job(job_id: str) -> Optional[ResearchJob]:
    data = await _fs_get("research_jobs", job_id)
    return ResearchJob(**data) if data else None

async def update_research_job(job_id: str, **fields) -> None:
    await _fs_update("research_jobs", job_id, **fields)

async def save_digest(digest: Digest) -> Digest:
    await _fs_set("digests", digest.digest_id, digest.model_dump())
    return digest

async def save_connection(conn: Connection) -> Connection:
    await _fs_set("connections", conn.connection_id, conn.model_dump())
    return conn

async def list_connections(user_id: str) -> list[Connection]:
    docs = await _fs_list("connections", {"user_id": user_id})
    return [Connection(**d) for d in docs]

async def list_users_with_monitoring() -> list[UserProfile]:
    docs = await _fs_list("users")
    users = []
    for d in docs:
        prefs = d.get("preferences", {})
        if prefs.get("monitored_topics"):
            users.append(UserProfile(**d))
    return users

async def get_user_profile(user_id: str) -> Optional[UserProfile]:
    data = await _fs_get("users", user_id)
    return UserProfile(**data) if data else None


# ── New Abstractions (removes get_db dependency from routers) ───────────────

async def get_latest_session_mood(user_id: str, item_id: str) -> str | None:
    """Used by resurface.py to replace Firestore stream sorted by started_at."""
    await _init_db()
    async with aiosqlite.connect(DB_PATH) as db:
        query = '''
            SELECT json_extract(data, '$.mood') 
            FROM store 
            WHERE collection = 'sessions' 
              AND json_extract(data, '$.user_id') = ? 
              AND json_extract(data, '$.item_id') = ?
            ORDER BY json_extract(data, '$.started_at') DESC 
            LIMIT 1
        '''
        async with db.execute(query, (user_id, item_id)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None

async def add_resurfacing_card(card: dict) -> None:
    """Used by resurface.py"""
    # use timestamp as a cheap doc_id if not provided
    doc_id = card.get("card_id", str(datetime.utcnow().timestamp()))
    await _fs_set("resurfacing_cards", doc_id, card)

async def get_recent_digests(user_id: str, limit: int = 10) -> list[dict]:
    """Used by digest.py to replace ordered stream."""
    await _init_db()
    async with aiosqlite.connect(DB_PATH) as db:
        query = '''
            SELECT data 
            FROM store 
            WHERE collection = 'digests' 
              AND json_extract(data, '$.user_id') = ?
            ORDER BY json_extract(data, '$.generated_at') DESC 
            LIMIT ?
        '''
        async with db.execute(query, (user_id, limit)) as cursor:
            rows = await cursor.fetchall()
            return [json.loads(row[0]) for row in rows]
