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

## Reading

- `GET /api/reading/journey`
- `GET /api/reading/levels`
- `GET /api/reading/recommendation`
- `GET /api/reading/subskills`
- `GET /api/reading/trainer/{sub_skill}`
- `POST /api/reading/guided-steps`
- `POST /api/reading/passage-map`
- `POST /api/reading/review-answer`
- `POST /api/reading/attempt`

Example Reading attempt:

```json
{
  "user_id": "default-user",
  "passage_id": "reading-1",
  "sub_skill": "main_idea",
  "score": 82,
  "max_score": 100,
  "subskill_scores": {
    "general_meaning": 90,
    "main_idea": 80,
    "detail_information": 75,
    "vocabulary_context": 70
  },
  "feedback": "Reading attempt tersimpan."
}
```

Example Reading trainer attempt:

```json
{
  "user_id": "default-user",
  "passage_id": "trainer-main-idea-1",
  "activity_type": "reading_subskill_trainer",
  "sub_skill": "main_idea",
  "selected": 1
}
```

`GET /api/reading/subskills` returns 10 Reading sub-skills:

- `general_meaning`
- `main_idea`
- `detail_information`
- `vocabulary_context`
- `reference`
- `sentence_simplification`
- `inference`
- `author_purpose`
- `paragraph_function`
- `ba_case_analysis`

`GET /api/reading/trainer/{sub_skill}` currently supports:

- `main_idea`
- `detail_information`
- `vocabulary_context`
- `inference`
- `sentence_simplification`

Trainer response includes:

- `sub_skill`
- `label`
- `mastery`
- `next_action`
- `passage`
- `question`
- `guidance`

Trainer attempt response includes `answer_feedback`, `reading_journey`, and `next_recommended_subskill`.
When the request includes a selected answer, Reading attempt also includes:

- `answer_review`
- `evidence_sentence`
- `distractor_analysis`
- `next_recommendation`

Example Guided Reading request:

```json
{
  "lesson_id": "reading-1",
  "title": "Stakeholder Needs and Strategy Alignment",
  "passage": "A business analyst ... proposing a solution.",
  "vocabulary": ["elicit", "alignment", "stakeholder"],
  "question_text": "What is the main idea of the passage?"
}
```

`POST /api/reading/guided-steps` returns:

- `steps`
- `total_steps`
- `support_activity`

Guided steps currently cover:

1. title understanding
2. first sentence
3. subject and main verb
4. important vocabulary
5. paragraph map
6. main idea
7. answer the question

`POST /api/reading/passage-map` returns:

- paragraph number
- simple meaning
- key vocabulary
- main point
- possible reading skill
- beginner tip

Guided Reading is rule-based for now and beginner-friendly in Indonesian. The frontend records completion as a support activity without lowering the Reading score.

Example Answer Review request:

```json
{
  "passage": "A business analyst ... organizational strategy.",
  "question": {
    "id": "r1q1",
    "text": "What is the main idea of the passage?",
    "options": [
      "Business analysts should write code immediately.",
      "Business analysts must connect requirements with stakeholder needs and strategy.",
      "Stakeholders should avoid discussing vague problems.",
      "Organizational strategy is unrelated to requirements."
    ],
    "answer": 1,
    "explanation": "The passage emphasizes eliciting requirements and aligning them with needs and strategy."
  },
  "selected": 0
}
```

`POST /api/reading/review-answer` returns:

- selected answer
- correct answer
- direct explanation
- evidence sentence from passage
- why correct answer is correct
- why selected answer is wrong if wrong
- distractor analysis for every option
- related reading sub-skill
- next practice recommendation

Reading Journey response includes:

- `reading_level`
- `reading_score`
- `completed_passages`
- `current_stage`
- `weak_subskills`
- `strong_subskills`
- `sub_skill_mastery`
- `last_passage_id`
- `next_recommended_action`

## AI

- `POST /api/ai/chat`
- `POST /api/ai/explain-sentence`
- `POST /api/ai/grammar-breakdown`
- `POST /api/ai/writing-feedback`
- `POST /api/ai/recommend-next-step`
- `POST /api/ai/contextual-help`

Compatibility endpoint lama:

- `POST /api/ai-tutor/chat`
- `POST /api/ai-tutor/recommendation`
- `POST /api/help/indonesian`
- `POST /api/grammar/breakdown`

Example contextual Bantuan ID request:

```json
{
  "text": "A business analyst elicits requirements from stakeholders.",
  "module": "reading",
  "context_type": "reading_paragraph",
  "user_level": "beginner",
  "extra_context": {
    "activity_id": "lesson-001"
  }
}
```

`extra_context` is optional but recommended. The frontend now sends richer context when available:

```json
{
  "passage_text": "A business analyst ... organizational strategy.",
  "question_text": "What is the main idea of the passage?",
  "option_text": "Business analysts should write code immediately.",
  "correct_answer": "Business analysts must connect requirements with stakeholder needs and strategy."
}
```

Expected response shape:

```json
{
  "text": "A business analyst elicits requirements from stakeholders.",
  "module": "reading",
  "context_type": "reading_paragraph",
  "explanation_id": "help-123",
  "explanation": {
    "direct_meaning_id": "Seorang Business Analyst menggali kebutuhan dari stakeholder.",
    "simple_meaning_id": "Seorang Business Analyst menggali kebutuhan dari stakeholder.",
    "subject": "A business analyst",
    "verb": "elicit / elicits",
    "object_or_complement": "requirements / stakeholder needs",
    "grammar_pattern": "Subject + Verb + Object/Complement",
    "important_vocabulary": []
  },
  "source": "mock"
}
```

Context-specific fields may appear depending on `context_type`:

- Reading question: `question_intent`, `what_to_find`, `how_to_answer`, `trap_to_avoid`, `key_words`
- Reading option: `option_meaning`, `relation_to_context`, `likely_correctness_hint`, `why`
- Vocabulary: `word_one_word_meaning_id`, `word_meaning_id`, `word_contextual_meaning_id`, `memory_tip`
- Grammar: `main_verb`, `modifier`, `grammar_pattern`, `beginner_warning`, `simplified_sentence`
- Listening: `listening_focus`, `keywords_to_hear`, `speaker_intent`, `answer_strategy`
- Scenario: `ba_context`, `business_problem`, `stakeholder_need`, `suggested_ba_action`

For vocabulary help, each `important_vocabulary` item may include:

```json
{
  "word": "maintain",
  "meaning_id": "menjaga atau merawat agar tetap berjalan",
  "one_word_meaning_id": "menjaga",
  "contextual_meaning_id": "Dalam contoh kalimat tertentu, maintain bisa berarti menjaga proses, sistem, atau kualitas agar tetap berjalan baik."
}
```

Valid contextual `module`: `reading`, `grammar`, `vocabulary`, `tutor`, `writing`, `listening`, `scenario`.

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
