"""Compatibility launcher for the FastAPI backend.

Recommended command:
    uvicorn backend.main:app --reload --port 8001

This file keeps the old `python3 server.py` habit working for local learners.
"""

import uvicorn


if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8001, reload=False)
