# ─────────────────────────────────────────────────────────────
#  Lesson 18 — SQLAlchemy & SQL Basics
#  Run: python3 main.py
#  Install: pip install sqlalchemy
#  Uses SQLite in-memory — no file or server needed.
# ─────────────────────────────────────────────────────────────

from __future__ import annotations

from sqlalchemy import (
    ForeignKey,
    String,
    Text,
    create_engine,
    desc,
    func,
    select,
    text,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
)


# ── ENGINE AND BASE ───────────────────────────────────────────

# In-memory SQLite — data is gone when the script ends
engine = create_engine("sqlite:///:memory:", echo=False)


class Base(DeclarativeBase):
    pass   # all models inherit from this


# ── MODELS ────────────────────────────────────────────────────

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(200), unique=True)

    # One user → many posts
    posts: Mapped[list["Post"]] = relationship(
        back_populates="author", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name!r})"


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    body: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # Many posts → one user
    author: Mapped["User"] = relationship(back_populates="posts")

    def __repr__(self) -> str:
        return f"Post(id={self.id}, title={self.title!r})"


# Create all tables
Base.metadata.create_all(engine)


# ── CREATE ────────────────────────────────────────────────────
print("── CREATE ───────────────────────────────────────────")

with Session(engine) as session:
    # Add multiple users at once
    users = [
        User(name="Alice",   email="alice@example.com"),
        User(name="Bob",     email="bob@example.com"),
        User(name="Carol",   email="carol@example.com"),
        User(name="Dave",    email="dave@example.com"),
    ]
    session.add_all(users)
    session.commit()

    # Refresh to get auto-assigned IDs
    for u in users:
        session.refresh(u)
    print(f"  created users: {[u.id for u in users]}")

    # Add posts linked to Alice and Bob
    posts = [
        Post(title="Python Tips",    body="Use type hints everywhere.", user_id=1),
        Post(title="FastAPI Guide",  body="FastAPI makes REST easy.",   user_id=1),
        Post(title="SQL Basics",     body="Learn SELECT before ORMs.",  user_id=2),
    ]
    session.add_all(posts)
    session.commit()
    print(f"  created posts: {[p.id for p in posts]}")


# ── READ ──────────────────────────────────────────────────────
print("\n── READ ─────────────────────────────────────────────")

with Session(engine) as session:
    # Get by primary key
    alice = session.get(User, 1)
    print(f"  get(User, 1): {alice}")

    # Select all users
    all_users = session.execute(select(User)).scalars().all()
    print(f"  all users: {all_users}")

    # Filter: users whose name starts with 'A' or 'B'
    stmt = select(User).where(User.name.like("A%") | User.name.like("B%"))
    ab_users = session.execute(stmt).scalars().all()
    print(f"  names starting with A or B: {ab_users}")

    # Order by name descending
    stmt = select(User).order_by(desc(User.name))
    ordered = session.execute(stmt).scalars().all()
    print(f"  ordered desc: {[u.name for u in ordered]}")

    # Count
    count = session.execute(select(func.count(User.id))).scalar()
    print(f"  total users: {count}")

    # Limit + offset (pagination)
    page = session.execute(select(User).limit(2).offset(1)).scalars().all()
    print(f"  page (limit=2, offset=1): {page}")


# ── RELATIONSHIPS ─────────────────────────────────────────────
print("\n── RELATIONSHIPS ────────────────────────────────────")

with Session(engine) as session:
    alice = session.get(User, 1)
    print(f"  Alice's posts:")
    for post in alice.posts:
        print(f"    - {post.title!r}")

    post = session.get(Post, 3)
    print(f"  Post 3 author: {post.author.name}")

    # JOIN: find users who have a post with "Python" in the title
    stmt = (
        select(User)
        .join(User.posts)
        .where(Post.title.like("%Python%"))
    )
    result = session.execute(stmt).scalars().all()
    print(f"  users with 'Python' posts: {result}")


# ── UPDATE ────────────────────────────────────────────────────
print("\n── UPDATE ───────────────────────────────────────────")

with Session(engine) as session:
    bob = session.get(User, 2)
    old_email = bob.email
    bob.email = "bob.new@example.com"
    session.commit()

    session.refresh(bob)
    print(f"  Bob's email: {old_email!r} → {bob.email!r}")


# ── DELETE ────────────────────────────────────────────────────
print("\n── DELETE ───────────────────────────────────────────")

with Session(engine) as session:
    dave = session.get(User, 4)
    session.delete(dave)
    session.commit()

    remaining = session.execute(select(User)).scalars().all()
    print(f"  after deleting Dave: {[u.name for u in remaining]}")


# ── RAW SQL ───────────────────────────────────────────────────
print("\n── RAW SQL ──────────────────────────────────────────")

with Session(engine) as session:
    # Parameterized query — never string-format user input into SQL
    result = session.execute(
        text("SELECT id, name, email FROM users WHERE id = :uid"),
        {"uid": 1},
    )
    row = result.fetchone()
    print(f"  raw SQL row: id={row.id}, name={row.name}")

    # Aggregate in raw SQL
    result = session.execute(
        text("SELECT COUNT(*) as total FROM posts WHERE user_id = :uid"),
        {"uid": 1},
    )
    total = result.scalar()
    print(f"  Alice's post count (raw SQL): {total}")
