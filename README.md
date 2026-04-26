# TOEFL Analyst AI

MVP awal untuk aplikasi pembelajaran TOEFL berbasis konteks Business Analyst.

## Fitur MVP

- Auth/profile lokal dengan `localStorage`.
- Dashboard progress.
- Reading Analyzer dengan passage BA dan TOEFL-style questions.
- Grammar Breakdown Engine versi rule-based.
- Vocabulary Drill.
- AI Tutor Chat versi lokal.
- Writing Evaluator awal.
- Listening scenario awal.
- Scenario-Based BA Practice.
- Admin CMS lokal untuk menambah reading lesson dan vocabulary.
- Recent activity untuk ringkasan latihan.
- Backend REST lokal tanpa dependency eksternal.
- Sinkronisasi state, content, progress, grammar breakdown, dan AI Tutor mock via `/api/*`.
- Endpoint scoring untuk reading, vocabulary, writing, listening, scenario, dan rekomendasi AI Tutor.
- Progress analytics untuk average score, weakest skill, strongest skill, total exercises, dan activity count.
- Bantuan Bahasa Indonesia untuk menerjemahkan, menjelaskan kosakata, dan menemukan subject/verb bagi user basic.
- Daily random vocabulary drill dengan target 25 kata per hari, reminder, dan result progress drill.
- Journey panel di Reading, Grammar, Vocabulary, Writing, dan Listening untuk melihat posisi belajar dan next step.

## Menjalankan

Mode lengkap dengan backend:

```bash
python3 server.py
```

Buka:

```text
http://localhost:8001
```

Mode statis saja:

```bash
python3 -m http.server 8000
```

Smoke test API:

```bash
python3 scripts/smoke_api.py
```

## Catatan

MVP ini sengaja dibuat tanpa dependency agar langsung dapat digunakan. Data backend tersimpan di `data/app_data.json`. Tahap berikutnya dapat memecah backend ini menjadi FastAPI atau Node.js, PostgreSQL, dan integrasi LLM/TTS sesuai `SKILL.md`.
