from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = "sqlite:///./budget.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def init_db() -> None:
    """Create database tables."""
    SQLModel.metadata.create_all(engine)


@contextmanager
def session_scope() -> Iterator[Session]:
    """Provide a transactional scope around a series of operations."""
    with Session(engine) as session:
        yield session


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
