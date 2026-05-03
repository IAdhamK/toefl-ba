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
- Guided Reading Mode Phase 3:
  - endpoint `POST /api/reading/guided-steps`
  - endpoint `POST /api/reading/passage-map`
  - UI Guided Reading di halaman Reading
  - step-by-step cards untuk judul, kalimat pertama, subject/verb, vocabulary, paragraph map, main idea, dan siap menjawab soal
- Answer Review Phase 4:
  - endpoint `POST /api/reading/review-answer`
  - response `POST /api/reading/attempt` menyertakan `answer_review`, `evidence_sentence`, `distractor_analysis`, dan `next_recommendation`
  - submit Reading normal menampilkan Answer Review panel setelah skor
  - review menjelaskan jawaban user, jawaban benar, evidence sentence, alasan benar/salah, analisis opsi, sub-skill terkait, dan rekomendasi latihan
- Reading Review Phase 5:
  - endpoint `GET /api/reading/review`
  - endpoint `GET /api/reading/mistake-patterns`
  - endpoint `GET /api/reading/review-queue`
  - UI Reading Review menampilkan weakness report, mistake pattern, review queue, recommended practice, dan mentor message
  - tombol "Latihan Ulang Skill Lemah" mengarahkan user ke trainer sub-skill yang direkomendasikan
- TOEFL Reading Simulation Phase 6:
  - endpoint `POST /api/reading/simulation/start`
  - endpoint `POST /api/reading/simulation/submit`
  - endpoint `GET /api/reading/simulation/result/{session_id}`
  - endpoint `GET /api/reading/simulation/history`
  - mode `short`, `medium`, dan `full`
  - UI simulasi dengan timer, warning Bantuan ID dibatasi, submit, final report, sub-skill breakdown, dan history

Yang belum tersedia:

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
- Service Reading menghasilkan guided steps untuk passage yang dipilih.
- Passage map menghasilkan simple meaning, key vocabulary, main point, possible reading skill, dan beginner tip per paragraf.
- Endpoint `POST /api/reading/guided-steps` tersedia.
- Endpoint `POST /api/reading/passage-map` tersedia.
- UI Reading memiliki Guided Reading Mode dengan tombol "Mulai Guided Reading" dan "Lanjut ke Langkah Berikutnya".
- Guided Reading mencatat aktivitas pendukung lokal saat selesai tanpa menurunkan skor latihan.
- Bantuan ID tetap tersedia pada teks guided step dan paragraph map.
- Smoke test mencakup guided steps dan passage map.

Pending:

- Guided Reading dengan multi-paragraph passage yang lebih panjang.
- Integrasi LLM opsional untuk penjelasan passage yang lebih natural.
- Penyimpanan completion guided reading di backend journey tanpa memengaruhi average score.

Testing checklist:

- Passage dapat dibaca dalam langkah kecil. Done.
- User bisa melihat arti kalimat dan vocabulary context. Done.
- Guided mode tidak mengganggu mode quiz. Done.

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
- Service Reading menghasilkan answer review terstruktur.
- Endpoint `POST /api/reading/review-answer` tersedia.
- `POST /api/reading/attempt` mengembalikan `answer_review`, `evidence_sentence`, `distractor_analysis`, dan `next_recommendation` jika payload berisi jawaban.
- Submit Reading normal mengembalikan `answer_reviews` untuk semua soal yang dijawab.
- UI menampilkan panel Answer Review setelah submit Reading.
- Bantuan ID tetap tersedia untuk evidence sentence dan setiap opsi di review.
- Smoke test mencakup review-answer dan answer review di Reading attempt.

Pending:

- Evidence sentence masih rule-based, belum berasal dari bank soal penuh.
- Distractor analysis masih rule-based untuk pola opsi umum dan belum disimpan per soal.
- Belum ada review history khusus Reading.

Testing checklist:

- Setiap soal punya explanation yang spesifik. Done untuk soal MVP.
- Jawaban salah menampilkan alasan dan evidence. Done.
- Distractor tidak dijelaskan secara generic. Done untuk pola opsi MVP.

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
- Service Reading menganalisis `learning_attempts` dan `skill_mastery` untuk mencari weak sub-skills, low score passages, repeated wrong question types, vocabulary yang sering salah, dan indikasi penggunaan Bantuan ID.
- Endpoint `GET /api/reading/review` tersedia.
- Endpoint `GET /api/reading/mistake-patterns` tersedia.
- Endpoint `GET /api/reading/review-queue` tersedia.
- UI Reading menampilkan panel Reading Review dekat Journey Summary.
- Tombol "Latihan Ulang Skill Lemah" mengarahkan user ke Reading Trainer sub-skill yang direkomendasikan.
- Smoke test mencakup Reading Review, mistake patterns, dan review queue.

Pending:

- Review history khusus Reading belum punya tabel sendiri.
- Mistake classification masih memakai rule-based analysis dari mastery dan attempts.
- Deteksi overuse Bantuan ID baru aktif jika event tersebut tersimpan di backend.

Testing checklist:

- User melihat kelemahan Reading paling dominan. Done.
- Recommendation berubah setelah beberapa attempt. Done berdasarkan mastery/attempt.
- Review list tidak kosong jika ada kesalahan. Done.

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

- Service Reading menghasilkan simulation session untuk mode short, medium, dan full.
- Submit simulation menghitung total score, accuracy, time spent, sub-skill breakdown, strongest/weakest sub-skill, recommended next practice, dan answer review summary.
- Simulation submit menyimpan attempt dengan `activity_type = reading_simulation`, sehingga progress masuk Reading Journey.
- Endpoint `POST /api/reading/simulation/start` tersedia.
- Endpoint `POST /api/reading/simulation/submit` tersedia.
- Endpoint `GET /api/reading/simulation/result/{session_id}` tersedia.
- Endpoint `GET /api/reading/simulation/history` tersedia.
- UI Reading menampilkan TOEFL Simulation Mode sebagai mode tambahan.
- Timer berjalan di frontend dan tidak menghapus mode Reading lain.
- Smoke test mencakup start, submit, dan history simulation.

Pending:

- Full practice masih memakai bank soal internal kecil, belum bank soal TOEFL besar.
- Timer belum auto-submit saat waktu habis.
- Result history masih disimpan lewat `learning_attempts`, belum tabel `reading_simulations` khusus.

Testing checklist:

- Timer berjalan dan tidak reset saat menjawab soal. Done.
- User bisa submit simulation set. Done.
- Final report menampilkan score dan sub-skill. Done.

### Reading Subfeature Progress UI

Status: Completed

Completed:

- Added `backend/services/reading_progress_service.py` to calculate progress per Reading subfeature.
- Added Reading progress endpoints:
  - `GET /api/reading/progress`
  - `GET /api/reading/progress/summary`
  - `GET /api/reading/progress/modules`
  - `GET /api/reading/progress/path`
  - `GET /api/reading/progress/recommended-section`
  - `GET /api/reading/progress/finish-status`
- Reading subfeatures now have visible status:
  - `Belum mulai`
  - `Sedang berjalan`
  - `Perlu diulang`
  - `Selesai`
  - `Direkomendasikan`
- Reading page now shows a progress summary, status board, recommended next step, and finish target.
- Reading mode tabs now show status and progress percentage.
- Reading roadmap/action cards now show progress, completed items, last score, and clear action labels.
- Each Reading subfeature panel now shows its own progress banner.
- Guided Reading completion now saves a support attempt with `activity_type = guided_reading`, so guided progress can move.

Known limitations:

- Progress is calculated from existing `learning_attempts` and `skill_mastery`, not from a dedicated Reading module progress table.
- Some older local attempts may not include enough metadata to map perfectly to subfeatures.
- Full finish target is still simple: Full Reading Simulation minimal 75%.

### Guided Reading Progress Target Fix

Status: Completed

Completed:

- Guided Reading progress now follows the number of active Reading passages available in the app, with a maximum target of 3 short passages.
- If only 2 active passages exist, Guided Reading is considered complete at `2/2`.
- If 3 or more passages exist, the target remains `3/3`.
- The next action text now tells the user to finish available active passages instead of always saying minimal 3 passages.

Problem solved:

- Users no longer get stuck at `2/3 selesai` when the app currently only provides 2 active Reading passages.

### Reading Review Completion Clarity

Status: Completed

Completed:

- Reading Review progress now uses active Review Queue items instead of showing a misleading `1/1 selesai` while progress is still below 100%.
- The Review banner now shows how many review items are completed and labels the score as weak-skill mastery.
- The Reading Review panel now explains how to reach 100%:
  - click `Latihan Ulang Skill Lemah`,
  - practice the recommended trainer skill,
  - raise the priority skill mastery to at least 70%,
  - return to Review until the queue is resolved.
- Review Queue items now include a completion rule so users know what counts as finished.

Problem solved:

- Users can now see that Review is completed by resolving weak-skill review items, not merely by opening the Review page.

### Reading Review Mode Removed From Main UI

Status: Completed

Completed:

- The standalone `Reading Review` mode is no longer shown in the Reading Lab navigation, roadmap cards, or progress module list.
- Existing review-related backend endpoints remain available for compatibility and for answer explanation data.
- If an older saved frontend state still points to `review`, the app now redirects the user to `Reading Trainer`.
- Answer Review after submitting Reading questions remains available because it teaches why answers are correct or wrong.

Problem solved:

- Users no longer see a separate Review subfeature that feels unclear or hard to finish.

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
