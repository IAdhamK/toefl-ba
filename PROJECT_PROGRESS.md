# Project Progress

## Status Saat Ini

Project sudah berada pada tahap **MVP fungsional dengan frontend, backend lokal, assessment scoring, dan progress analytics**.

## Selesai

- Menyusun `SKILL.md` dari dokumen planning proyek.
- Membuat frontend MVP:
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
- Membuat backend REST lokal di `server.py`:
  - Auth register/login.
  - Lessons.
  - Vocabulary.
  - State persistence.
  - Progress summary.
  - Grammar breakdown.
  - AI Tutor chat.
  - Reading scoring.
  - Vocabulary scoring.
  - Writing evaluation.
  - Listening scoring.
  - Scenario scoring.
  - AI Tutor recommendation.
  - Progress analytics.
- Improvisasi UI/UX untuk pemula:
  - Navigasi dengan label Bahasa Indonesia.
  - Beranda dengan langkah belajar 1-2-3.
  - Tips pemula di Reading, Grammar, Vocabulary, Writing, Listening, dan Scenario.
  - Fitur Bantuan ID untuk menjelaskan kalimat Inggris dalam Bahasa Indonesia.
- Vocabulary drill harian:
  - Random 25 kata per hari.
  - Pengingat target belajar harian.
  - Result drill: terjawab, benar, salah, sisa, akurasi, dan kata yang perlu diulang.
  - Bank kosakata dasar diperluas menjadi 30 kata.
- Journey panel per modul:
  - Reading journey.
  - Grammar journey.
  - Vocabulary journey.
  - Writing journey.
  - Listening journey.
  - Setiap journey menampilkan posisi saat ini, progress score, tahap belajar, dan next action.
- Verifikasi UI di in-app browser:
  - Navigasi pemula tampil.
  - Bantuan ID dapat menerima kalimat Inggris dan menampilkan penjelasan Bahasa Indonesia.
  - Tidak ada error console browser setelah uji fitur Bantuan ID.
- Menambahkan smoke test API di `scripts/smoke_api.py`.
- Menambahkan dokumentasi menjalankan aplikasi di `README.md`.

## Sedang Berjalan

- Aplikasi berjalan di backend lokal:
  - `http://localhost:8001`
- Data runtime backend disimpan di:
  - `data/app_data.json`
- Frontend otomatis fallback ke mode lokal jika backend mati.

## Belum Dikerjakan

- Migrasi backend ke FastAPI atau Node.js.
- Database PostgreSQL.
- JWT authentication production-grade.
- Role-based access control.
- Integrasi LLM asli untuk AI Tutor.
- Integrasi LLM asli untuk Bantuan ID.
- Integrasi TTS/STT untuk AI Listening Engine.
- Admin CMS dengan edit/delete konten.
- Test end-to-end browser.
- Deployment Docker/cloud.

## Rekomendasi Step Berikutnya

1. Rapikan struktur project menjadi `frontend/` dan `backend/`.
2. Migrasikan backend lokal ke FastAPI.
3. Tambahkan database SQLite atau PostgreSQL schema awal.
4. Tambahkan endpoint CRUD lengkap untuk lesson, question, vocabulary, dan prompt.
5. Tambahkan integrasi LLM asli di balik endpoint AI.
