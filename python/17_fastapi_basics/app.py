# ─────────────────────────────────────────────────────────────
#  Lesson 17 — FastAPI Basics
#  Install: pip install fastapi uvicorn
#  Run:     uvicorn app:app --reload
#  Docs:    http://127.0.0.1:8000/docs
# ─────────────────────────────────────────────────────────────

from __future__ import annotations

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Lesson 17 — FastAPI Demo", version="1.0.0")

# ── IN-MEMORY "DATABASE" ──────────────────────────────────────
# Stands in for a real database — see lesson 18 for SQLAlchemy.
_items: dict[int, dict] = {
    1: {"id": 1, "name": "Widget",  "price": 9.99,  "in_stock": True},
    2: {"id": 2, "name": "Gadget",  "price": 24.99, "in_stock": True},
    3: {"id": 3, "name": "Doohickey", "price": 4.49, "in_stock": False},
}
_next_id = 4


# ── PYDANTIC MODELS ───────────────────────────────────────────

class ItemCreate(BaseModel):
    """Request body for creating a new item."""
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0, description="Must be greater than 0")
    in_stock: bool = True


class ItemResponse(BaseModel):
    """Response shape — always includes id."""
    id: int
    name: str
    price: float
    in_stock: bool


class ItemUpdate(BaseModel):
    """All fields optional — only provided fields are updated."""
    name: str | None = None
    price: float | None = Field(default=None, gt=0)
    in_stock: bool | None = None


# ── ROOT ──────────────────────────────────────────────────────

@app.get("/")
def root() -> dict:
    """Health check — returns a welcome message."""
    return {"message": "FastAPI demo running", "docs": "/docs"}


# ── LIST ALL ITEMS ────────────────────────────────────────────

@app.get("/items", response_model=list[ItemResponse])
def list_items(
    in_stock: bool | None = None,
    limit: int = 10,
    offset: int = 0,
) -> list[dict]:
    """
    Return all items with optional filtering.

    - **in_stock**: filter by availability (omit for all)
    - **limit**: max items to return (default 10)
    - **offset**: items to skip (for pagination)
    """
    items = list(_items.values())
    if in_stock is not None:
        items = [i for i in items if i["in_stock"] == in_stock]
    return items[offset : offset + limit]


# ── GET ONE ITEM ──────────────────────────────────────────────

@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int) -> dict:
    """Return a single item by ID. Returns 404 if not found."""
    item = _items.get(item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found",
        )
    return item


# ── CREATE ITEM ───────────────────────────────────────────────

@app.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate) -> dict:
    """Create a new item. Returns the created item with its assigned ID."""
    global _next_id
    new_item = {"id": _next_id, **item.model_dump()}
    _items[_next_id] = new_item
    _next_id += 1
    return new_item


# ── PARTIAL UPDATE ────────────────────────────────────────────

@app.patch("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, updates: ItemUpdate) -> dict:
    """Partially update an item. Only provided fields are changed."""
    item = _items.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

    # Only update fields that were explicitly provided (not None)
    patch = updates.model_dump(exclude_none=True)
    item.update(patch)
    return item


# ── DELETE ITEM ───────────────────────────────────────────────

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int) -> None:
    """Delete an item. Returns 204 No Content on success."""
    if item_id not in _items:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    del _items[item_id]


# ── SEARCH ────────────────────────────────────────────────────

@app.get("/search", response_model=list[ItemResponse])
def search_items(q: str, max_price: float | None = None) -> list[dict]:
    """Search items by name substring, optionally filtered by max price."""
    results = [
        item for item in _items.values()
        if q.lower() in item["name"].lower()
    ]
    if max_price is not None:
        results = [i for i in results if i["price"] <= max_price]
    return results
