from fastapi import HTTPException
from sqlalchemy import text

from src.api.db import engine


def fetch_all(sql, params=None):
    try:
        with engine.connect() as conn:
            rows = conn.execute(text(sql), params or {}).fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return rows


def fetch_one(sql, params=None):
    try:
        with engine.connect() as conn:
            row = conn.execute(text(sql), params or {}).fetchone()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return row
