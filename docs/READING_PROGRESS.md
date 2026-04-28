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

Yang belum tersedia:

- Reading sub-skill mastery khusus.
- Guided Reading mode.
- Question Trainer berdasarkan tipe soal.
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

Pending:

- Tabel/kolom khusus Reading sub-skill mastery.
- UI Reading Journey yang lebih detail.
- API summary khusus Reading.

Testing checklist:

- User submit Reading dan progress Reading naik.
- Reading journey tidak reset saat app dibuka ulang.
- Response scoring tetap kompatibel dengan frontend lama.
- Smoke test membaca summary Reading tanpa error.

### Phase 2 — Reading Sub-skill Trainer

Tujuan: memisahkan latihan Reading berdasarkan tipe kemampuan.

Deliverables:

- Trainer untuk:
  - main idea
  - detail
  - vocabulary
  - reference
  - inference
  - purpose
- Bank soal dengan `question_type`.
- Scoring per sub-skill.
- Feedback singkat per tipe soal.

Completed:

- Belum dimulai.

Pending:

- Schema question type.
- Seed data soal berdasarkan tipe.
- UI filter/trainer.
- Smoke test per question type.

Testing checklist:

- User bisa memilih tipe latihan.
- Setiap jawaban memperbarui mastery tipe soal yang benar.
- Feedback sesuai tipe soal, bukan generic.

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
- Reading-specific service layer.
- Reading-specific API endpoints.
- Guided Reading UI.
- Question Trainer UI.
- Answer Review UI.
- Reading Review analytics.
- TOEFL Simulation.
- E2E tests untuk alur Reading.

## Next Codex Prompt Recommendation

Gunakan prompt ini untuk Phase 1:

```text
You are working inside repository IAdhamK/toefl-ba.

Task: Implement Phase 1 — Reading Journey Foundation.

Use docs/READING_PROGRESS.md and docs/READING_SPEC.md as the source of truth.

Goals:
- Add Reading-specific journey summary without breaking current MVP.
- Track Reading sub-skills:
  general_meaning, main_idea, detail_information, vocabulary_context.
- Preserve existing Reading Analyzer UI and scoring behavior.
- Add backend service functions for Reading progress summary.
- Add API endpoint GET /api/reading/journey or similar.
- Add frontend Reading Journey panel if safe, or expose API first.
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
