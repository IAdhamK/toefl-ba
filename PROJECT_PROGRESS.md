# Project Progress

## Status Saat Ini

Project sudah naik dari MVP lokal satu file menjadi **MVP terstruktur dengan FastAPI, SQLite foundation, service layer, router API, migrasi data, dan dokumentasi pemula**.

## Selesai Sebelumnya

- Frontend MVP:
  - Auth/profile lokal.
  - Dashboard progress.
  - Reading Analyzer.
  - Grammar Breakdown.
  - Vocabulary Drill.
  - AI Tutor lokal.
  - Writing Evaluator.
  - Listening scenario.
  - Scenario-Based BA Practice.
  - Admin CMS lokal.
- UI/UX Bahasa Indonesia untuk pemula.
- Bantuan ID untuk menjelaskan kalimat Inggris.
- Daily vocabulary drill 25 kata/hari.
- Journey panel di Reading, Grammar, Vocabulary, Writing, dan Listening.
- Smoke test API awal.

## Selesai Pada Fase Ini

- Struktur project dirapikan:
  - `frontend/`
  - `backend/`
  - `backend/routers/`
  - `backend/services/`
  - `docs/`
  - `scripts/`
  - `data/`
- Frontend dipindah ke:
  - `frontend/index.html`
  - `frontend/app.js`
  - `frontend/styles.css`
- Backend FastAPI baru dibuat di:
  - `backend/main.py`
- SQLite foundation dibuat di:
  - `backend/database.py`
  - `backend/models.py`
  - `backend/schemas.py`
  - `backend/seed.py`
- Tabel awal disiapkan:
  - `users`
  - `sessions`
  - `lessons`
  - `questions`
  - `vocabulary`
  - `progress`
  - `attempts`
  - `ai_sessions`
  - `prompts`
  - `app_state`
  - `admin_content`
- Migrasi data lama dibuat:
  - `scripts/migrate_json_to_sqlite.py`
- Router API dibuat:
  - `auth`
  - `lessons`
  - `vocabulary`
  - `progress`
  - `scoring`
  - `ai_tutor`
  - `admin`
- Endpoint lama tetap dipertahankan agar frontend tidak rusak:
  - `/api/reading/submit-answer`
  - `/api/grammar/breakdown`
  - `/api/ai-tutor/chat`
  - `/api/ai-tutor/recommendation`
  - `/api/help/indonesian`
  - `/api/writing/evaluate`
  - `/api/listening/submit-answer`
  - `/api/scenario/submit-answer`
- AI service layer dibuat:
  - Mock provider default.
  - OpenAI/OpenRouter-compatible provider disiapkan lewat environment variable.
  - Tidak ada API key yang di-hardcode.
- Listening service disiapkan:
  - Mock audio metadata.
  - Transcript.
  - Listening question.
  - Scoring.
  - Catatan integrasi TTS/STT masa depan.
- Smoke test diperbarui untuk FastAPI.
- Dokumentasi dibuat:
  - `README.md`
  - `docs/ARCHITECTURE.md`
  - `docs/API_SPEC.md`
  - `docs/DEV_PROGRESS.md`
  - `docs/ROADMAP.md`
- Docker support dasar dibuat:
  - `Dockerfile`
  - `docker-compose.yml`
  - `.dockerignore`
- Integrated User Learning Journey:
  - tabel `learning_journeys`, `skill_journeys`, `learning_attempts`, `skill_mastery`, `vocabulary_memory`, `ai_recommendations`
  - service `backend/services/journey_service.py`
  - router `backend/routers/journey.py`
  - UI `Perjalanan Belajar Saya`
  - daily plan, continue learning, review list, mentor summary
  - scoring endpoint sekarang mengirim `journey_update`
- Adaptive mentor:
  - endpoint latihan adaptif
  - endpoint mentor summary
  - endpoint complete adaptive practice
  - UI latihan adaptif di halaman Perjalanan
  - masih rule-based, belum LLM asli
- Bantuan ID kontekstual:
  - tombol kecil muncul langsung di konten Reading, Grammar, Vocabulary, AI Tutor, Writing, Listening, dan Scenario BA
  - hasil penjelasan sekarang muncul sebagai panel melayang agar tidak mengubah layout modul
  - panel Bantuan ID dapat digeser oleh user dan ditutup kapan saja
  - kosakata penting sekarang menampilkan arti singkat satu kata, arti umum, dan arti dalam contoh kalimat tertentu
  - penjelasan pertanyaan/opsi jawaban dibuat lebih langsung ke arti teks yang diklik, tidak lagi memakai fallback generik yang membingungkan
  - backend memakai dispatcher per `context_type`, sehingga reading question, reading option, vocabulary, grammar, writing, listening, dan scenario mendapat format penjelasan berbeda
  - frontend mengirim `extra_context` untuk Reading, Vocabulary, Listening, dan Scenario agar helper bisa membandingkan opsi dengan passage/case/transcript
  - endpoint baru `POST /api/ai/contextual-help`
  - endpoint lama `POST /api/help/indonesian` tetap dipertahankan
  - respons mock fallback berisi arti sederhana, struktur kalimat, subject, verb, object/complement, kosakata penting, konteks, dan tips
  - penggunaan Bantuan ID dicatat sebagai aktivitas lokal belajar pendukung tanpa menurunkan skor journey
- Reading documentation foundation:
  - `docs/READING_PROGRESS.md` untuk melacak vision, fase implementasi, status, deliverables, testing checklist, dan prompt Codex berikutnya
  - `docs/READING_SPEC.md` untuk mendefinisikan target Reading Journey, Guided Reading, Question Trainer, Answer Review, Reading Review, dan TOEFL Simulation
- Reading Journey Foundation:
  - service `backend/services/reading_service.py`
  - router `backend/routers/reading.py`
  - endpoint `GET /api/reading/journey`
  - endpoint `GET /api/reading/levels`
  - endpoint `GET /api/reading/recommendation`
  - endpoint `POST /api/reading/attempt`
  - halaman Reading menampilkan Reading level, score, completed passages, strongest/weakest sub-skill, dan next recommended action
  - sub-skill Phase 1: `general_meaning`, `main_idea`, `detail_information`, `vocabulary_context`
- Reading Sub-skill Trainer:
  - service Reading sekarang mendukung 10 sub-skill Reading
  - endpoint `GET /api/reading/subskills`
  - endpoint `GET /api/reading/trainer/{sub_skill}`
  - `POST /api/reading/attempt` bisa menerima `sub_skill` dan memperbarui mastery yang tepat
  - trainer awal tersedia untuk `main_idea`, `detail_information`, `vocabulary_context`, `inference`, dan `sentence_simplification`
  - halaman Reading menampilkan progress per sub-skill dan selector trainer
  - Bantuan ID tetap tersedia di passage, question, dan option trainer
- Guided Reading Mode:
  - endpoint `POST /api/reading/guided-steps`
  - endpoint `POST /api/reading/passage-map`
  - halaman Reading memiliki mode step-by-step untuk memahami judul, kalimat pertama, subject/verb, vocabulary, paragraph map, main idea, dan kesiapan menjawab soal
  - passage map menampilkan simple meaning, key vocabulary, main point, possible reading skill, dan beginner tip
  - completion Guided Reading dicatat sebagai aktivitas pendukung lokal tanpa menurunkan skor
- Reading Answer Review:
  - endpoint `POST /api/reading/review-answer`
  - `POST /api/reading/attempt` mengembalikan `answer_review`, `evidence_sentence`, `distractor_analysis`, dan `next_recommendation` ketika payload berisi jawaban
  - submit Reading normal mengembalikan review untuk setiap soal yang dijawab
  - UI menampilkan jawaban user, jawaban benar, bukti passage, alasan benar/salah, analisis opsi A/B/C/D, sub-skill terkait, dan rekomendasi latihan berikutnya
  - Bantuan ID tetap tersedia pada evidence sentence dan setiap opsi review
- Reading Review:
  - endpoint `GET /api/reading/review`
  - endpoint `GET /api/reading/mistake-patterns`
  - endpoint `GET /api/reading/review-queue`
  - backend menganalisis weak sub-skills, repeated wrong question types, low score passages, vocabulary yang sering salah, dan indikasi penggunaan Bantuan ID jika tercatat
  - UI menampilkan weakness report, mistake pattern, review queue, recommended practice, dan mentor message
  - tombol "Latihan Ulang Skill Lemah" mengarahkan user ke Reading Trainer sub-skill yang direkomendasikan
- TOEFL Reading Simulation:
  - endpoint `POST /api/reading/simulation/start`
  - endpoint `POST /api/reading/simulation/submit`
  - endpoint `GET /api/reading/simulation/result/{session_id}`
  - endpoint `GET /api/reading/simulation/history`
  - mode short, medium, dan full practice
  - UI Reading menampilkan timer, warning Bantuan ID dibatasi, soal simulasi, submit, final report, sub-skill breakdown, dan history
  - submit simulasi menyimpan progress ke Reading Journey melalui `learning_attempts`

## Verifikasi

- `python3 -m py_compile ...` berhasil.
- `node --check frontend/app.js` berhasil.
- `python3 scripts/migrate_json_to_sqlite.py` berhasil:
  - 2 lessons.
  - 30 vocabulary items.
  - 2 users.
  - state frontend termigrasi.
- `.venv/bin/python scripts/smoke_api.py` berhasil terhadap FastAPI di port 8001.
- Smoke test diperluas untuk journey summary, skill journeys, attempt, continue learning, daily plan, dan review list.
- Smoke test diperluas lagi untuk adaptive practice, mentor summary, dan complete adaptive practice.
- Smoke test diperluas untuk Bantuan ID kontekstual di Reading, Grammar, Vocabulary, Listening, Scenario, reading main idea question, reading correct/wrong/contradictory option, dan scenario problem statement.
- Dokumentasi Reading foundation dibuat tanpa mengubah behavior frontend/backend.
- Smoke test diperluas untuk Reading Journey, Reading levels, Reading recommendation, dan save Reading attempt.
- Smoke test diperluas untuk Reading subskills, Reading trainer main idea, attempt main idea, dan attempt vocabulary context.
- Smoke test diperluas untuk Guided Reading steps dan passage map.
- Smoke test diperluas untuk Reading answer review dan distractor analysis.
- Smoke test diperluas untuk Reading review, mistake patterns, dan review queue.
- Smoke test diperluas untuk TOEFL Reading Simulation start, submit, dan history.

## UI/UX Refresh - 29 April 2026

- Global layout diperbarui agar aplikasi terasa seperti learning platform modern:
  - sidebar diberi grouping menu: Home, Latihan TOEFL, Mentor & Admin.
  - active navigation dibuat lebih jelas.
  - responsive sidebar pada tablet/mobile dibuat horizontal-scroll agar tidak memakan layar terlalu panjang.
  - focus state untuk button/input/select/textarea ditambahkan.
- Design system kecil ditambahkan di `frontend/styles.css`:
  - `page-header`, `module-surface`, `module-grid`, `module-card`, `empty-state`, `quick-actions`, `progress-card`, `analytics-card`.
  - button global dibuat lebih aman untuk teks panjang dan mobile tap target.
  - empty/success/warning/error state dibuat lebih konsisten.
- Dashboard diperbaiki:
  - hero lebih ringkas dengan next action yang jelas.
  - progress skill dibuat dalam kartu visual.
  - modul utama dan recent activity dibuat lebih mudah dipindai.
- Reading UI tetap mempertahankan Journey Lab, Reading Lab, Guided Reading, Trainer, Practice, dan TOEFL Simulation; mode belajar dan mode testing sudah dibedakan secara visual.
- Grid koleksi di UI dibuat lebih adaptif dengan `auto-fit`, sehingga saat card/menu ditambah, diedit, atau dihapus, layout tidak meninggalkan slot kosong atau komposisi yang kaku.
- Bantuan ID, Grammar, Vocabulary, AI Tutor, Writing, Listening, Scenario, dan Admin CMS diperbarui agar memakai struktur halaman yang lebih konsisten:
  - header halaman, microcopy, form/card yang lebih jelas, empty state, dan feedback area.
  - AI Tutor sekarang punya quick prompt buttons.
  - Writing feedback dipisahkan menjadi score, grammar issue, revised sentence, dan next practice.
  - Listening punya placeholder audio mock dan urutan transcript -> question -> feedback.
  - Scenario dibuat lebih seperti case study dengan konteks dan pertanyaan terpisah.
  - Admin CMS menjelaskan bahwa edit/delete masih roadmap, bukan tombol palsu.

## Cara Menjalankan Saat Ini

```bash
source .venv/bin/activate
uvicorn backend.main:app --reload --port 8001
```

Buka:

```text
http://127.0.0.1:8001
```

Smoke test:

```bash
python3 scripts/smoke_api.py
```

## Belum Dikerjakan

- Bantuan ID untuk kalimat yang dipilih manual di dalam textarea masih sederhana; saat ini tombol membaca contoh/prompt yang terlihat.
- Integrasi penggunaan Bantuan ID ke tabel journey perlu desain khusus agar tidak menaikkan atau menurunkan skor latihan.
- UI edit/delete Admin CMS di frontend.
- Browser end-to-end tests.
- API unit tests dengan test database terpisah.
- Mastery calculation yang lebih detail.
- Spaced repetition vocabulary yang lebih matang.
- PostgreSQL migration path.
- Real LLM integration di production.
- TTS/STT provider nyata untuk Listening Engine.
- Auth production-grade dan role-based access control.
- Bank soal Reading yang lebih besar dan test coverage browser untuk semua mode Reading.

## Rekomendasi Step Berikutnya

1. Tambahkan bank soal Reading yang lebih besar dan simpan di database.
2. Tambahkan edit/delete di Admin CMS frontend.
3. Tambahkan E2E browser tests untuk alur utama.
4. Tambahkan API tests dengan SQLite test database.
5. Matangkan mastery calculation dan spaced repetition.
