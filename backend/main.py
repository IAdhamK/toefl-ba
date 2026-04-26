from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.repository import get_state, set_state
from backend.routers import admin, ai_tutor, auth, lessons, progress, scoring, vocabulary
from backend.seed import seed_database
from backend.services.listening_service import generate_listening_scenario
from backend.services.scoring_service import SCENARIO_QUESTIONS


ROOT_DIR = Path(__file__).resolve().parents[1]
FRONTEND_DIR = ROOT_DIR / "frontend"

app = FastAPI(
    title="TOEFL Analyst AI API",
    description="FastAPI backend untuk TOEFL + Business Analyst learning app.",
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    seed_database()


@app.get("/api")
def api_root() -> dict:
    return {
        "ok": True,
        "name": "TOEFL Analyst AI API",
        "version": "0.2.0",
        "message": "FastAPI aktif. Frontend tetap tersedia di root URL.",
    }


@app.get("/api/health")
def health() -> dict:
    return {"ok": True, "service": "TOEFL Analyst AI API", "backend": "FastAPI", "database": "SQLite"}


@app.get("/api/state")
def read_state() -> dict:
    return {"state": get_state()}


@app.post("/api/state")
def write_state(state: dict) -> dict:
    return {"state": set_state(state)}


@app.get("/api/listening/sessions/default")
def listening_default() -> dict:
    return {"session": generate_listening_scenario()}


@app.post("/api/listening/generate-scenario")
def listening_generate() -> dict:
    return {"session": generate_listening_scenario()}


@app.get("/api/scenario/questions")
def scenario_questions() -> dict:
    return {"questions": SCENARIO_QUESTIONS}


app.include_router(auth.router)
app.include_router(lessons.router)
app.include_router(vocabulary.router)
app.include_router(progress.router)
app.include_router(scoring.router)
app.include_router(ai_tutor.router)
app.include_router(admin.router)


@app.get("/")
def index() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")


if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
