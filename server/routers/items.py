"""GET /items — list items for a user, optionally filtered by state."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from models import Item
from services.sqlite_repo import list_items, delete_item

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/{user_id}", response_model=list[Item])
async def get_items(user_id: str, state: str | None = None) -> list[Item]:
    """Return all items for a user, optionally filtered by state."""
    return await list_items(user_id, state)


@router.delete("/{user_id}/{item_id}", status_code=204)
async def remove_item(user_id: str, item_id: str) -> None:
    """Permanently delete an item."""
    deleted = await delete_item(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
