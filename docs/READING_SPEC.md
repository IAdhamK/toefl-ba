# Reading Feature Specification

Dokumen ini menjelaskan target sistem Reading untuk TOEFL Analyst AI. Ini adalah spesifikasi arah, bukan implementasi final. Fase berikutnya harus mengambil bagian kecil dari dokumen ini dan mengimplementasikannya secara bertahap.

## Product Goal

Reading Feature membantu pemula memahami teks TOEFL dengan konteks Business Analyst. User tidak hanya mengejar skor, tetapi belajar cara membaca: memahami arti umum, menemukan ide utama, mencari detail, memahami vocabulary context, menganalisis inference, dan membaca case BA.

## Target Structure

```text
Reading Feature
├── Reading Journey
│   ├── Level
│   ├── Score
│   ├── Sub-skill mastery
│   └── Next action
├── Guided Reading
│   ├── Title understanding
│   ├── Sentence breakdown
│   ├── Main idea detection
│   └── Vocabulary context
├── Question Trainer
│   ├── Main idea
│   ├── Detail
│   ├── Vocabulary
│   ├── Reference
│   ├── Inference
│   └── Purpose
├── Answer Review
│   ├── Correct/wrong explanation
│   ├── Evidence sentence
│   └── Distractor analysis
├── Reading Review
│   ├── Weakness report
│   ├── Mistake pattern
│   └── Recommended practice
└── TOEFL Simulation
    ├── Timer
    ├── Full set
    └── Final report
```

## Reading Sub-skills

Use these sub-skill identifiers consistently:

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

## Reading Levels

1. Understand Simple Meaning
2. Find Main Idea
3. Find Supporting Details
4. Vocabulary in Context
5. Reference and Pronoun
6. Complex Sentence Breakdown
7. Inference
8. Author Purpose and Logic
9. BA Case Reading
10. TOEFL Reading Simulation

## Component Specs

### Reading Journey

Purpose:
Shows where the learner is in Reading and what to do next.

Fields:

- `current_level`
- `reading_score`
- `completed_reading_exercises`
- `sub_skill_mastery`
- `weakest_sub_skill`
- `strongest_sub_skill`
- `next_action`
- `last_reading_activity`

Beginner-friendly next action examples:

- "Hari ini fokus memahami arti umum passage pendek."
- "Latihan main idea: pilih jawaban yang merangkum seluruh passage."
- "Ulangi vocabulary in context, jangan hanya arti kamus."
- "Latihan inference: cari informasi yang tersirat, bukan tertulis langsung."

### Guided Reading

Purpose:
Guides users through a passage before answering questions.

Steps:

1. Title understanding
   - Ask: "Judul ini kira-kira tentang apa?"
   - Output: prediction in Indonesian.
2. Sentence breakdown
   - Identify subject, verb, modifier, object/complement only when useful.
   - Avoid forcing grammar breakdown on every sentence.
3. Main idea detection
   - Show possible main idea.
   - Explain why it covers the passage.
4. Vocabulary context
   - Explain key words using:
     - one-word meaning
     - general meaning
     - contextual meaning
     - BA/TOEFL meaning

### Question Trainer

Purpose:
Lets users practice by question type.

Question types:

- `main_idea`
- `detail`
- `vocabulary`
- `reference`
- `inference`
- `purpose`

Each question should store:

- `id`
- `lesson_id`
- `question_type`
- `question_text`
- `options`
- `answer`
- `evidence_sentence`
- `explanation`
- `distractor_notes`
- `sub_skill`

### Answer Review

Purpose:
Explains the answer after user submits.

For correct answer:

- Confirm why it is correct.
- Show evidence sentence.
- Explain key vocabulary if needed.

For wrong answer:

- Explain what the selected option means.
- Explain why it is weak/wrong.
- Show the correct answer.
- Show evidence sentence.
- Give one small next practice.

Distractor analysis should explain:

- `too_broad`
- `too_narrow`
- `not_supported`
- `opposite_meaning`
- `true_but_not_answer`
- `irrelevant_detail`

### Reading Review

Purpose:
Summarizes learner weakness after multiple attempts.

Report should include:

- weakest sub-skill
- common mistake pattern
- review vocabulary
- question types often missed
- recommended practice

Example:

```text
Kelemahan utama: main_idea.
Pola salah: sering memilih detail kecil sebagai ide utama.
Latihan berikutnya: kerjakan 3 soal main idea dan baca kalimat pertama/terakhir passage.
```

### TOEFL Simulation

Purpose:
Provides mini or full Reading simulation.

Features:

- Timer.
- Passage set.
- Question navigation.
- Submit full set.
- Final report.
- Sub-skill breakdown.

Future report fields:

- `raw_score`
- `estimated_toefl_score`
- `time_spent`
- `accuracy_by_question_type`
- `weakest_sub_skill`
- `recommended_next_session`

## Data Model Direction

Recommended future tables or fields:

- `reading_lessons`
- `reading_questions`
- `reading_attempts`
- `reading_sub_skill_mastery`
- `reading_reviews`
- `reading_simulations`

Important:
Use SQLite first. Do not require PostgreSQL yet.

## API Direction

Possible future endpoints:

- `GET /api/reading/journey`
- `GET /api/reading/lessons`
- `GET /api/reading/lessons/{lesson_id}`
- `POST /api/reading/attempt`
- `GET /api/reading/review`
- `GET /api/reading/trainer?question_type=main_idea`
- `POST /api/reading/trainer/submit`
- `POST /api/reading/simulation/start`
- `POST /api/reading/simulation/submit`

Keep compatibility endpoint:

- `POST /api/reading/submit-answer`

## Bantuan ID Integration

Reading Bantuan ID should use `extra_context`:

- `passage_title`
- `passage_text`
- `question_text`
- `option_text`
- `correct_answer`
- `explanation`
- `tags`

For reading question, show:

- Arti langsung pertanyaan.
- Maksud pertanyaan.
- Yang harus dicari.
- Cara menjawab.
- Jebakan yang harus dihindari.

For reading option, show:

- Arti langsung opsi.
- Hubungan dengan passage.
- Kemungkinan benar/salah if `correct_answer` exists.
- Alasan.
- Kata penting.

## Implementation Rules

- Preserve existing Reading Analyzer.
- Add small pieces incrementally.
- Keep Indonesian beginner-friendly text.
- Avoid fake grammar parsing.
- Do not remove existing endpoints.
- Keep old local fallback behavior.
- Add smoke tests with each phase.
- Update `docs/READING_PROGRESS.md` after each phase.
