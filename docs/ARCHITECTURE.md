# Architecture

TOEFL Analyst AI sekarang memakai struktur bertahap:

- `frontend/`: aplikasi browser tanpa build step.
- `backend/`: FastAPI backend untuk REST API.
- `backend/routers/`: pemisahan endpoint per domain.
- `backend/services/`: logika scoring, grammar, progress, AI mock, dan listening.
- `data/`: file lokal runtime, termasuk JSON lama dan SQLite baru.
- `scripts/`: alat migrasi dan smoke test.

## Alur Request

1. User membuka `http://127.0.0.1:8001`.
2. FastAPI menyajikan file dari `frontend/`.
3. `frontend/app.js` memanggil endpoint `/api/*`.
4. Router FastAPI memanggil repository/service.
5. SQLite menyimpan content, progress, attempt, state, prompt, dan session.

## Prinsip Migrasi

- Endpoint lama tetap dipertahankan agar UI MVP tidak rusak.
- SQLite menjadi database pertama, dengan struktur yang mudah dipindahkan ke PostgreSQL.
- AI asli belum wajib. `backend/services/ai_service.py` memakai mock fallback jika tidak ada API key.
- Listening engine disiapkan untuk TTS/STT, tetapi saat ini masih memakai transcript dan mock audio metadata.

## Integrated User Learning Journey

Journey layer menambahkan memori belajar terpadu per user. Setiap attempt dari reading, grammar, vocabulary, writing, listening, dan scenario masuk ke `learning_attempts`, lalu service memperbarui `skill_journeys`, `learning_journeys`, `skill_mastery`, `vocabulary_memory`, dan `ai_recommendations`.

Frontend membaca ringkasan dari `/api/journey/summary` dan tetap memakai fallback lokal jika backend mati.
