from sqlalchemy import text

from src.api.db import engine


def fetch_all(sql, params=None):
    with engine.connect() as conn:
        rows = conn.execute(text(sql), params or {}).fetchall()

    return rows


def fetch_one(sql, params=None):
    with engine.connect() as conn:
        row = conn.execute(text(sql), params or {}).fetchone()

    return row
