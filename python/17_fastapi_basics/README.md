# Lesson 17 — FastAPI Basics

## Overview

FastAPI is a modern Python web framework for building REST APIs. It's fast, auto-generates interactive docs, and uses Pydantic for data validation. If you've done lesson 16 (type hints), FastAPI will feel natural — your annotations *are* your API spec.

---

## Install

```bash
pip install fastapi uvicorn
```

- `fastapi` — the framework
- `uvicorn` — the ASGI server that runs it

---

## Running the App

```bash
uvicorn app:app --reload
```

- `app:app` — module name `app`, variable name `app` (the FastAPI instance)
- `--reload` — auto-restart on file changes (development only)

Then open: `http://127.0.0.1:8000`

**Interactive docs (auto-generated):**
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

---

## Your First Route

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello, World!"}
```

FastAPI serializes the return value to JSON automatically.

---

## Path Parameters

```python
@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id}

# GET /items/42 → {"item_id": 42}
# GET /items/abc → 422 Unprocessable Entity (FastAPI validates the type)
```

---

## Query Parameters

Any parameter not in the path becomes a query parameter:

```python
@app.get("/search")
def search(q: str, limit: int = 10, offset: int = 0):
    return {"query": q, "limit": limit, "offset": offset}

# GET /search?q=python&limit=5 → {"query": "python", "limit": 5, "offset": 0}
```

Optional query parameters use `| None` with a default of `None`:

```python
@app.get("/users")
def list_users(role: str | None = None):
    ...
```

---

## Request Bodies with Pydantic

Use Pydantic `BaseModel` to define and validate the JSON body of POST/PUT requests:

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True

@app.post("/items")
def create_item(item: Item):
    return {"created": item.name, "price": item.price}
```

FastAPI automatically:
- Reads the JSON body
- Validates field types
- Returns 422 with details if validation fails
- Shows the schema in `/docs`

---

## Response Models

Declare what the response looks like with `response_model`:

```python
class ItemResponse(BaseModel):
    id: int
    name: str
    price: float

@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int):
    return {"id": item_id, "name": "Widget", "price": 9.99}
```

This filters the response to only include declared fields — useful for hiding internal fields (like passwords).

---

## HTTP Methods

```python
@app.get("/items/{id}")     # Read
@app.post("/items")          # Create
@app.put("/items/{id}")      # Full update
@app.patch("/items/{id}")    # Partial update
@app.delete("/items/{id}")   # Delete
```

---

## Status Codes

```python
from fastapi import HTTPException
from fastapi import status

@app.get("/items/{item_id}")
def get_item(item_id: int):
    item = db.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    ...
```

---

## Dependency Injection

FastAPI has a lightweight DI system using `Depends`. Common use: shared DB sessions, auth checks:

```python
from fastapi import Depends

def get_db():
    db = create_session()
    try:
        yield db
    finally:
        db.close()

@app.get("/users")
def list_users(db = Depends(get_db)):
    return db.query(User).all()
```

---

## Pydantic Validation

```python
from pydantic import BaseModel, Field, field_validator

class User(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    age: int = Field(ge=0, le=150)    # ge=greater-or-equal, le=less-or-equal
    email: str

    @field_validator("email")
    @classmethod
    def email_must_contain_at(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("invalid email")
        return v.lower()
```

---

## Common Pitfalls

| Mistake | Fix |
|---------|-----|
| Using `python app.py` to run | Use `uvicorn app:app --reload` |
| Forgetting `--reload` during dev | Changes won't be picked up without it |
| Returning non-serializable types | Return dicts, Pydantic models, or primitives — not arbitrary objects |
| Mutable default in Pydantic model | Use `Field(default_factory=list)` instead of `= []` |
| `HTTPException` with wrong status | Import and use `status.HTTP_*` constants for clarity |

---

## Quick Reference Card

```bash
# Install
pip install fastapi uvicorn

# Run
uvicorn app:app --reload

# Docs
# http://127.0.0.1:8000/docs   (Swagger)
# http://127.0.0.1:8000/redoc  (ReDoc)
```

```python
from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, Field

app = FastAPI()

# Route
@app.get("/path/{id}")
def handler(id: int, q: str | None = None):
    return {"id": id, "q": q}

# Request body
class ItemIn(BaseModel):
    name: str
    price: float = Field(gt=0)

@app.post("/items", status_code=status.HTTP_201_CREATED)
def create(item: ItemIn):
    return item

# 404
raise HTTPException(status_code=404, detail="not found")

# Dependency
def get_db(): yield session
@app.get("/data")
def data(db=Depends(get_db)): ...
```
