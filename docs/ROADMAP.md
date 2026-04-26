# Roadmap

## Next Short-Term Work

1. Add edit/delete controls to the Admin CMS frontend.
2. Add browser end-to-end tests for main learner journeys.
3. Add API unit tests with an isolated test database.
4. Improve auth with password or magic-link style login for real users.
5. Add richer lesson/question schema and validation.

## AI Roadmap

1. Connect `backend/services/ai_service.py` to the selected LLM provider using environment variables.
2. Add prompt versioning in the `prompts` table.
3. Add structured AI feedback for writing, grammar, and next-step recommendation.
4. Add rate limiting and safer error handling before production use.

## Listening Roadmap

1. Add TTS provider integration to generate audio from transcript.
2. Store audio metadata and transcript timestamps.
3. Add STT-ready endpoint for spoken answers.
4. Add listening question generation from transcript.

## Integrated Journey Roadmap

Phase 1:
- Basic integrated journey.
- Skill progress.
- Continue learning.
- Daily plan.

Phase 2:
- Better mastery calculation.
- Spaced repetition vocabulary.
- More detailed mistake analysis.

Phase 3:
- AI mentor reads journey memory with real LLM support.
- Personalized learning path with adaptive question difficulty.

Phase 4:
- Production auth and per-user security.

## Deployment Roadmap

1. Improve Docker setup with production and development profiles.
2. Add PostgreSQL migration path.
3. Add production config and environment examples.
4. Add CI checks for API smoke test and frontend syntax.
