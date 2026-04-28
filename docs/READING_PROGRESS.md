# Reading Progress

Dokumen ini melacak arah pengembangan fitur Reading di TOEFL Analyst AI. Tujuannya agar pengembangan berikutnya bisa dilakukan bertahap, tidak merusak MVP, dan mudah dipahami oleh developer pemula maupun Codex pada prompt berikutnya.

## Reading Vision

Reading Feature akan berkembang dari Reading Analyzer sederhana menjadi sistem belajar Reading TOEFL berbasis journey. User tidak hanya menjawab soal, tetapi juga dibimbing untuk memahami judul, kalimat, main idea, vocabulary in context, evidence sentence, dan alasan kenapa opsi benar atau salah.

Target akhirnya:

- User tahu level Reading mereka saat ini.
- User paham sub-skill Reading mana yang kuat dan lemah.
- User bisa belajar passage secara bertahap sebelum menjawab soal.
- User mendapat review jawaban yang jelas, termasuk evidence dan distractor analysis.
- User bisa latihan simulasi TOEFL Reading dengan timer dan final report.
- Semua progres masuk ke Integrated User Learning Journey.

## Current Status

Status saat ini: MVP Reading sudah ada, tetapi belum menjadi sistem Reading penuh.

Yang sudah tersedia:

- Reading Analyzer dasar.
- Passage Business Analyst context.
- TOEFL-style questions dasar.
- Submit Reading dan scoring.
- Progress Reading di dashboard.
- Journey panel umum untuk Reading.
- Contextual Bantuan ID untuk passage, question, option, vocabulary, dan grammar insight.
- Backend scoring sudah mengirim journey update.
- Reading Journey Foundation Phase 1:
  - endpoint `GET /api/reading/journey`
  - endpoint `GET /api/reading/levels`
  - endpoint `GET /api/reading/recommendation`
  - endpoint `POST /api/reading/attempt`
  - panel Reading Journey Summary di halaman Reading
  - tracking awal sub-skill `general_meaning`, `main_idea`, `detail_information`, dan `vocabulary_context`
- Reading Sub-skill Trainer Phase 2:
  - endpoint `GET /api/reading/subskills`
  - endpoint `GET /api/reading/trainer/{sub_skill}`
  - `POST /api/reading/attempt` menerima `sub_skill`
  - trainer awal untuk `main_idea`, `detail_information`, `vocabulary_context`, `inference`, dan `sentence_simplification`
  - halaman Reading menampilkan progress 10 sub-skill dan selector trainer

Yang belum tersedia:

- Guided Reading mode.
- Evidence sentence per jawaban.
- Distractor analysis lengkap.
- Reading weakness report.
- TOEFL Reading simulation dengan timer.
- Reading-specific review history.

## Implementation Phases

### Phase 1 — Reading Journey Foundation

Tujuan: membuat fondasi journey khusus Reading tanpa mengubah pengalaman utama secara drastis.

Deliverables:

- Reading level berdasarkan progres user.
- Reading score ringkas.
- Tracking sub-skill dasar:
  - `general_meaning`
  - `main_idea`
  - `detail_information`
  - `vocabulary_context`
- Reading next action dalam Bahasa Indonesia.
- Struktur data awal untuk Reading attempts dan sub-skill mastery.
- Dokumentasi endpoint/data yang dibutuhkan.

Completed:

- Reading masuk Integrated User Learning Journey secara umum.
- Scoring Reading sudah bisa memperbarui progress.
- Contextual Bantuan ID Reading sudah lebih spesifik untuk question dan option.
- Reading service dan router Phase 1 dibuat.
- Reading page menampilkan Reading level, score, completed passages, strongest/weakest sub-skill, dan next action.
- Smoke test membaca endpoint Reading Journey Foundation.

Pending:

- UI Reading Journey yang lebih detail.
- Reading-specific review history.
- Evidence sentence dan distractor analysis.

Testing checklist:

- User submit Reading dan progress Reading naik.
- Reading journey tidak reset saat app dibuka ulang.
- Response scoring tetap kompatibel dengan frontend lama.
- Smoke test membaca summary Reading tanpa error.
- Smoke test menyimpan reading attempt tanpa error.

### Phase 2 — Reading Sub-skill Trainer

Tujuan: memisahkan latihan Reading berdasarkan tipe kemampuan.

Deliverables:

- Trainer untuk:
  - main idea
  - detail
  - vocabulary
  - inference
  - sentence simplification
- Bank soal dengan `question_type`.
- Scoring per sub-skill.
- Feedback singkat per tipe soal.

Completed:

- Reading service menyimpan dan mengklasifikasikan `sub_skill`/`question_type`.
- `POST /api/reading/attempt` memperbarui mastery sub-skill yang dikirim.
- Endpoint `GET /api/reading/subskills` mengembalikan progress 10 sub-skill Reading.
- Endpoint `GET /api/reading/trainer/{sub_skill}` mengembalikan konten trainer untuk 5 sub-skill awal.
- UI Reading menampilkan progress sub-skill dan selector trainer.
- Bantuan ID tetap tersedia untuk trainer passage, question, dan option.
- Smoke test mencakup subskills, trainer main idea, attempt main idea, dan attempt vocabulary context.

Pending:

- Trainer untuk `reference`, `author_purpose`, `paragraph_function`, dan `ba_case_analysis`.
- Bank soal yang lebih besar dan tersimpan di database.
- Feedback distractor per opsi salah.
- Review history khusus Reading.

Testing checklist:

- User bisa memilih tipe latihan. Done.
- Setiap jawaban memperbarui mastery tipe soal yang benar. Done.
- Feedback sesuai tipe soal, bukan generic. Done untuk trainer awal.
- Bantuan ID tetap muncul di passage, question, dan option trainer. Done.

### Phase 3 — Guided Reading Mode

Tujuan: membantu pemula memahami passage sebelum menjawab soal.

Deliverables:

- Title understanding.
- Sentence breakdown per kalimat penting.
- Main idea detection.
- Vocabulary context.
- Guided notes dalam Bahasa Indonesia.
- Bantuan ID memakai passage context.

Completed:

- Bantuan ID sudah kontekstual.

Pending:

- UI Guided Reading.
- Segmentasi passage per paragraph/sentence.
- Step-by-step reading guidance.

Testing checklist:

- Passage dapat dibaca dalam langkah kecil.
- User bisa melihat arti kalimat dan vocabulary context.
- Guided mode tidak mengganggu mode quiz.

### Phase 4 — Answer Review

Tujuan: setelah submit, user paham kenapa jawaban benar/salah.

Deliverables:

- Correct/wrong explanation.
- Evidence sentence dari passage.
- Distractor analysis untuk opsi salah.
- Explanation dalam Bahasa Indonesia.
- Link ke Bantuan ID untuk evidence sentence.

Completed:

- Basic result dan explanation sudah ada.
- Bantuan ID option sudah mulai mengenali opsi kuat/lemah.

Pending:

- Evidence sentence data.
- Distractor analysis terstruktur.
- UI review setelah submit.

Testing checklist:

- Setiap soal punya explanation yang spesifik.
- Jawaban salah menampilkan alasan dan evidence.
- Distractor tidak dijelaskan secara generic.

### Phase 5 — Reading Review

Tujuan: user tahu pola kelemahan Reading mereka.

Deliverables:

- Weakness report.
- Mistake pattern.
- Recommended practice.
- Review list per sub-skill.
- Daily Reading plan.

Completed:

- Integrated Journey sudah punya daily plan umum.

Pending:

- Reading-specific analytics.
- Mistake classification.
- Recommended practice berdasarkan sub-skill.

Testing checklist:

- User melihat kelemahan Reading paling dominan.
- Recommendation berubah setelah beberapa attempt.
- Review list tidak kosong jika ada kesalahan.

### Phase 6 — TOEFL Simulation

Tujuan: menyediakan latihan Reading seperti TOEFL mini/full simulation.

Deliverables:

- Timer.
- Full set Reading.
- Navigation antar soal.
- Final report.
- Score estimate.
- Sub-skill breakdown.

Completed:

- Belum dimulai.

Pending:

- Simulation state.
- Timer UI.
- Full set data.
- Final report generation.

Testing checklist:

- Timer berjalan dan tidak reset saat pindah soal.
- User bisa submit full set.
- Final report menampilkan score dan sub-skill.

## Completed Items

- Reading Analyzer MVP.
- Reading scoring endpoint compatibility.
- Reading progress masuk dashboard.
- Reading masuk Integrated User Learning Journey.
- Reading Bantuan ID kontekstual untuk question dan option.
- Documentation foundation dibuat:
  - `docs/READING_PROGRESS.md`
  - `docs/READING_SPEC.md`

## Pending Items

- Reading-specific data model.
- Reading-specific data model yang lebih detail untuk fase lanjut.
- Guided Reading UI.
- Question Trainer UI.
- Answer Review UI.
- Reading Review analytics.
- TOEFL Simulation.
- E2E tests untuk alur Reading.

## Next Codex Prompt Recommendation

Gunakan prompt ini untuk Phase 2:

```text
You are working inside repository IAdhamK/toefl-ba.

Task: Implement Phase 2 — Reading Sub-skill Trainer.

Use docs/READING_PROGRESS.md and docs/READING_SPEC.md as the source of truth.

Goals:
- Preserve Reading Journey Foundation.
- Add trainer mode for question types:
  main_idea, detail, vocabulary, reference, inference, purpose.
- Add question_type and sub_skill handling without breaking existing lessons.
- Add API endpoint for Reading trainer if needed.
- Add beginner-friendly Indonesian feedback per question type.
- Keep Indonesian beginner-friendly wording.
- Add smoke tests.
- Update documentation.

Do not rewrite the whole app.
Do not remove existing endpoints.
Do not break Integrated User Learning Journey.

Final response:
- Summary of changes
- Files modified
- How to test
- Remaining limitations
```
