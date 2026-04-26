---
name: toefl-business-analyst-ai-app
description: Project skill for building the TOEFL Business Analyst AI Learning App. Use this when designing, implementing, reviewing, or planning features in this repository.
---

# TOEFL Business Analyst AI Learning App Skill

## Purpose

Build a contextual TOEFL learning application for aspiring or junior Business Analysts. The product combines TOEFL practice, Business Analyst workplace context, BABOK-style concepts, AI tutoring, progress tracking, and scenario-based learning.

The core promise is:

> Help users improve English for TOEFL through Business Analyst scenarios, with an AI Tutor that explains mistakes simply and recommends the next practice.

## Target User

Primary persona: **Junior BA Learner**

- Basic English ability.
- Wants to become or improve as a Business Analyst.
- Struggles with long English sentences, grammar structure, professional vocabulary, and meeting/listening comprehension.
- Needs beginner-friendly explanation, repeated practice, and visible progress.

Design and implementation must favor clarity, guidance, and practical learning over academic complexity.

## Product Positioning

This is not a generic TOEFL app. Every major learning feature should be grounded in Business Analyst contexts such as:

- Requirement elicitation.
- Stakeholder needs.
- Business process.
- Business case.
- System requirements.
- User story and use case.
- Solution evaluation.
- Strategy analysis.
- Meeting discussion.

When adding content, examples, prompts, or UI labels, prefer professional BA scenarios instead of generic school or everyday topics.

## Core Product Pillars

1. **TOEFL Learning Core**
   - Reading.
   - Listening.
   - Structure and grammar.
   - Writing.
   - Vocabulary.
   - Speaking is optional and can come later.

2. **Business Analyst Context Layer**
   - All exercises should feel relevant to BA work.
   - Use workplace documents, stakeholder conversations, requirement statements, and analysis decisions as learning material.

3. **AI Tutor Internal**
   - Acts as English tutor, TOEFL mentor, BA learning assistant, grammar explainer, writing reviewer, listening coach, and daily study guide.
   - Must explain in simple Indonesian when useful.
   - Must identify user weakness and recommend small next steps.

4. **AI Listening Engine**
   - Generates BA meeting scripts, audio-friendly text, listening quizzes, transcript, explanations, vocabulary, and scores.
   - This is a differentiating feature, but should come after the MVP core is stable.

## MVP Scope

Build the first MVP in this order:

1. Authentication and user profile.
2. Dashboard progress.
3. Reading Analyzer.
4. Grammar Breakdown.
5. Vocabulary Drill.
6. AI Tutor Chat.

After the core MVP is stable, add:

1. Writing Feedback.
2. AI Listening Engine.
3. Scenario-Based BA Practice.
4. Admin CMS.
5. Payment or subscription, if needed.

Avoid expanding into all modules at once. Keep each feature small, testable, and connected to progress tracking.

## Learning Levels

Use three learning levels across content, AI prompts, and recommendations:

- **Foundation**
  - Basic sentence structure.
  - Subject, verb, object.
  - Basic TOEFL and BA vocabulary.
  - Short reading passages.

- **Intermediate**
  - Complex sentences.
  - Passive voice.
  - Reduced clauses.
  - Short meeting listening.
  - Simple requirement writing.

- **Advanced**
  - BABOK-style cases.
  - Long reading passages.
  - TOEFL inference questions.
  - Stakeholder simulation.
  - Business writing.

## Feature Guidance

### Dashboard

The dashboard is the user's learning control center.

It should show:

- TOEFL or learning level.
- Daily progress.
- Weakest skill.
- AI Tutor recommendation.
- Streak or consistency indicator.
- Scores for reading, grammar, listening, writing, and vocabulary when available.
- Weekly target.

### Reading Analyzer

Use BA documents and short passages, such as:

- Requirement documents.
- Stakeholder memos.
- Business cases.
- System proposals.
- Meeting summaries.
- Strategy analysis paragraphs.

Support TOEFL-style question types:

- Main idea.
- Inference.
- Reference.
- Vocabulary in context.
- Detail questions.

Output should include score, answer explanation, important vocabulary, and grammar insights.

### Grammar Breakdown

This is a core differentiator. It must be beginner-friendly.

Analyze:

- Subject and main verb.
- Object or complement.
- Main clause and subordinate clauses.
- Phrase.
- Reduced relative clause.
- Passive voice.
- Gerund.
- Nominalization.
- Modal verb.
- Parallel structure.
- Correlative conjunctions.
- Noun phrase.
- Adjective and adverbial clauses.

Output should include:

- Sentence structure.
- Grammar function.
- Pattern.
- Natural Indonesian translation.
- Simple explanation.
- Similar BA-context examples.
- Follow-up practice.

### Vocabulary Drill

Vocabulary should combine TOEFL academic words and BA workplace words.

Core categories:

- Requirement: elicit, validate, verify, specify.
- Stakeholder: sponsor, user, client, regulator.
- Analysis: assess, evaluate, define, prioritize.
- Strategy: objective, capability, initiative.
- Solution: design, implement, monitor, measure.
- TOEFL academic: significant, determine, establish, indicate.

Each vocabulary item should support:

- Word.
- Part of speech.
- Indonesian meaning.
- English meaning.
- BA-context example sentence.
- Level.
- Quiz or flashcard use.

### Writing Evaluator

Writing tasks can include:

- TOEFL essay.
- Requirement statement.
- Business case summary.
- Stakeholder meeting summary.
- User story.
- Problem statement.
- Solution recommendation.

Evaluate:

- Grammar.
- Clarity.
- Coherence.
- Vocabulary.
- Formality.
- BA relevance.
- TOEFL writing quality.

Return score, main mistakes, revised version, explanation, and next practice recommendation.

### AI Tutor Chat

The AI Tutor should be context-aware and connected to user progress.

It should:

- Explain mistakes.
- Answer grammar and vocabulary questions.
- Recommend daily practice.
- Generate short practice.
- Detect weakness.
- Use simple Indonesian for explanations when appropriate.

### AI Listening Engine

Listening scenarios should focus on:

- Requirement meetings.
- Stakeholder interviews.
- Sprint reviews.
- Product clarification.
- Conflict resolution meetings.
- Business process discussions.
- Solution evaluation meetings.

Each listening session should include:

- Scenario title and context.
- Script text.
- Generated audio URL when available.
- Transcript.
- Listening questions.
- Correct answers.
- Explanations.
- Vocabulary.
- Score.

### Scenario-Based BA Practice

Use decision-making questions that teach BA reasoning and English comprehension.

Example pattern:

```text
A stakeholder says, "The system should be more flexible."
What should the business analyst do first?
```

The expected reasoning should favor clarification, elicitation, validation, prioritization, and alignment with business goals.

## Recommended Architecture

Preferred stack from the planning document:

- Frontend: Vue.js or Nuxt.
- UI: Tailwind CSS with Preline UI.
- State management: Pinia.
- Backend: FastAPI or Node.js.
- API style: REST.
- Auth: JWT with role-based access control.
- Database: PostgreSQL.
- AI: OpenAI or OpenRouter.
- Listening: Text-to-Speech and Speech-to-Text.
- Storage: object storage for generated audio.
- Deployment: Docker and cloud hosting.

Use existing project conventions if the repository has already chosen a stack. Do not switch stacks without a strong reason.

## Initial Data Model

Start with these domain entities:

- `users`: identity, email, password hash, role.
- `learning_profiles`: TOEFL level, BA level, target score, weakness area, learning goal.
- `lessons`: title, module type, level, BA context, content.
- `questions`: lesson, text, options, correct answer, explanation.
- `user_answers`: selected answer, correctness, score.
- `vocabulary_items`: word, part of speech, meanings, example sentence, BA context, level.
- `writing_submissions`: prompt, submission, AI feedback, score.
- `listening_sessions`: scenario, script, audio URL, transcript, score.
- `ai_feedback_logs`: module type, input, AI feedback, score.
- `progress_records`: module type, lesson, score, completion status.

## Initial API Surface

Core endpoints may include:

```text
POST /auth/register
POST /auth/login
GET /auth/me
POST /auth/logout

GET /users/me
PATCH /users/me
GET /learning-profile
PATCH /learning-profile

GET /lessons
GET /lessons/:id
POST /lessons
PATCH /lessons/:id
DELETE /lessons/:id

GET /reading/lessons
GET /reading/lessons/:id
POST /reading/submit-answer
POST /reading/analyze

POST /grammar/breakdown
POST /grammar/generate-practice
POST /grammar/submit-answer

GET /vocabulary
GET /vocabulary/daily
POST /vocabulary/submit-answer

POST /ai-tutor/chat
POST /ai-tutor/recommendation
POST /ai-tutor/explain-answer

POST /listening/generate-scenario
POST /listening/generate-audio
GET /listening/sessions/:id
POST /listening/submit-answer

GET /progress/summary
GET /progress/module/:moduleType
POST /progress/record
```

## Prompt Patterns

### Grammar Breakdown

```text
Anda adalah AI English Tutor untuk calon Business Analyst.
Tugas Anda adalah membedah kalimat bahasa Inggris berikut.

Berikan analisis:
1. Subject
2. Main verb
3. Object atau complement
4. Clause
5. Phrase
6. Grammar pattern
7. Terjemahan natural bahasa Indonesia
8. Penjelasan sederhana untuk pemula
9. Contoh kalimat serupa dalam konteks Business Analyst

Kalimat:
[INPUT_KALIMAT]
```

### Reading Question Generator

```text
Anda adalah pembuat soal TOEFL berbasis konteks Business Analyst.

Buatkan:
1. Satu passage pendek bertema Business Analyst
2. Lima soal TOEFL reading
3. Pilihan A-D
4. Jawaban benar
5. Penjelasan jawaban
6. Vocabulary penting
7. Grammar yang muncul dalam passage

Level:
[BEGINNER / INTERMEDIATE / ADVANCED]

Topik BA:
[REQUIREMENT / STAKEHOLDER / ELICITATION / STRATEGY / SOLUTION EVALUATION]
```

### Writing Evaluator

```text
Anda adalah AI Writing Evaluator untuk calon Business Analyst.

Evaluasi tulisan berikut berdasarkan:
1. Grammar
2. Clarity
3. Coherence
4. Formality
5. Vocabulary
6. Business Analyst relevance
7. TOEFL writing quality

Berikan:
1. Skor 1-100
2. Kesalahan utama
3. Versi perbaikan
4. Penjelasan perbaikan
5. Rekomendasi latihan berikutnya

Tulisan user:
[INPUT_TULISAN]
```

### AI Tutor Recommendation

```text
Anda adalah AI Tutor internal untuk aplikasi TOEFL Business Analyst.

Berdasarkan data progress user berikut:
- Reading score: [SCORE]
- Grammar score: [SCORE]
- Listening score: [SCORE]
- Writing score: [SCORE]
- Vocabulary score: [SCORE]
- Weakness area: [WEAKNESS]

Berikan:
1. Ringkasan kondisi user
2. Prioritas latihan hari ini
3. Latihan yang direkomendasikan
4. Penjelasan sederhana mengapa latihan itu penting
5. Target kecil untuk hari ini
```

## Success Metrics

Learning metrics:

- Completed exercises.
- Reading score improvement.
- Grammar score improvement.
- Vocabulary growth.
- Writing clarity improvement.
- Listening comprehension improvement.
- Daily learning consistency.

Product metrics:

- Daily active users.
- Weekly active users.
- Completion rate.
- Retention rate.
- Average session duration.
- AI Tutor usage.
- Listening completion rate.

MVP is successful when:

- User can register, login, and use the dashboard.
- User can complete reading exercises.
- AI can explain grammar clearly.
- User can practice vocabulary.
- AI Tutor can answer user questions.
- Progress is saved.
- Users feel the app helps their learning.

## Risk Guardrails

- Keep scope small; do not build all planned modules at once.
- Validate AI-generated explanations before treating them as learning truth.
- Use prompt guardrails and structured outputs for AI features.
- Cache expensive AI outputs where practical.
- Keep UI simple and guided.
- Keep listening scripts short until audio quality and scoring are reliable.
- Use a consistent content model and review content regularly.
- Make modules independent enough to iterate separately.

## Development Workflow

Use this loop:

```text
Idea
-> Small technical spec
-> Scaffold or implement one module slice
-> Review
-> Test and debug
-> Document important changes
-> Commit when requested or appropriate
```

Development principles:

- Start from the smallest usable MVP.
- Break features into small tasks.
- Keep prompts specific.
- Review AI-generated code and content.
- Test before considering a feature done.
- Document important decisions.
- Prefer modular implementation.

## Recommended Sprint Order

1. **Sprint 0: Setup**
   - Repository, frontend, backend, database, environment variables, Docker basics.

2. **Sprint 1: Auth and Dashboard**
   - Register, login, user profile, initial dashboard.

3. **Sprint 2: Reading Module**
   - Lesson list, reading detail, questions, answer submission, score display.

4. **Sprint 3: Grammar Breakdown**
   - Sentence input, AI breakdown endpoint, result display, feedback log.

5. **Sprint 4: Vocabulary Drill**
   - Vocabulary database, flashcard UI, quiz UI, score recording.

6. **Sprint 5: AI Tutor Chat**
   - Chat UI, backend AI endpoint, context prompt, AI logs.

7. **Sprint 6: Writing Feedback**
   - Prompt, submission form, AI evaluation, feedback display.

8. **Sprint 7: AI Listening Engine**
   - Scenario generation, TTS audio, listening quiz, transcript, score.

9. **Sprint 8: Testing and Pilot**
   - End-to-end test, bug fixing, UX improvement, limited pilot, feedback collection.

## Definition of Done

A feature is done only when:

- UI can be used end to end.
- Backend API works.
- Data is persisted when needed.
- Major errors are handled.
- User flow can be completed from start to finish.
- AI output is displayed clearly.
- Manual testing has been completed.
- Important changes are documented.
- A commit has been made if the workflow requires it.

## Always Remember

- The product goal is **TOEFL skill plus Business Analyst skill**.
- Grammar explanations must be simple enough for beginners.
- Progress data should drive AI Tutor recommendations.
- Listening is a key differentiator, but should not distract from the core MVP.
- Keep the roadmap gradual, modular, and reviewable.
