from fastapi import FastAPI

from sqlalchemy import text
from src.utils.db import get_db_engine
import os

app = FastAPI()

env = os.getenv("PLEIADES_ENV", "sandbox")
engine = get_db_engine(env)


@app.get("/v1/books")
def get_books():
    with engine.connect() as conn:
        rows = conn.execute(text("""
            SELECT
                b.id
                , b.common_name AS name
                , b.canonical_order AS order
            FROM books b
            ORDER BY 
                b.canonical_order
            ;
        """)).fetchall()

    return [
        {
            "id": row.id,
            "name": row.name,
            "order": row.order
        } for row in rows
    ]