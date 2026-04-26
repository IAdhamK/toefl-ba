import time

from fastapi import APIRouter, Header, HTTPException

from backend.database import get_connection, now_iso
from backend.schemas import LoginRequest, UserCreate


router = APIRouter(prefix="/api/auth", tags=["auth"])


def public_user(row) -> dict:
    return {
        "id": row["id"],
        "name": row["name"],
        "email": row["email"],
        "targetScore": row["target_score"],
        "weakness": row["weakness"],
        "level": row["level"],
    }


@router.post("/register", status_code=201)
def register(payload: UserCreate) -> dict:
    user_id = f"user-{int(time.time() * 1000)}"
    email = payload.email or f"{payload.name.lower().replace(' ', '.')}@example.local"
    token = f"token-{user_id}"
    now = now_iso()
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO users (id, name, email, target_score, weakness, level, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, payload.name, email, payload.targetScore, payload.weakness, payload.level, now),
        )
        conn.execute("INSERT INTO sessions (token, user_id, created_at) VALUES (?, ?, ?)", (token, user_id, now))
        row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    return {"user": public_user(row), "token": token}


@router.post("/login")
def login(payload: LoginRequest) -> dict:
    now = now_iso()
    with get_connection() as conn:
        row = None
        if payload.email:
            row = conn.execute("SELECT * FROM users WHERE email = ?", (payload.email,)).fetchone()
        if row is None:
            row = conn.execute("SELECT * FROM users ORDER BY created_at ASC LIMIT 1").fetchone()
        if row is None:
            user_id = "guest-user"
            conn.execute(
                """
                INSERT OR IGNORE INTO users (id, name, email, target_score, weakness, level, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    payload.name or "Junior BA Learner",
                    "guest@example.local",
                    payload.targetScore,
                    payload.weakness,
                    "Foundation",
                    now,
                ),
            )
            row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        token = f"token-{row['id']}"
        conn.execute(
            "INSERT OR REPLACE INTO sessions (token, user_id, created_at) VALUES (?, ?, ?)",
            (token, row["id"], now),
        )
    return {"user": public_user(row), "token": token}


@router.get("/profile")
def profile(authorization: str | None = Header(default=None)) -> dict:
    token = (authorization or "").replace("Bearer ", "")
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT users.* FROM users
            JOIN sessions ON sessions.user_id = users.id
            WHERE sessions.token = ?
            """,
            (token,),
        ).fetchone()
    if not row:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"user": public_user(row)}
