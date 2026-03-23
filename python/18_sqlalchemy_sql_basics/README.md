# Lesson 18 — SQLAlchemy & SQL Basics

## Overview

SQLAlchemy is the standard Python ORM (Object-Relational Mapper). It lets you work with databases using Python classes instead of raw SQL strings. This lesson uses SQLite (built into Python — no server needed) and SQLAlchemy 2.x style.

---

## Install

```bash
pip install sqlalchemy
```

SQLite requires no extra install — it's part of Python's standard library.

---

## Core Concepts

| Term | Meaning |
|------|---------|
| **Engine** | Connection factory — knows the DB URL and driver |
| **Session** | Unit of work — tracks objects, issues queries, handles transactions |
| **Model** | Python class mapped to a database table |
| **ORM** | Object-Relational Mapper — maps rows ↔ Python objects |

---

## Setup: Engine and Base

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session

# SQLite file-based database
engine = create_engine("sqlite:///app.db", echo=False)

# In-memory SQLite (useful for tests — gone when engine is closed)
engine = create_engine("sqlite:///:memory:")

class Base(DeclarativeBase):
    pass   # all models inherit from this
```

---

## Defining Models

```python
from sqlalchemy import String, Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(200), unique=True)

    # One-to-many: one user has many posts
    posts: Mapped[list["Post"]] = relationship(back_populates="author")

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name!r})"

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    body: Mapped[str] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    author: Mapped["User"] = relationship(back_populates="posts")
```

`Mapped[T]` + `mapped_column(...)` is the SQLAlchemy 2.x style. It's type-hint-friendly and works with mypy.

---

## Create Tables

```python
Base.metadata.create_all(engine)
```

This creates all tables defined in models that haven't been created yet. Safe to call multiple times.

---

## CRUD Operations

### Create

```python
with Session(engine) as session:
    user = User(name="Alice", email="alice@example.com")
    session.add(user)
    session.commit()
    session.refresh(user)   # reload to get the auto-assigned id
    print(user.id)          # 1
```

### Read

```python
from sqlalchemy import select

with Session(engine) as session:
    # Get by primary key
    user = session.get(User, 1)

    # Select with filter
    stmt = select(User).where(User.name == "Alice")
    result = session.execute(stmt).scalars().all()

    # All rows
    all_users = session.execute(select(User)).scalars().all()
```

### Update

```python
with Session(engine) as session:
    user = session.get(User, 1)
    user.email = "newalice@example.com"   # modify the object
    session.commit()                       # change is committed automatically
```

### Delete

```python
with Session(engine) as session:
    user = session.get(User, 1)
    session.delete(user)
    session.commit()
```

---

## Querying

```python
from sqlalchemy import select, and_, or_, desc, func

with Session(engine) as session:
    # WHERE
    stmt = select(User).where(User.name == "Alice")

    # AND / OR
    stmt = select(User).where(and_(User.name == "Alice", User.id > 0))

    # ORDER BY
    stmt = select(User).order_by(desc(User.name))

    # LIMIT / OFFSET
    stmt = select(User).limit(10).offset(20)

    # COUNT
    count = session.execute(select(func.count(User.id))).scalar()

    # LIKE
    stmt = select(User).where(User.name.like("A%"))

    # JOIN (automatic via relationship)
    stmt = select(User).join(User.posts).where(Post.title.like("%Python%"))

    results = session.execute(stmt).scalars().all()
```

---

## Relationships

```python
# Access related objects — SQLAlchemy loads them automatically (lazy by default)
with Session(engine) as session:
    user = session.get(User, 1)
    for post in user.posts:          # triggers a SELECT on posts
        print(post.title)

    post = session.get(Post, 1)
    print(post.author.name)          # follows the relationship back
```

---

## Using SQLAlchemy with FastAPI

The standard pattern is a `get_db` dependency that yields a session:

```python
from sqlalchemy.orm import Session
from fastapi import Depends

def get_db():
    with Session(engine) as session:
        yield session

@app.get("/users")
def list_users(db: Session = Depends(get_db)):
    return db.execute(select(User)).scalars().all()
```

---

## Raw SQL When You Need It

```python
from sqlalchemy import text

with Session(engine) as session:
    result = session.execute(
        text("SELECT id, name FROM users WHERE id = :uid"),
        {"uid": 1}
    )
    row = result.fetchone()
    print(row.id, row.name)
```

Use parameterized queries (`:param` syntax) — never string-format user input into SQL.

---

## Common Pitfalls

| Mistake | Fix |
|---------|-----|
| Accessing lazy-loaded relationships outside a session | Keep the session open while accessing `.posts`, `.author`, etc. |
| Forgetting `session.commit()` | Changes are not saved without committing |
| `session.refresh(obj)` after commit | Required if you need auto-generated fields (like `id`) after insert |
| String-formatting SQL | Use parameterized queries: `text("... :param")` with `{"param": val}` |
| Using SQLAlchemy 1.x style in 2.x | Use `select()` instead of `session.query()` in new code |

---

## Quick Reference Card

```python
from sqlalchemy import create_engine, select, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Session, Mapped, mapped_column, relationship

# Engine
engine = create_engine("sqlite:///app.db")
engine = create_engine("sqlite:///:memory:")  # in-memory for tests

# Model
class Base(DeclarativeBase): pass

class Thing(Base):
    __tablename__ = "things"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

Base.metadata.create_all(engine)

# Session CRUD
with Session(engine) as s:
    s.add(Thing(name="foo")); s.commit()               # create
    t = s.get(Thing, 1)                                # read by PK
    all_t = s.execute(select(Thing)).scalars().all()   # read all
    t.name = "bar"; s.commit()                         # update
    s.delete(t); s.commit()                            # delete

# Query
select(Thing).where(Thing.name == "foo").order_by(Thing.id).limit(10)
```
