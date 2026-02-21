"""GET /items — list items for a user, optionally filtered by state."""

from __future__ import annotations

from fastapi import APIRouter
from models import Item
from services.firestore_repo import list_items

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/{user_id}", response_model=list[Item])
async def get_items(user_id: str, state: str | None = None) -> list[Item]:
    """Return all items for a user, optionally filtered by state."""
    return await list_items(user_id, state)
