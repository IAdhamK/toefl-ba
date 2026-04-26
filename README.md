# TOEFL Analyst AI

TOEFL Analyst AI adalah aplikasi belajar TOEFL dengan konteks kerja Business Analyst. Fokusnya untuk pemula: membaca kalimat Inggris pelan-pelan, memahami subject dan verb, menghafal vocabulary harian, latihan scoring, dan mendapat bantuan Bahasa Indonesia.

## Fitur Saat Ini

- Frontend MVP di `frontend/` dengan dashboard, journey panel, dan UX Bahasa Indonesia.
- FastAPI backend di `backend/` dengan pola endpoint `/api/*`.
- SQLite foundation di `data/toefl_ba.sqlite3` yang dibuat otomatis saat backend berjalan.
- Migrasi data lama dari `data/app_data.json` ke SQLite.
- Reading Analyzer, Grammar Breakdown, Vocabulary Drill 25 kata/hari, Writing Evaluator, Listening scenario, Scenario BA, AI Tutor mock, Bantuan ID, Admin CMS dasar.
- Safe AI fallback: tanpa API key, aplikasi tetap menjawab memakai mock rule-based.

## Struktur Folder

```text
toefl-ba/
├── frontend/
│   ├── index.html
│   ├── app.js
│   └── styles.css
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── seed.py
│   ├── routers/
│   └── services/
├── data/
│   ├── app_data.json
│   └── toefl_ba.sqlite3
├── docs/
├── scripts/
├── README.md
├── PROJECT_PROGRESS.md
└── requirements.txt
```

Catatan: `data/app_data.json`, `data/toefl_ba.sqlite3`, dan `.venv/` adalah file runtime lokal dan tidak perlu masuk git.

## Cara Menjalankan Untuk Pemula

1. Buat virtual environment:

```bash
python3 -m venv .venv
```

2. Aktifkan environment:

```bash
source .venv/bin/activate
```

3. Install dependency:

```bash
pip install -r requirements.txt
```

4. Jalankan backend + frontend:

```bash
uvicorn backend.main:app --reload --port 8001
```

5. Buka aplikasi:

```text
http://127.0.0.1:8001
```

Perintah lama juga masih bisa dipakai:

```bash
python3 server.py
```

## Migrasi Data Lama

Jika ada data lama di `data/app_data.json`, jalankan:

```bash
python3 scripts/migrate_json_to_sqlite.py
```

Backend juga akan melakukan seed otomatis saat pertama kali berjalan.

## Smoke Test

Pastikan backend sedang berjalan, lalu jalankan:

```bash
python3 scripts/smoke_api.py
```

Output yang sehat akan berisi banyak baris `ok - ...` dan ditutup dengan:

```text
Selesai. API utama berjalan baik.
```

## Docker Opsional

Jika kamu memakai Docker:

```bash
docker compose up --build
```

Buka:

```text
http://127.0.0.1:8001
```

## Konfigurasi AI Opsional

Tanpa API key, aplikasi memakai mock AI yang aman untuk lokal. Untuk provider OpenAI/OpenRouter-compatible di masa depan, gunakan environment variable:

```bash
export LLM_PROVIDER=openai
export LLM_API_KEY=isi_api_key_di_mesin_lokal
export LLM_BASE_URL=https://api.openai.com/v1
export LLM_MODEL=gpt-4o-mini
```

Jangan menulis API key langsung di kode.

## Troubleshooting

- Jika `uvicorn` tidak ditemukan, aktifkan `.venv` lalu ulangi `pip install -r requirements.txt`.
- Jika port 8001 sudah dipakai, hentikan proses lama atau gunakan port lain.
- Jika data kosong, jalankan `python3 scripts/migrate_json_to_sqlite.py`.
- Jika frontend dibuka tanpa backend, beberapa fitur tetap fallback lokal, tetapi scoring API dan sinkronisasi tidak aktif.
