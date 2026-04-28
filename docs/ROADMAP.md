# Roadmap

## Next Short-Term Work

1. Implement Reading Journey Foundation from `docs/READING_PROGRESS.md` and `docs/READING_SPEC.md`.
2. Add edit/delete controls to the Admin CMS frontend.
3. Add browser end-to-end tests for main learner journeys.
4. Add API unit tests with an isolated test database.
5. Improve auth with password or magic-link style login for real users.

## Reading Roadmap

Phase 1:
- Reading Journey Foundation.
- Reading level, score, sub-skill mastery, and next action.
- Initial sub-skills: `general_meaning`, `main_idea`, `detail_information`, `vocabulary_context`.
- Status: implemented as initial foundation.

Phase 2:
- Reading Sub-skill Trainer.
- Main idea, detail, vocabulary, reference, inference, and purpose practice.

Phase 3:
- Guided Reading Mode.
- Title understanding, sentence breakdown, main idea detection, and vocabulary context.

Phase 4:
- Answer Review.
- Correct/wrong explanation, evidence sentence, and distractor analysis.

Phase 5:
- Reading Review.
- Weakness report, mistake pattern, and recommended practice.

Phase 6:
- TOEFL Simulation.
- Timer, full set, and final report.

## AI Roadmap

1. Connect `backend/services/ai_service.py` to the selected LLM provider using environment variables.
2. Add prompt versioning in the `prompts` table.
3. Add structured AI feedback for writing, grammar, and next-step recommendation.
4. Add rate limiting and safer error handling before production use.

## Bantuan ID Roadmap

Phase 1:
- Contextual Bantuan ID inside Reading, Grammar, Vocabulary, AI Tutor, Writing, Listening, and Scenario BA.
- Mock-safe `/api/ai/contextual-help` endpoint.
- Inline explanation cards in Indonesian.

Phase 2:
- Explain user-selected text inside textarea and chat messages.
- Store helper usage more deeply in journey memory.
- Improve vocabulary pronunciation and memory tips.
- Add larger content-aware dictionaries for TOEFL question types, distractor patterns, and BA scenario patterns.

Phase 3:
- Let real AI mentor read journey history before explaining.
- Adapt explanation depth to user level and common mistakes.
- Use real LLM provider for open-ended explanations while preserving strict JSON output and mock fallback.

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
