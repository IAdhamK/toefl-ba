from __future__ import annotations

import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from backend.database import init_db
from backend.services.journey_service import backfill_user_journeys


if __name__ == "__main__":
    init_db()
    result = backfill_user_journeys()
    print("Backfill journey selesai.")
    print(f"- Users: {result['users']}")
    print(f"- Skill journeys: {result['skills']}")
