from __future__ import annotations

from datetime import date

from fastapi import FastAPI

from .database import init_db, session_scope
from .routers import auth as auth_router
from .routers import dashboard as dashboard_router
from .seed import seed_initial_data

app = FastAPI(title="Better Budget Tracker", version="0.1.0")


@app.on_event("startup")
def on_startup() -> None:
    init_db()
    with session_scope() as session:
        seed_initial_data(session)


@app.get("/")
def read_root() -> dict[str, str]:
    return {
        "message": "Welcome to the Better Budget Tracker API",
        "today": date.today().isoformat(),
    }


app.include_router(auth_router.router)
app.include_router(dashboard_router.router)
