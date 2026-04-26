# API Spec

Base URL lokal:

```text
http://127.0.0.1:8001/api
```

## Core

- `GET /api`
- `GET /api/health`
- `GET /api/state`
- `POST /api/state`

## Auth

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/profile`

## Lessons

- `GET /api/lessons`
- `GET /api/lessons/{lesson_id}`
- `POST /api/lessons`
- `PUT /api/lessons/{lesson_id}`
- `DELETE /api/lessons/{lesson_id}`

## Vocabulary

- `GET /api/vocabulary`
- `GET /api/vocabulary/daily`
- `POST /api/vocabulary`
- `PUT /api/vocabulary/{vocab_id}`
- `DELETE /api/vocabulary/{vocab_id}`
- `POST /api/vocabulary/submit-answer`

## Progress

- `GET /api/progress/summary`
- `GET /api/progress/analytics`
- `POST /api/progress/analytics`
- `POST /api/progress/record`
- `POST /api/progress/attempt`

## Scoring

- `POST /api/scoring/reading`
- `POST /api/scoring/vocabulary`
- `POST /api/scoring/writing`
- `POST /api/scoring/listening`
- `POST /api/scoring/scenario`

Compatibility endpoint lama tetap tersedia:

- `POST /api/reading/submit-answer`
- `POST /api/writing/evaluate`
- `POST /api/listening/submit-answer`
- `POST /api/scenario/submit-answer`

## AI

- `POST /api/ai/chat`
- `POST /api/ai/explain-sentence`
- `POST /api/ai/grammar-breakdown`
- `POST /api/ai/writing-feedback`
- `POST /api/ai/recommend-next-step`

Compatibility endpoint lama:

- `POST /api/ai-tutor/chat`
- `POST /api/ai-tutor/recommendation`
- `POST /api/help/indonesian`
- `POST /api/grammar/breakdown`

## Admin

- `GET /api/admin/content`
- `POST /api/admin/content`
- `PUT /api/admin/content/{content_id}`
- `DELETE /api/admin/content/{content_id}`

## Integrated Journey

- `GET /api/journey/summary`
- `GET /api/journey/skills`
- `GET /api/journey/skills/{skill_type}`
- `POST /api/journey/attempt`
- `GET /api/journey/continue`
- `GET /api/journey/recommendations`
- `GET /api/journey/daily-plan`
- `GET /api/journey/review-list`
- `GET /api/journey/adaptive-practice`
- `GET /api/journey/mentor-summary`
- `POST /api/journey/adaptive-practice/complete`
- `POST /api/journey/reset?dev=true`

Valid `skill_type`: `reading`, `grammar`, `vocabulary`, `writing`, `listening`, `scenario`.

Example attempt:

```json
{
  "user_id": "default-user",
  "skill_type": "reading",
  "activity_id": "lesson-001",
  "activity_type": "reading_quiz",
  "score": 8,
  "max_score": 10,
  "mistakes": [],
  "feedback": "Good progress."
}
```
