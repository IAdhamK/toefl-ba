from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
DB_PATH = DATA_DIR / "toefl_ba.sqlite3"
JSON_DATA_PATH = DATA_DIR / "app_data.json"


def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


def get_connection() -> sqlite3.Connection:
    DATA_DIR.mkdir(exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def encode_json(value: Any) -> str:
    return json.dumps(value if value is not None else {}, ensure_ascii=False)


def decode_json(value: str | None, fallback: Any = None) -> Any:
    if value in (None, ""):
        return {} if fallback is None else fallback
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return {} if fallback is None else fallback


def row_to_dict(row: sqlite3.Row | None) -> dict[str, Any] | None:
    return dict(row) if row else None


def init_db() -> None:
    with get_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                target_score INTEGER DEFAULT 500,
                weakness TEXT DEFAULT 'Grammar',
                level TEXT DEFAULT 'Foundation',
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS sessions (
                token TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS lessons (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                level TEXT DEFAULT 'Foundation',
                context TEXT DEFAULT '',
                passage TEXT DEFAULT '',
                vocabulary_json TEXT DEFAULT '[]',
                grammar TEXT DEFAULT '',
                questions_json TEXT DEFAULT '[]',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS questions (
                id TEXT PRIMARY KEY,
                lesson_id TEXT,
                text TEXT NOT NULL,
                options_json TEXT DEFAULT '[]',
                answer INTEGER DEFAULT 0,
                explanation TEXT DEFAULT '',
                skill TEXT DEFAULT 'Reading',
                created_at TEXT NOT NULL,
                FOREIGN KEY (lesson_id) REFERENCES lessons(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS vocabulary (
                id TEXT PRIMARY KEY,
                word TEXT NOT NULL,
                part TEXT DEFAULT '',
                meaning_id TEXT DEFAULT '',
                meaning_en TEXT DEFAULT '',
                example TEXT DEFAULT '',
                answer TEXT DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT DEFAULT 'guest-user',
                skill TEXT NOT NULL,
                score INTEGER NOT NULL,
                metadata_json TEXT DEFAULT '{}',
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS attempts (
                id TEXT PRIMARY KEY,
                user_id TEXT DEFAULT 'guest-user',
                module TEXT NOT NULL,
                score INTEGER NOT NULL,
                payload_json TEXT DEFAULT '{}',
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS ai_sessions (
                id TEXT PRIMARY KEY,
                user_id TEXT DEFAULT 'guest-user',
                provider TEXT DEFAULT 'mock',
                message TEXT NOT NULL,
                response TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS prompts (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS app_state (
                key TEXT PRIMARY KEY,
                value_json TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS admin_content (
                id TEXT PRIMARY KEY,
                content_type TEXT NOT NULL,
                title TEXT NOT NULL,
                payload_json TEXT DEFAULT '{}',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """
        )


def table_count(table: str) -> int:
    with get_connection() as conn:
        row = conn.execute(f"SELECT COUNT(*) AS total FROM {table}").fetchone()
        return int(row["total"])


def load_json_data() -> dict[str, Any]:
    if not JSON_DATA_PATH.exists():
        return {}
    with JSON_DATA_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)
