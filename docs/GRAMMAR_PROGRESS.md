# Grammar Development Progress

Dokumen ini melacak pengembangan Grammar module untuk TOEFL Analyst AI. Tujuannya agar setiap fase bisa dikerjakan kecil, aman, dan tidak merusak fitur Grammar yang sudah ada.

## Current Status

Grammar feature saat ini masih basic. Fungsi utamanya adalah membantu user memasukkan satu kalimat, lalu aplikasi memberikan breakdown sederhana seperti subject, verb, object/complement, dan penjelasan Bahasa Indonesia.

Phase 2 sudah menambahkan Grammar Topic Library statis dengan level Basic, Intermediate, dan Advanced. Fitur ini belum menjadi Grammar Learning Journey penuh, tetapi sudah menyediakan struktur topic yang akan dipakai oleh fase trainer, journey, review, dan simulasi.

## Existing Capability

- Basic grammar breakdown untuk kalimat Inggris.
- Indonesian explanation support agar pemula lebih mudah memahami.
- Contextual Bantuan ID integration di beberapa bagian aplikasi.
- Journey update sudah ada dalam bentuk sederhana melalui sistem learning journey umum.
- Grammar Topic Library statis dengan 21 topic: 7 Basic, 7 Intermediate, dan 7 Advanced.
- Endpoint backend untuk level, topic list, topic detail, summary, dan next topic.
- Grammar Sentence Builder untuk arrange words, complete sentence, combine sentences, rewrite formal BA sentence, dan fix word order.

## Known Limitations

- Belum ada grammar level structure.
- Belum ada diagnostic test.
- Belum ada grammar trainer.
- Belum ada grammar mistake pattern analysis.
- Belum ada error correction module.
- Sentence Builder masih static dan scoring free-text masih sederhana.
- Belum ada grammar simulation.
- Current scoring masih terlalu sederhana dan belum cukup adaptif.
- Breakdown saat ini belum selalu membedakan main verb, modifier, phrase, dan clause secara mendalam.
- Topic library masih static in-memory data, belum database-backed.
- Belum ada frontend topic library UI.

## Target Architecture

Komponen yang direncanakan:

- Grammar topic service
- Grammar journey service
- Grammar trainer
- Grammar review service
- Grammar simulation service
- Grammar frontend panels

Arsitektur target tetap sederhana:

- Gunakan FastAPI backend yang sudah ada.
- Gunakan frontend build-free yang sudah ada.
- Simpan logic bertahap di service layer.
- Pertahankan endpoint lama seperti `/api/grammar/breakdown`.
- Gunakan mock/rule-based logic dulu jika AI belum tersedia.

## Development Phases

### Phase 1 - Grammar Documentation

Status: Completed

Deliverables:

- `docs/GRAMMAR_SPEC.md`
- `docs/GRAMMAR_PROGRESS.md`

### Phase 2 - Grammar Topic Library

Status: Completed

Deliverables:

- Static grammar topic data
- `GET /api/grammar/levels`
- `GET /api/grammar/topics`
- `GET /api/grammar/topics/{topic_id}`
- `GET /api/grammar/topic-summary`
- `GET /api/grammar/next-topic`

### Phase 3 - Grammar Journey Foundation

Status: Completed

Deliverables:

- Grammar level
- Grammar score
- Completed topics
- Weakest topic
- Next recommended topic
- Topic mastery summary
- `GET /api/grammar/journey`
- `POST /api/grammar/attempt`
- `GET /api/grammar/mastery`
- `GET /api/grammar/recommendation`

### Phase 4 - Basic Grammar Trainer

Status: Completed

Deliverables:

- Trainer for subject and verb
- Trainer for object and complement
- Trainer for modal verb
- Trainer for simple sentence pattern
- Trainer for all Basic topics:
  - parts of speech
  - subject and verb
  - object and complement
  - modal verb
  - simple sentence pattern
  - simple tense
  - prepositional phrase
- `GET /api/grammar/trainer/basic`
- `GET /api/grammar/trainer/basic/{topic_id}`
- `POST /api/grammar/trainer/basic/submit`

### Phase 5 - Deep Grammar Breakdown

Status: Completed

Deliverables:

- Richer sentence analysis
- Grammar patterns
- Common traps
- BA context meaning
- Next practice recommendation
- Backward-compatible `POST /api/grammar/breakdown`
- Optional deep endpoint `POST /api/grammar/breakdown/deep`

### Phase 6 - Intermediate Grammar Trainer

Status: Completed

Deliverables:

- Gerund vs main verb
- Infinitive phrase
- Relative clause
- Reduced relative clause
- Passive voice
- Parallel structure
- Connector logic
- Trap items for common misunderstanding
- `GET /api/grammar/trainer/intermediate`
- `GET /api/grammar/trainer/intermediate/{topic_id}`
- `POST /api/grammar/trainer/intermediate/submit`

### Phase 7 - Grammar Error Correction

Status: Completed

Deliverables:

- Error correction exercises
- Explanation of why the original sentence is wrong
- Corrected sentence suggestion
- Topic-based correction feedback
- `GET /api/grammar/error-correction/categories`
- `GET /api/grammar/error-correction`
- `GET /api/grammar/error-correction/{error_type}`
- `POST /api/grammar/error-correction/submit`

### Phase 8 - Sentence Builder

Status: Completed

Deliverables:

- Guided BA sentence construction
- Subject + verb + object practice
- Connector and modifier practice
- Feedback for clarity and grammar
- `GET /api/grammar/sentence-builder/levels`
- `GET /api/grammar/sentence-builder`
- `GET /api/grammar/sentence-builder/{item_id}`
- `POST /api/grammar/sentence-builder/submit`

### Phase 9 - Advanced Grammar Lab

Status: Completed

Deliverables:

- Complex sentence mapping
- Nominalization practice
- Hedging language practice
- Formal BA writing grammar
- Inversion practice
- Conditional sentence practice
- Academic connectors practice
- `GET /api/grammar/advanced/topics`
- `GET /api/grammar/advanced/topics/{topic_id}`
- `GET /api/grammar/advanced/practice`
- `GET /api/grammar/advanced/rewrite`
- `POST /api/grammar/advanced/practice/submit`
- `POST /api/grammar/advanced/rewrite/submit`

### Phase 10 - Grammar Review and Mistake Pattern

Status: Completed

Deliverables:

- Weak topic report
- Repeated mistake analysis
- Recommended review queue
- Mentor message in Indonesian
- `GET /api/grammar/review`
- `GET /api/grammar/mistake-patterns`
- `GET /api/grammar/review-queue`
- `GET /api/grammar/weakness-summary`
- `GET /api/grammar/recommended-practice`

### Phase 11 - Grammar Simulation

Status: Completed

Deliverables:

- TOEFL-style grammar simulation
- Timed grammar practice
- Final score
- Topic breakdown
- Next recommendation
- `GET /api/grammar/simulation/modes`
- `POST /api/grammar/simulation/start`
- `POST /api/grammar/simulation/submit`
- `GET /api/grammar/simulation/result/{session_id}`
- `GET /api/grammar/simulation/history`

## Testing Checklist

Future testing checklist:

- Python compile check.
- Frontend JavaScript syntax check.
- Smoke test for grammar endpoints.
- Manual UI check.
- Backward compatibility check for existing `/api/grammar/breakdown`.
- Check that no existing Grammar, Bantuan ID, Journey, or AI Tutor behavior is broken.

## Phase 2 - Grammar Topic Library

Phase 2 selesai sebagai backend-first implementation. Grammar module sekarang punya sumber data statis yang rapi untuk Basic, Intermediate, dan Advanced grammar topics.

### Implemented Files

- `backend/services/grammar_topic_service.py`
- `backend/routers/grammar.py`
- `backend/main.py`
- `scripts/smoke_api.py`
- `docs/GRAMMAR_PROGRESS.md`

### New Endpoints

- `GET /api/grammar/levels`
- `GET /api/grammar/topics`
- `GET /api/grammar/topics?level=basic`
- `GET /api/grammar/topics/{topic_id}`
- `GET /api/grammar/topic-summary`
- `GET /api/grammar/next-topic`

### Testing Checklist

- Python compile check for `backend/main.py`, `backend/routers/grammar.py`, and `backend/services/grammar_topic_service.py`.
- Smoke test for all new grammar topic endpoints.
- Backward compatibility check for existing `POST /api/grammar/breakdown`.
- No database migration required.

### Known Limitations

- Topics are still static data.
- No user progress per topic yet.
- No trainer questions yet.
- No Grammar Journey yet.
- No frontend topic library UI yet.
- No database tables yet.

### Next Recommended Phase

Phase 3 - Grammar Journey Foundation.

The next phase should connect the topic library with user progress, but still keep the current `/api/grammar/breakdown` behavior backward compatible.

## Phase 3 - Grammar Journey Foundation

Phase 3 selesai sebagai backend-first implementation. Grammar module sekarang bisa menampilkan progress dasar user untuk Grammar berdasarkan topic library dan attempt yang disimpan melalui infrastruktur journey yang sudah ada.

### Implemented Files

- `backend/services/grammar_journey_service.py`
- `backend/routers/grammar.py`
- `scripts/smoke_api.py`
- `docs/GRAMMAR_PROGRESS.md`

### New Endpoints

- `GET /api/grammar/journey`
- `POST /api/grammar/attempt`
- `GET /api/grammar/mastery`
- `GET /api/grammar/recommendation`

Existing endpoints that must remain working:

- `POST /api/grammar/breakdown`
- `GET /api/grammar/levels`
- `GET /api/grammar/topics`
- `GET /api/grammar/topics/{topic_id}`
- `GET /api/grammar/topic-summary`
- `GET /api/grammar/next-topic`

### Grammar Level Calculation

For now, Grammar level is calculated from `grammar_score` and `completed_topics`.

- If `completed_topics` is `0`: `Basic 1 - Sentence Foundation`
- If `grammar_score < 25`: `Basic 1 - Sentence Foundation`
- If `grammar_score >= 25` and `< 50`: `Basic 2 - Subject and Verb Control`
- If `grammar_score >= 50` and `< 70`: `Intermediate 1 - Phrase and Clause Awareness`
- If `grammar_score >= 70` and `< 85`: `Intermediate 2 - Complex Grammar Control`
- If `grammar_score >= 85`: `Advanced 1 - Professional Grammar Usage`

### Topic Mastery Status Calculation

Each topic returns a mastery status:

- `mastered`: mastery score `>= 85`
- `in_progress`: mastery score `>= 70`
- `need_review`: mastery score `>= 1`
- `not_started`: mastery score `== 0`

Each topic mastery item includes:

- `topic_id`
- `title`
- `level`
- `mastery_score`
- `completed_count`
- `status`
- `last_score`
- `next_action`

### Testing Checklist

- Python compile check for `backend/main.py`, `backend/routers/grammar.py`, `backend/services/grammar_topic_service.py`, and `backend/services/grammar_journey_service.py`.
- Smoke test for Grammar Topic Library endpoints.
- Smoke test for Grammar Journey endpoints.
- Smoke test for `POST /api/grammar/attempt`.
- Backward compatibility check for existing `POST /api/grammar/breakdown`.

### Known Limitations

- Mastery calculation is still simple and rule-based.
- Topic progress uses existing `learning_attempts` and `skill_mastery` infrastructure, not dedicated grammar tables.
- No dedicated grammar database tables yet.
- Grammar Trainer UI is still minimal and intended for Phase 4 validation, not final polish.
- No error correction yet.
- No sentence builder yet.
- Grammar breakdown is not deeply integrated with the new Grammar Journey beyond the existing simple journey update.

### Next Recommended Phase

Phase 4 - Basic Grammar Trainer.

The next phase should add focused trainer exercises for:

- Subject and Verb
- Object and Complement
- Modal Verb
- Simple Sentence Pattern

## Phase 4 - Basic Grammar Trainer

Phase 4 selesai. Grammar module sekarang punya Basic Grammar Trainer statis untuk membantu pemula belajar grammar dengan alur:

```text
Learn -> Guided Practice -> Quiz -> Feedback
```

### Implemented Files

- `backend/services/grammar_trainer_service.py`
- `backend/routers/grammar.py`
- `frontend/app.js`
- `frontend/index.html`
- `frontend/styles.css`
- `scripts/smoke_api.py`
- `docs/GRAMMAR_PROGRESS.md`

### New Endpoints

- `GET /api/grammar/trainer/basic`
- `GET /api/grammar/trainer/basic/{topic_id}`
- `POST /api/grammar/trainer/basic/submit`

### Basic Topics Covered

- `parts_of_speech`
- `subject_verb`
- `object_complement`
- `modal_verb`
- `simple_sentence_pattern`
- `simple_tense`
- `prepositional_phrase`

### Question Types Implemented

- `identify_subject`
- `identify_main_verb`
- `identify_object`
- `choose_correct_pattern`
- `choose_correct_sentence`
- `simple_meaning_from_structure`

### How Scoring Works

Scoring is rule-based:

- Each quiz item has one `correct_answer`.
- User answer is compared to the correct answer after simple normalization.
- Score is calculated as `correct_count / total_questions * 100`.
- Passing threshold is `70`.

### Grammar Journey Integration

When user submits Basic Trainer answers:

- Backend calculates score.
- Backend calls Grammar Journey attempt logic.
- Attempt uses `activity_type = basic_grammar_trainer`.
- Attempt uses `activity_id = topic_id`.
- Mistakes are included for wrong answers.
- Response returns updated `grammar_journey`.

### Frontend Changes

Minimal frontend panel added to the existing Grammar page:

- Basic trainer topic buttons.
- Explanation, beginner tip, and BA context.
- Example sentence breakdown.
- Guided practice cards.
- Quiz select controls.
- Score and recommendation result after submit.

Existing Grammar Breakdown UI remains available.

### Testing Checklist

- Python compile check for grammar router and services.
- Frontend JavaScript syntax check.
- Smoke test for Basic Grammar Trainer topic list.
- Smoke test for Basic Grammar Trainer detail.
- Smoke test for Basic Grammar Trainer submit.
- Backward compatibility check for `POST /api/grammar/breakdown`.
- Backward compatibility check for Grammar Topic Library and Grammar Journey endpoints.

### Known Limitations

- Trainer data is still static.
- Scoring is still rule-based.
- No database-backed question bank yet.
- Intermediate Trainer is not implemented yet.
- Error Correction is not implemented yet.
- Sentence Builder is not implemented yet.
- Grammar Simulation is not implemented yet.
- Frontend UI is intentionally minimal and can be polished later.

### Next Recommended Phase

Phase 5 - Deep Grammar Breakdown.

The next phase should improve sentence analysis depth while keeping the Basic Trainer, Topic Library, and Grammar Journey stable.

## Phase 5 - Deep Grammar Breakdown

Phase 5 selesai. Existing Grammar Breakdown sekarang mengembalikan field lama dan field deep baru, sehingga frontend lama tetap kompatibel tetapi user mendapat analisis grammar yang lebih kaya.

### Implemented Files

- `backend/services/grammar_service.py`
- `backend/routers/ai_tutor.py`
- `backend/routers/grammar.py`
- `frontend/app.js`
- `frontend/index.html`
- `frontend/styles.css`
- `scripts/smoke_api.py`
- `docs/GRAMMAR_PROGRESS.md`

### Upgraded Response Fields

Old fields tetap tersedia:

- `subject`
- `mainVerb`
- `phrase`
- `pattern`
- `translation`
- `explanation`

New deep fields:

- `sentence_level`
- `sentence_type`
- `main_subject`
- `main_verb`
- `object_or_complement`
- `modifier_phrases`
- `clauses`
- `grammar_patterns`
- `common_trap`
- `simple_meaning_id`
- `ba_context_meaning`
- `structure_steps`
- `detected_keywords`
- `grammar_focus`
- `next_practice`
- `recommended_topic_id`
- `confidence_note`

### Supported Grammar Detections

Rule-based detection now covers:

- Modal verb
- Gerund / `-ing` confusion
- Relative clause
- Passive voice
- Parallel structure
- Nominalization
- Connector logic
- Academic connectors

### Endpoint Changes

- `POST /api/grammar/breakdown` remains available and backward compatible.
- `POST /api/grammar/breakdown/deep` was added and calls the same upgraded breakdown engine.

### Journey Integration Status

Grammar breakdown now infers `recommended_topic_id` and saves a simple Grammar Journey attempt when safe:

- `activity_type = deep_grammar_breakdown`
- `activity_id = recommended_topic_id`
- `score = 100` for non-empty sentence, otherwise `0`
- `feedback = next_practice` or fallback explanation

### Frontend Changes

The existing Grammar result panel now shows extra sections when deep fields are available:

- Sentence level and sentence type
- Main subject, main verb, object/complement
- Modifier phrases
- Clauses
- Grammar patterns
- Common trap
- Simple meaning in Indonesian
- BA context meaning
- Structure steps
- Next practice

Basic Grammar Trainer remains available.

### Testing Checklist

- Python compile check for grammar router and services.
- Frontend JavaScript syntax check.
- Smoke test for old `POST /api/grammar/breakdown` fields.
- Smoke test for new deep fields.
- Smoke test for `POST /api/grammar/breakdown/deep`.
- Backward compatibility check for Topic Library, Grammar Journey, and Basic Trainer endpoints.

### Known Limitations

- Analysis is still rule-based.
- Unusual sentence structures may be approximate.
- No real NLP parser yet.
- No real LLM explanation yet unless configured separately.
- Intermediate Trainer is implemented with static/rule-based content.
- No Error Correction module yet.
- No Sentence Builder yet.

### Next Recommended Phase

Phase 6 - Intermediate Grammar Trainer.

The next phase should add trainer content for gerund vs main verb, relative clause, reduced relative clause, passive voice, and parallel structure.

## Phase 6 - Intermediate Grammar Trainer

Phase 6 selesai. Grammar module sekarang punya Intermediate Grammar Trainer untuk membantu user memahami kalimat TOEFL + Business Analyst yang lebih panjang dan penuh grammar trap.

### Implemented Files

- `backend/services/grammar_trainer_service.py`
- `backend/routers/grammar.py`
- `frontend/app.js`
- `frontend/index.html`
- `scripts/smoke_api.py`
- `docs/GRAMMAR_PROGRESS.md`

### New Endpoints

- `GET /api/grammar/trainer/intermediate`
- `GET /api/grammar/trainer/intermediate/{topic_id}`
- `POST /api/grammar/trainer/intermediate/submit`

### Intermediate Topics Covered

- `gerund_vs_main_verb`
- `infinitive_phrase`
- `relative_clause`
- `reduced_relative_clause`
- `passive_voice`
- `parallel_structure`
- `connector_logic`

### Question Types Implemented

- `identify_main_verb`
- `identify_modifier_phrase`
- `identify_relative_clause`
- `identify_passive_voice`
- `choose_correct_parallel_structure`
- `choose_correct_connector`

The service structure also supports future `simplify_complex_sentence`, `identify_grammar_trap`, and other intermediate question types.

### Trap Item Design

Each intermediate topic includes `trap_items`. Trap items focus on common misunderstanding, for example:

- User thinks `working` is the main verb.
- User reads relative clause as the main clause.
- User treats passive voice as active voice.
- User misses contrast connector logic.

Each trap item includes:

- `trap_type`
- `incorrect_assumption`
- `sentence`
- `question`
- `options`
- `correct_answer`
- `explanation_id`
- `why_wrong_answers_are_wrong`

### How Scoring Works

Scoring is still rule-based:

- Quiz items and trap items are scored together.
- Each item has one `correct_answer`.
- User answer is normalized and compared to the correct answer.
- Score is calculated as `correct_count / total_questions * 100`.
- Passing threshold is `70`.

### Grammar Journey Integration

When user submits Intermediate Trainer answers:

- Backend calculates score.
- Backend calls Grammar Journey attempt logic.
- Attempt uses `activity_type = intermediate_grammar_trainer`.
- Attempt uses `activity_id = topic_id`.
- Mistakes are included for wrong quiz/trap answers.
- Response returns updated `grammar_journey`.

### Frontend Changes

The Grammar page now includes a minimal Intermediate Trainer panel:

- Intermediate topic buttons.
- Explanation, common trap, beginner tip, and BA context.
- Example sentence breakdown.
- Guided practice.
- Trap items.
- Quiz/trap select controls.
- Score, mistakes, and next recommendation after submit.

Existing Grammar Breakdown and Basic Grammar Trainer remain available.

### Testing Checklist

- Python compile check for grammar router and services.
- Frontend JavaScript syntax check.
- Smoke test for Intermediate Trainer topic list.
- Smoke test for `gerund_vs_main_verb` trainer detail.
- Smoke test for `reduced_relative_clause` trainer detail.
- Smoke test for Intermediate Trainer submit.
- Backward compatibility check for Grammar Breakdown, Topic Library, Grammar Journey, and Basic Trainer endpoints.

### Known Limitations

- Trainer data is still static.
- Scoring is still rule-based.
- No database-backed question bank yet.
- Error Correction is not implemented yet.
- Sentence Builder is not implemented yet.
- Advanced Grammar Lab is not implemented yet.
- Grammar Review is not implemented yet.
- Grammar Simulation is not implemented yet.

### Next Recommended Phase

Phase 7 - Grammar Error Correction. Completed.

The next phase should move into Sentence Builder so users can create better BA sentences, not only fix wrong ones.

## Phase 7 - Grammar Error Correction

Phase 7 selesai. Grammar module sekarang punya latihan khusus untuk mengenali grammar error, memahami kenapa kalimat salah, dan memilih corrected sentence yang benar.

### Implemented Files

- `backend/services/grammar_error_service.py`
- `backend/routers/grammar.py`
- `backend/services/grammar_journey_service.py`
- `frontend/app.js`
- `frontend/index.html`
- `scripts/smoke_api.py`
- `docs/GRAMMAR_PROGRESS.md`

### New Endpoints

- `GET /api/grammar/error-correction/categories`
- `GET /api/grammar/error-correction`
- `GET /api/grammar/error-correction?level=basic`
- `GET /api/grammar/error-correction?error_type=passive_voice_error`
- `GET /api/grammar/error-correction/{error_type}`
- `POST /api/grammar/error-correction/submit`

### Error Categories Covered

- `subject_verb_agreement`
- `missing_be_after_modal`
- `wrong_modal_pattern`
- `missing_main_verb`
- `gerund_as_main_verb`
- `passive_voice_error`
- `parallel_structure_error`
- `double_connector`
- `wrong_connector`
- `article_error`
- `preposition_error`
- `word_form_error`

### Example Correction Patterns

- `The requirements is unclear.` -> `The requirements are unclear.`
- `The system must flexible for all users.` -> `The system must be flexible for all users.`
- `The analyst working with stakeholders clarify the requirement.` -> `The analyst working with stakeholders clarifies the requirement.`
- `The data is process by the system.` -> `The data is processed by the system.`
- `Although the workflow is useful, but it is too complex.` -> `Although the workflow is useful, it is too complex.`
- `The implementation will improve efficient.` -> `The implementation will improve efficiency.`

### How Scoring Works

- User memilih corrected sentence dari opsi yang tersedia.
- Jawaban dinormalisasi dan dibandingkan dengan `correct_answer`.
- Score dihitung dengan rumus `correct_count / total_questions * 100`.
- Passing threshold tetap `70`.
- Response menampilkan `incorrect_sentence`, `corrected_sentence`, `explanation_id`, dan daftar `mistakes`.

### Grammar Journey Integration

Saat user submit Error Correction:

- Backend menghitung score.
- Backend menyimpan Grammar attempt dengan `activity_type = grammar_error_correction`.
- `activity_id` memakai `error_type`, atau `mixed_error_correction` jika latihan campuran.
- Mistakes dimasukkan ke attempt payload.
- Response mengembalikan `grammar_journey` terbaru.

### Frontend Changes

Grammar page sekarang punya panel minimal Grammar Error Correction:

- Tombol kategori error.
- Penjelasan aturan, common trap, dan konteks BA.
- Contoh kalimat salah dan corrected sentence.
- Select control untuk memilih jawaban benar.
- Result card berisi score, corrected sentence, explanation, dan rekomendasi.

Existing Grammar Breakdown, Basic Trainer, dan Intermediate Trainer tetap tersedia.

### Testing Checklist

- Python compile check untuk router dan service grammar.
- Frontend JavaScript syntax check.
- Smoke test untuk error correction categories.
- Smoke test untuk daftar correction items.
- Smoke test untuk filter `level=basic`.
- Smoke test untuk detail `missing_be_after_modal`.
- Smoke test untuk detail `passive_voice_error`.
- Smoke test untuk submit Error Correction.
- Backward compatibility check untuk Grammar Breakdown, Topic Library, Journey, Basic Trainer, Intermediate Trainer, dan Deep Breakdown.

### Known Limitations

- Error correction data masih static in-memory.
- Scoring masih rule-based.
- Belum ada database-backed question bank.
- Belum ada free-text correction scoring.
- Sentence Builder belum diimplementasikan.
- Advanced Grammar Lab belum diimplementasikan.
- Grammar Review belum diimplementasikan.
- Grammar Simulation belum diimplementasikan.

### Next Recommended Phase

Phase 8 - Sentence Builder. Completed.

The next phase should expand into Advanced Grammar Lab, with deeper practice for complex sentence mapping, nominalization, hedging, and formal Business Analyst writing.

## Phase 8 - Grammar Sentence Builder

Phase 8 selesai. Grammar module sekarang punya Sentence Builder agar user aktif membangun kalimat, bukan hanya memilih jawaban atau memperbaiki error.

### Implemented Files

- `backend/services/grammar_sentence_builder_service.py`
- `backend/routers/grammar.py`
- `frontend/app.js`
- `frontend/index.html`
- `scripts/smoke_api.py`
- `docs/GRAMMAR_PROGRESS.md`

### New Endpoints

- `GET /api/grammar/sentence-builder/levels`
- `GET /api/grammar/sentence-builder`
- `GET /api/grammar/sentence-builder?level=basic`
- `GET /api/grammar/sentence-builder?mode=arrange_words`
- `GET /api/grammar/sentence-builder/{item_id}`
- `POST /api/grammar/sentence-builder/submit`

### Builder Levels

- `basic`
- `intermediate`
- `advanced_preview`

`advanced_preview` hanya preview kecil untuk formal BA writing. Full Advanced Grammar Lab tetap menjadi Phase 9.

### Builder Modes

- `arrange_words`
- `complete_sentence`
- `combine_sentences`
- `rewrite_formal_ba_sentence`
- `fix_word_order`

### Example Exercises

- `must / requirements / elicit / A business analyst` -> `A business analyst must elicit requirements.`
- `The system must ___ flexible for all users.` -> `be`
- `Must the system generate reports automatically.` -> `The system must generate reports automatically.`
- `The analyst interviews users. The analyst documents requirements.` -> `The analyst interviews users and documents requirements.`
- `The system helps users make reports faster.` -> `The system helps users generate reports more efficiently.`

### How Scoring Works

- Jawaban dinormalisasi: lowercase, final punctuation diabaikan, extra spaces dirapikan.
- Exact match dengan `expected_answer` atau `acceptable_answers` mendapat full score.
- `rewrite_formal_ba_sentence` mendukung partial credit berbasis required keywords.
- Score akhir adalah rata-rata `partial_score` dari item yang dijawab.
- Passing threshold tetap `70`.

### Grammar Journey Integration

Saat user submit Sentence Builder:

- Backend menghitung score.
- Backend menyimpan Grammar attempt dengan `activity_type = grammar_sentence_builder`.
- `activity_id` memakai `level_mode`, atau `mixed_sentence_builder` jika campuran.
- Mistakes dimasukkan ke attempt payload.
- Response mengembalikan `grammar_journey` terbaru.

### Frontend Changes

Grammar page sekarang punya panel minimal Sentence Builder:

- Tombol level: Basic, Intermediate, Advanced Preview.
- Tombol mode sesuai level aktif.
- Prompt dan input parts.
- Text input untuk jawaban user.
- Result card dengan score, expected answer, grammar rule, explanation, dan rekomendasi.

Existing Grammar Breakdown, Basic Trainer, Intermediate Trainer, dan Error Correction tetap tersedia.

### Testing Checklist

- Python compile check untuk router dan service grammar.
- Frontend JavaScript syntax check.
- Smoke test untuk Sentence Builder levels.
- Smoke test untuk daftar Sentence Builder items.
- Smoke test untuk filter `level=basic`.
- Smoke test untuk filter `mode=arrange_words`.
- Smoke test untuk detail `arrange_basic_modal_1`.
- Smoke test untuk submit Sentence Builder.
- Backward compatibility check untuk Grammar Breakdown, Topic Library, Journey, Basic Trainer, Intermediate Trainer, Deep Breakdown, dan Error Correction.

### Known Limitations

- Sentence builder data masih static in-memory.
- Scoring masih rule-based.
- Free-text rewrite scoring masih sederhana dan berbasis keyword.
- Belum ada database-backed exercise bank.
- Advanced Grammar Lab belum fully implemented.
- Grammar Review belum diimplementasikan.
- Grammar Simulation belum diimplementasikan.

### Next Recommended Phase

Phase 9 - Advanced Grammar Lab. Completed.

The next phase should analyze accumulated Grammar attempts and show weak topics, repeated mistakes, and a review queue.

## Phase 9 - Advanced Grammar Lab

Phase 9 selesai. Grammar module sekarang punya Advanced Grammar Lab untuk TOEFL, academic writing, dan dokumentasi Business Analyst formal.

### Implemented Files

- `backend/services/grammar_advanced_service.py`
- `backend/routers/grammar.py`
- `frontend/app.js`
- `frontend/index.html`
- `scripts/smoke_api.py`
- `docs/GRAMMAR_PROGRESS.md`

### New Endpoints

- `GET /api/grammar/advanced/topics`
- `GET /api/grammar/advanced/topics/{topic_id}`
- `GET /api/grammar/advanced/practice`
- `GET /api/grammar/advanced/practice?topic_id=nominalization`
- `GET /api/grammar/advanced/rewrite`
- `GET /api/grammar/advanced/rewrite?topic_id=formal_ba_writing`
- `POST /api/grammar/advanced/practice/submit`
- `POST /api/grammar/advanced/rewrite/submit`

### Advanced Topics Covered

- `complex_sentence_mapping`
- `nominalization`
- `hedging_language`
- `inversion`
- `conditional_sentence`
- `academic_connectors`
- `formal_ba_writing`

### Practice Item Design

Practice items use multiple-choice questions for advanced recognition:

- identify nominalization
- identify hedging
- identify academic connector
- identify conditional logic
- identify inversion pattern
- simplify advanced sentence
- choose formal sentence
- choose professional rewrite

Each item includes `advanced_pattern`, `simpler_version`, `explanation_id`, `related_topic_id`, and BA context.

### Rewrite Item Design

Rewrite items ask users to transform simpler/informal sentences into more formal BA sentences. Each rewrite item includes:

- `original_sentence`
- `expected_answer`
- `acceptable_answers`
- `required_keywords`
- `explanation_id`
- `professional_usage_note`
- `grammar_rule_id`

### How Scoring Works

- Practice scoring uses exact match with `correct_answer`.
- Rewrite scoring normalizes casing, final punctuation, and extra spaces.
- Rewrite exact/acceptable matches get full score.
- Non-exact rewrite answers can receive partial credit based on required keywords.
- Passing threshold remains `70`.

### Grammar Journey Integration

When user submits Advanced Practice or Advanced Rewrite:

- Backend calculates score.
- Backend saves Grammar attempt with `advanced_grammar_practice` or `advanced_grammar_rewrite`.
- `activity_id` uses the advanced `topic_id`.
- Mistakes are included in the attempt payload.
- Response returns updated `grammar_journey`.

### Frontend Changes

Grammar page now includes a minimal Advanced Grammar Lab panel:

- Advanced topic buttons.
- Beginner bridge.
- Professional usage and common trap.
- Examples with simpler version and breakdown.
- Practice quiz selects.
- Rewrite text inputs.
- Score, expected answer, required keywords, feedback, and recommendation.

Existing Grammar Breakdown, Basic Trainer, Intermediate Trainer, Error Correction, and Sentence Builder remain available.

### Testing Checklist

- Python compile check for grammar router and services.
- Frontend JavaScript syntax check.
- Smoke test for advanced topic list.
- Smoke test for `nominalization` topic detail.
- Smoke test for `formal_ba_writing` topic detail.
- Smoke test for advanced practice items.
- Smoke test for advanced rewrite items.
- Smoke test for advanced practice submit.
- Smoke test for advanced rewrite submit.
- Backward compatibility check for Grammar Breakdown, Topic Library, Journey, Basic Trainer, Intermediate Trainer, Error Correction, and Sentence Builder.

### Known Limitations

- Advanced grammar data is still static.
- Scoring is still rule-based.
- Rewrite scoring is still simple and keyword-based.
- No database-backed advanced question bank yet.
- No real LLM-based writing evaluation yet.
- Grammar Review is not implemented yet.
- Grammar Simulation is not implemented yet.

### Next Recommended Phase

Phase 10 - Grammar Review and Mistake Pattern. Completed.

The next phase should add a TOEFL-style Grammar Simulation with timed practice and a final report.

## Phase 10 - Grammar Review and Mistake Pattern Analysis

Phase 10 selesai. Grammar module sekarang punya review system yang menganalisis attempt grammar, topic mastery, mistake pattern, review queue, dan recommended next practice.

### Implemented Files

- `backend/services/grammar_review_service.py`
- `backend/routers/grammar.py`
- `frontend/app.js`
- `frontend/index.html`
- `scripts/smoke_api.py`
- `docs/GRAMMAR_PROGRESS.md`

### New Endpoints

- `GET /api/grammar/review`
- `GET /api/grammar/mistake-patterns`
- `GET /api/grammar/review-queue`
- `GET /api/grammar/weakness-summary`
- `GET /api/grammar/recommended-practice`

### Data Sources Used

- `learning_attempts` with `skill_type = grammar`
- `mistakes_json` from grammar attempts
- `skill_mastery` with `skill_type = grammar`
- Grammar Journey summary from `grammar_journey_service`
- Static fallback review data if attempts are still limited

### Mistake Classification Rules

Mistakes are classified with simple rule-based checks from:

- `error_type`
- `related_topic_id`
- `topic_id`
- `question_type`
- `trap_type`
- `activity_id`
- `activity_type`
- text content inside `mistakes_json`

Supported categories include:

- `subject_verb_agreement`
- `missing_be_after_modal`
- `modal_verb_pattern`
- `main_verb_detection`
- `gerund_vs_main_verb`
- `reduced_relative_clause`
- `passive_voice`
- `parallel_structure`
- `connector_logic`
- `nominalization`
- `formal_ba_writing`
- `word_order`
- `sentence_builder`
- `unknown_grammar_issue`

### Review Queue Design

Review queue combines:

- mistake patterns with high frequency
- low mastery topics
- deterministic fallback if there is not enough practice data

Each review item includes priority, topic, reason, action label, target endpoint, estimated minutes, source, and status.

### Recommended Practice Design

The system chooses one best next practice based on the primary mistake pattern or weakest topic. The recommendation includes:

- recommended topic
- recommended module
- reason
- next action
- target endpoint
- estimated minutes
- difficulty

### Frontend Changes

Grammar page now includes a minimal Grammar Review panel:

- weakness summary
- primary and secondary weakness cards
- mistake pattern cards
- review queue cards
- recommended practice card
- mentor message
- refresh review button

Existing Grammar Breakdown, Basic Trainer, Intermediate Trainer, Error Correction, Sentence Builder, and Advanced Grammar Lab remain available.

### Testing Checklist

- Python compile check for grammar router and services.
- Frontend JavaScript syntax check.
- Smoke test for Grammar Review.
- Smoke test for Mistake Patterns.
- Smoke test for Review Queue.
- Smoke test for Weakness Summary.
- Smoke test for Recommended Practice.
- Backward compatibility check for all previous Grammar phases.

### Known Limitations

- Analysis is still rule-based.
- Review quality depends on available grammar attempts.
- No dedicated grammar review database table yet.
- No advanced analytics yet.
- No long-term spaced repetition scheduler yet.
- Grammar Simulation is not implemented yet.

### Next Recommended Phase

Phase 11 - Grammar Simulation. Completed.

The Grammar phase roadmap is now complete through Simulation. Next improvements should focus on UI polish, persistence, analytics quality, or replacing static content with database-backed content.

## Phase 11 - Grammar Simulation

Phase 11 selesai. Grammar module sekarang punya timed simulation untuk mengukur readiness grammar setelah user memakai Basic Trainer, Intermediate Trainer, Error Correction, Sentence Builder, Advanced Lab, dan Review.

### Implemented Files

- `backend/services/grammar_simulation_service.py`
- `backend/routers/grammar.py`
- `frontend/app.js`
- `frontend/index.html`
- `scripts/smoke_api.py`
- `docs/GRAMMAR_PROGRESS.md`

### New Endpoints

- `GET /api/grammar/simulation/modes`
- `POST /api/grammar/simulation/start`
- `POST /api/grammar/simulation/submit`
- `GET /api/grammar/simulation/result/{session_id}`
- `GET /api/grammar/simulation/history`

### Simulation Modes

- `short`: 10 questions, 10 minutes
- `medium`: 20 questions, 20 minutes
- `full`: 40 questions, 40 minutes

### Question Types

- `identify_subject`
- `identify_main_verb`
- `identify_modifier_phrase`
- `choose_correct_sentence`
- `error_correction`
- `sentence_completion`
- `connector_logic`
- `passive_voice`
- `parallel_structure`
- `nominalization`
- `formal_ba_writing`
- `grammar_meaning`
- `sentence_builder`

### Scoring Logic

- Multiple-choice answers use normalized exact match.
- Final punctuation and extra spaces are ignored.
- Sentence Builder and Formal BA Writing can receive keyword-based partial credit.
- Total score is average points across all questions.

### Level Breakdown Design

Simulation result groups score by level:

- `basic`
- `intermediate`
- `advanced`
- `mixed`

Each level breakdown includes score, correct count, total questions, and status.

### Subskill Breakdown Design

Simulation result groups score by `skill_area`, such as:

- `main_verb_detection`
- `modal_verb`
- `passive_voice`
- `parallel_structure`
- `connector_logic`
- `nominalization`
- `formal_ba_writing`
- `sentence_builder`

Weakest subskill drives the next recommendation.

### Recommendation Logic

The service recommends the next practice endpoint from the weakest subskill:

- weak `main_verb_detection` -> Intermediate Gerund vs Main Verb
- weak `passive_voice` -> Intermediate Passive Voice
- weak `modal_verb` -> Basic Modal Verb
- weak `formal_ba_writing` -> Advanced Formal BA Writing
- weak `error_correction` -> Error Correction
- weak `sentence_builder` -> Sentence Builder

### Frontend Changes

Grammar page now includes a minimal Grammar Simulation panel:

- mode cards: Short, Medium, Full
- start simulation button
- question list
- select or text input answers
- submit simulation
- final score
- level breakdown
- subskill breakdown
- answer review summary
- simulation history

Existing Grammar Breakdown, Basic Trainer, Intermediate Trainer, Error Correction, Sentence Builder, Advanced Lab, and Grammar Review remain available.

### Testing Checklist

- Python compile check for grammar router and services.
- Frontend JavaScript syntax check.
- Smoke test for simulation modes.
- Smoke test for simulation start.
- Smoke test for simulation submit.
- Smoke test for result lookup.
- Smoke test for simulation history.
- Backward compatibility check for all previous Grammar phases.

### Known Limitations

- Simulation question bank is still static.
- Scoring is still rule-based.
- In-memory sessions/history reset when backend restarts.
- No dedicated simulation database table yet.
- No advanced proctoring or real TOEFL timing behavior yet.
- No real LLM evaluation for open-ended answers yet.

### Next Recommended Work

- Persist simulation sessions/results in SQLite.
- Add database-backed Grammar content bank.
- Improve Grammar UI grouping so the page does not become too long.
- Add analytics charts for Grammar readiness.
- Add optional LLM scoring for open-ended formal rewrite answers.

## Phase 12 - Grammar Hub Navigation Refactor

Phase 12 selesai sebagai frontend UX refactor. Grammar page tidak lagi menampilkan semua fitur sekaligus saat pertama dibuka.

### Problem Solved

Sebelumnya Grammar page langsung merender semua fitur:

- Grammar Breakdown
- Basic Trainer
- Intermediate Trainer
- Error Correction
- Sentence Builder
- Advanced Lab
- Review
- Simulation

Akibatnya halaman terasa terlalu panjang, padat, dan membingungkan untuk pemula.

### Implemented Frontend Changes

- Menambahkan state `grammarHub`.
- Menambahkan active section flow:
  - `menu`
  - `breakdown`
  - `basic_trainer`
  - `intermediate_trainer`
  - `error_correction`
  - `sentence_builder`
  - `advanced_lab`
  - `review`
  - `simulation`
- Menambahkan Grammar Hub menu cards. Catatan terbaru: quick-pick cards kemudian dihapus karena duplikatif dengan roadmap.
- Menambahkan helper:
  - `renderGrammarHub()`
  - `setGrammarSection()`
  - `grammarBackButton()`
  - `renderGrammarSectionShell()`
  - `grammarBreakdownPanel()`
- Menambahkan tombol `Kembali ke Menu Grammar` di setiap sub-section.

### New Navigation Behavior

Saat user membuka Grammar page:

1. User melihat Grammar Hub menu.
2. User memilih satu fokus latihan.
3. Hanya section yang dipilih yang muncul.
4. User bisa kembali ke Grammar Hub melalui tombol back.

Grammar page tidak lagi merender semua panel sekaligus.

### Sub-menu Flow

- Grammar Hub -> Grammar Breakdown
- Grammar Hub -> Basic Grammar Trainer
- Grammar Hub -> Intermediate Grammar Trainer
- Grammar Hub -> Error Correction
- Grammar Hub -> Sentence Builder
- Grammar Hub -> Advanced Grammar Lab
- Grammar Hub -> Grammar Review
- Grammar Hub -> Grammar Simulation

Setiap feature function lama tetap dipertahankan. Refactor ini hanya mengubah navigasi dan rendering.

### Known Limitations

- Section state masih disimpan di localStorage/API state sederhana.
- Belum ada tab horizontal atau breadcrumb lanjutan.
- Beberapa panel internal masih panjang dan bisa dipoles lagi setelah hub navigation stabil.
- Belum ada lazy API preload per section.

### Next Recommended Polish

- Tambahkan visual grouping dalam section yang panjang.
- Tambahkan progress mini card di Grammar Hub.
- Tambahkan rekomendasi otomatis di Hub: `Lanjutkan latihan terakhir`.
- Buat mobile navigation untuk Grammar Hub lebih compact.

## Phase 12 - Guided Grammar Learning Path UX

Status: Completed

### Problem Solved

Grammar Hub sebelumnya sudah memisahkan fitur, tetapi masih terasa seperti kumpulan tool yang setara. Pemula belum langsung tahu harus mulai dari mana, apa urutan belajarnya, dan kapan Grammar Lab dianggap selesai.

### New Start Here Card

Grammar Hub sekarang menampilkan kartu besar `Mulai dari Sini` di bagian paling atas. Kartu ini memperlihatkan:

- level grammar saat ini jika tersedia
- progress grammar sederhana
- rekomendasi langkah berikutnya
- penjelasan pemula tentang kenapa harus mulai dari langkah tersebut
- tombol `Mulai Belajar Terarah`

Jika data review atau journey belum tersedia, rekomendasi aman diarahkan ke `Basic Grammar Trainer`.

### Recommended Learning Path

Hub sekarang menampilkan roadmap `Alur Belajar yang Disarankan`:

1. Basic Foundation
2. Sentence Breakdown
3. Intermediate Grammar
4. Error Correction
5. Sentence Builder
6. Advanced Grammar
7. Review Weakness
8. Final Test

Setiap langkah menjelaskan fungsi module, target belajar, dan tombol untuk membuka section tersebut.

### Finish Target

Ditambahkan section `Target Finish Grammar` dengan target jelas:

> User dianggap selesai Grammar Lab jika mampu menyelesaikan Full Grammar Simulation dengan skor minimal 75%.

Section ini juga menampilkan checklist ringkas agar user memahami posisi belajar saat ini dan finish line.

### Improved Beginner Guidance

Copy pada roadmap card diperjelas agar setiap fitur menjawab:

- fitur ini dipakai untuk apa
- kapan sebaiknya digunakan
- hasil belajar apa yang diharapkan

Tombol back pada sub-section juga diarahkan ke `Kembali ke Grammar Learning Path` agar konsep jalur belajar tetap konsisten.

### Known Limitations

- Progress checklist masih sederhana dan belum membaca seluruh riwayat simulasi secara detail.
- Rekomendasi otomatis masih rule-based dari grammar review, grammar journey, atau fallback progress lokal.
- Hub belum punya animasi stepper atau status selesai per module yang benar-benar granular.
- Quick pick sudah dihapus karena membuat dua jalur navigasi yang ambigu. User diarahkan memakai Start Here dan Roadmap saja.

### Next Recommended Polish

- Tandai setiap langkah roadmap sebagai `Belum mulai`, `Sedang dipelajari`, atau `Selesai` dari data attempt.
- Tambahkan last activity dan tombol `Lanjutkan terakhir`.
- Tampilkan skor Full Grammar Simulation terakhir jika sudah ada.
- Rapikan layout internal setiap sub-section agar terasa seperti satu workflow, bukan form panjang.

## Phase 13 - Grammar Subfeature Progress Integration

Status: Completed

### Problem Solved

Semua subfitur Grammar sudah ada, tetapi sebelumnya user belum bisa melihat status tiap module. Grammar Hub sekarang tidak hanya menjadi menu, tetapi juga menunjukkan progress nyata untuk setiap bagian Grammar Lab.

### New Backend Progress Service

Implemented file:

- `backend/services/grammar_progress_service.py`

Service ini menghitung progress dari data yang sudah ada:

- `learning_attempts`
- `skill_mastery`
- Grammar Journey
- Grammar Review
- Grammar Simulation history jika tersedia

Tidak ada database migration baru pada phase ini.

### New Progress Endpoints

New endpoints:

- `GET /api/grammar/progress`
- `GET /api/grammar/progress/summary`
- `GET /api/grammar/progress/modules`
- `GET /api/grammar/progress/path`
- `GET /api/grammar/progress/recommended-section`
- `GET /api/grammar/progress/finish-status`

### Module Progress Rules

Tracked modules:

- `grammar_breakdown`
- `basic_trainer`
- `intermediate_trainer`
- `error_correction`
- `sentence_builder`
- `advanced_lab`
- `review`
- `simulation`

Each module returns:

- status
- progress percent
- completed items
- total items
- last score
- best score
- attempt count
- next action
- recommended flag
- target score
- frontend section key

Status labels:

- `not_started`
- `in_progress`
- `need_review`
- `completed`
- `recommended`
- `locked`

### Frontend Progress Summary

Grammar Hub now shows:

- Overall Grammar Progress
- Current Grammar Level
- Active Module
- Recommended Next Step
- Finish Target
- Completed Modules

The `Mulai dari Sini` card now uses backend recommendation when available, with local fallback to Basic Grammar Trainer.

### Learning Path Progress Cards

Each Grammar roadmap card now shows:

- status badge
- progress bar
- completed items / total items
- last score
- next action
- contextual button label: `Mulai`, `Lanjutkan`, `Ulangi`, `Selesai`, or `Direkomendasikan`

Quick Pick cards were removed after UX testing because they duplicated the Learning Path and made module choice ambiguous. The Learning Path cards now act as the single visible navigation surface for Grammar modules.

## Grammar Hub Quick Pick Removal

Status: Completed

### Problem Solved

The `Pilih Cepat` section duplicated the same module cards already shown in the Grammar Learning Path. Beginner users could not tell whether they should follow the roadmap or choose a quick card, so the hub felt like two competing navigation systems.

### Implemented Changes

- Removed `renderGrammarQuickPick()` from the Grammar Hub.
- Removed the unused `grammarHubCard()` helper.
- Kept Start Here, Learning Path, Progress Summary, Status Board, and Finish Target.
- Existing Grammar subfeatures remain accessible through the Learning Path cards and recommendation button.

### UX Result

Grammar Hub now has one clear flow:

1. Check current progress.
2. Use `Mulai / Lanjutkan Rekomendasi`.
3. Follow `Alur Belajar yang Disarankan`.
4. Return from any subfeature to Grammar Learning Path.

### Finish Status Rule

Finish rule:

> Grammar Lab is finished when Full Grammar Simulation reaches at least 75%.

The finish status endpoint returns whether the user has finished, the full simulation score if known, and a beginner-friendly message.

### Testing Checklist

- `python3 -m py_compile backend/main.py backend/routers/grammar.py backend/services/grammar_progress_service.py`
- `node --check frontend/app.js`
- `python3 scripts/smoke_api.py`

### Known Limitations

- Progress is calculated from existing attempts.
- There is no dedicated grammar module progress table yet.
- Some module progress depends on consistent `activity_type` and `activity_id`.
- Simulation history may still be temporary if only in-memory session history is available.
- Module completion is rule-based and can be refined after real user data accumulates.

### Next Recommended Polish

- Add per-topic completion state inside each Grammar subfeature.
- Persist simulation mode in a dedicated table later.
- Add `last activity` and `continue last exercise` inside each Grammar module card.
- Improve mobile layout for progress-heavy Grammar Hub cards.

## Grammar Hub Progress UI Fix

Status: Completed

### What Changed

- Grammar Hub now shows visible progress per subfeature.
- Each Grammar subfeature card shows status, progress percentage, completed items, last score, and next action.
- The `Mulai dari Sini` button opens the recommended module from Grammar Progress data, with fallback to Basic Grammar Trainer.
- Learning Path cards now show progress per step instead of static descriptions only.
- Finish target is visible: Grammar Lab is finished when Full Grammar Simulation reaches at least 75%.
- A Grammar status board now summarizes how many subfeatures are recommended, not started, in progress, need review, or completed.
- Every Grammar subfeature page now shows its own progress banner so the selected feature still feels connected to the Grammar Journey.
- Roadmap progress now reads the actual `learning_path` array from `/api/grammar/progress` instead of falling back to local zero-progress data.
- Frontend progress loading accepts both the fixed array shape and the older nested `learning_path.learning_path` shape for safer compatibility.

## Basic Grammar Trainer Quiz State Fix

### Problem Solved

- Quiz pendek sebelumnya memakai satu state global untuk `answers` dan `result`.
- Saat user pindah topic lalu kembali, pilihan jawaban dan hasil submit terlihat hilang.
- UI juga belum memberi status yang jelas apakah sebuah topic sudah mulai dijawab, siap submit, selesai, atau perlu diulang.

### Implemented Changes

- Basic Grammar Trainer now stores quiz answers and submit results per topic in frontend state.
- Topic buttons now show status:
  - `Belum mulai`
  - `Mulai dijawab`
  - `Siap submit`
  - `Selesai`
  - `Perlu diulang`
- Quiz cards now show per-question feedback after submit.
- If a user selects an answer, moves to another topic, then returns, the previous selection is preserved.
- If a submitted topic is reopened, the score and feedback remain visible.

### Known Limitations

- This state is frontend/local-state based and depends on saved browser state.
- Backend progress still depends on submit actions, not on merely selecting an answer.
- The same persistence pattern has now been applied to the other major Grammar subfeatures.

## Grammar Subfeature UX Hardening

Status: Completed

### Problem Solved

Basic Grammar Trainer already had clearer per-topic progress, but the other Grammar subfeatures still felt disconnected. User answers could look lost after switching topic, category, mode, or simulation mode, and several panels did not clearly show whether the current activity was belum mulai, sedang berjalan, siap submit, selesai, atau perlu diulang.

### Implemented Changes

- Intermediate Grammar Trainer now stores answer and submit result state per topic.
- Grammar Error Correction now stores answer and submit result state per error category.
- Grammar Sentence Builder now stores answer and submit result state per level and mode.
- Advanced Grammar Lab now stores practice and rewrite state per advanced topic.
- Grammar Simulation now stores session, answers, and result per simulation mode.
- Grammar Breakdown keeps the last sentence and analysis visible after leaving and returning to the section.
- Grammar Review now explains how review progress should be completed: open the recommended practice, finish the weak module, then refresh review.

### UI Result

- Topic, category, and mode cards now show status badges, score, and progress bars.
- Quiz/practice items show whether an answer has been filled, submitted correctly, or needs review.
- Switching to another Grammar subfeature no longer forces the user to restart choices that were already filled.
- Each subfeature has a progress banner that keeps the user connected to Grammar Journey.

### Testing Checklist

- Intermediate Trainer: choose an answer, switch topic, return, and confirm the answer remains visible.
- Error Correction: choose an answer, switch error category, return, and confirm the answer remains visible.
- Sentence Builder: type an answer, switch mode, return, and confirm the typed answer remains visible.
- Advanced Lab: choose practice/rewrite answers, switch topic, return, and confirm state remains visible.
- Simulation: start or answer in one mode, switch mode, return, and confirm session state is preserved.

## Grammar Subfeature UI Polish

Status: Completed

### Problem Solved

Several Grammar subfeature panels had uneven spacing. In Grammar Breakdown, the input panel stretched to match the long result panel, causing large empty gaps between the beginner tip, textarea, help button, and submit button. Other subfeatures also needed more consistent spacing, card density, and clearer colors.

### Implemented Changes

- Added scoped `#grammarView` UI rules so Grammar polish does not disturb Reading, Vocabulary, Writing, or other modules.
- Improved Grammar two-column layouts so side panels align to the top instead of stretching awkwardly.
- Made Grammar Breakdown input panel compact and sticky on desktop.
- Grouped Grammar Breakdown help actions into one action row.
- Refined Grammar cards, chips, quiz answer cards, status banners, and progress bars.
- Improved Grammar color usage with teal, mint, blue, green, and amber states.
- Reduced oversized gaps and made nested cards easier to scan.

### UX Result

Grammar subfeatures now feel closer to a focused learning workspace:

- input and result panels are balanced
- progress/status cards are easier to read
- quiz states are visually clearer
- long breakdown results have better hierarchy
- buttons no longer appear stranded by excessive vertical spacing

### Status Labels

- `not_started` -> `Belum mulai`
- `in_progress` -> `Sedang berjalan`
- `need_review` -> `Perlu diulang`
- `completed` -> `Selesai`
- `recommended` -> `Direkomendasikan`
- `locked` -> `Belum dibuka`

### Button Labels

- `not_started` -> `Mulai`
- `in_progress` -> `Lanjutkan`
- `need_review` -> `Ulangi`
- `completed` -> `Lihat / Ulangi`
- `recommended` -> `Lanjutkan Rekomendasi`
- `locked` -> `Belum Dibuka`

## Codex Next Prompt

Use this prompt for the next improvement:

```text
You are working on the repository IAdhamK/toefl-ba.

Read first:
- docs/GRAMMAR_SPEC.md
- docs/GRAMMAR_PROGRESS.md
- backend/main.py
- backend/routers/grammar.py
- backend/services/grammar_topic_service.py
- backend/services/grammar_journey_service.py
- backend/services/grammar_trainer_service.py
- backend/services/grammar_error_service.py
- backend/services/grammar_sentence_builder_service.py
- backend/services/grammar_advanced_service.py
- backend/services/grammar_review_service.py
- backend/services/grammar_simulation_service.py
- frontend/app.js
- docs/GRAMMAR_PROGRESS.md

Task:
Improve the completed Grammar module after Phase 11.

Goal:
Polish the Grammar user experience and make the completed Grammar system easier to navigate for beginner Indonesian users.

Scope:
1. Keep all existing grammar endpoints working.
2. Do not add database migrations unless explicitly requested.
3. Improve Grammar page navigation and grouping.
4. Make completed phases easier to access:
   - Journey
   - Breakdown
   - Basic Trainer
   - Intermediate Trainer
   - Error Correction
   - Sentence Builder
   - Advanced Lab
   - Review
   - Simulation

Frontend requirements:
1. Keep UI beginner-friendly in Bahasa Indonesia.
2. Do not remove existing features.
3. Improve layout density and clarity.

Testing:
Run:
- python3 -m py_compile backend/main.py
- node --check frontend/app.js
- python3 scripts/smoke_api.py
```
