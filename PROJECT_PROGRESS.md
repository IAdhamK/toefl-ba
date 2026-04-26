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

- UI edit/delete Admin CMS di frontend.
- Browser end-to-end tests.
- API unit tests dengan test database terpisah.
- Mastery calculation yang lebih detail.
- Spaced repetition vocabulary yang lebih matang.
- PostgreSQL migration path.
- Real LLM integration di production.
- TTS/STT provider nyata untuk Listening Engine.
- Auth production-grade dan role-based access control.

## Rekomendasi Step Berikutnya

1. Tambahkan edit/delete di Admin CMS frontend.
2. Tambahkan E2E browser tests untuk alur utama.
3. Tambahkan API tests dengan SQLite test database.
4. Matangkan mastery calculation dan spaced repetition.
5. Hubungkan AI service ke provider asli setelah API key tersedia.
