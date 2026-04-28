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
- Contextual Bantuan ID added across learning modules. The old Indonesian helper page remains available, but the primary UX is now small inline help buttons beside actual English content.
- New `POST /api/ai/contextual-help` endpoint returns predictable JSON with mock fallback for Reading, Grammar, Vocabulary, AI Tutor, Writing, Listening, and Scenario contexts.
- Bantuan ID quality improved from generic fallback to context-specific explanations. Reading questions, reading options, vocabulary, grammar, listening, and scenario now use different response fields and can use `extra_context`.

## Verified

- Python compile check passed.
- Frontend JavaScript syntax check passed.
- JSON to SQLite migration completed.
- Smoke API test passed against FastAPI on port 8001.
- Smoke API test now covers contextual Bantuan ID samples for reading, grammar, vocabulary, listening, scenario, reading main idea question, correct option, wrong option, contradictory option, and scenario problem statement.

## Notes

The frontend remains intentionally simple and build-free. Admin CMS UI still focuses on create operations, while backend CRUD support is now ready for edit/delete UI in the next phase.

Journey calculation is intentionally simple for this phase: score averages, score-based levels, basic review status, and mock AI-style recommendations. Adaptive practice is rule-based for now; later phases can make mastery, spaced repetition, and adaptive difficulty smarter with real LLM support.

Contextual Bantuan ID still uses rule-based fallback unless an LLM key is configured, but the fallback is now less generic: it explains the exact clicked text, compares reading options against passage context when available, and avoids fake grammar parsing for questions/options.
