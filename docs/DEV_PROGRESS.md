# Development Progress

## Phase Implemented

- Project restructured into `frontend/`, `backend/`, `docs/`, `scripts/`, and `data/`.
- FastAPI backend introduced with CORS and static frontend serving.
- SQLite database layer added at `data/toefl_ba.sqlite3`.
- JSON migration script added.
- Routers added for auth, lessons, vocabulary, progress, scoring, AI, and admin.
- AI service abstraction added with mock fallback and future OpenAI/OpenRouter-compatible provider.
- Listening service prepared for future TTS/STT architecture.
- Smoke test updated for FastAPI endpoints and compatibility endpoints.
- Beginner-friendly README and API documentation added.
- Basic Docker support added for local development.
- Integrated User Learning Journey added with database tables, service layer, router, scoring integration, frontend journey UI, and smoke checks.
- Adaptive mentor phase added: journey memory now produces short practice tasks, mentor summary, and completion tracking.

## Verified

- Python compile check passed.
- Frontend JavaScript syntax check passed.
- JSON to SQLite migration completed.
- Smoke API test passed against FastAPI on port 8001.

## Notes

The frontend remains intentionally simple and build-free. Admin CMS UI still focuses on create operations, while backend CRUD support is now ready for edit/delete UI in the next phase.

Journey calculation is intentionally simple for this phase: score averages, score-based levels, basic review status, and mock AI-style recommendations. Adaptive practice is rule-based for now; later phases can make mastery, spaced repetition, and adaptive difficulty smarter with real LLM support.
