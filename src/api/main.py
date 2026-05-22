from fastapi import FastAPI, HTTPException

from sqlalchemy import text
from src.utils.db import get_db_engine
import os

app = FastAPI() # fastapi dev src/api/main.py 


env = os.getenv("PLEIADES_ENV", "sandbox")
engine = get_db_engine(env)


@app.get("/v1/books")
def get_books():
    with engine.connect() as conn:
        rows = conn.execute(text("""
            SELECT
                b.id
                , b.common_name
                , b.canonical_order
            FROM books b
            ORDER BY 
                b.canonical_order
            ;
        """)).fetchall()

    return [
        {
            "id": row.id,
            "name": row.common_name,
            "order": row.canonical_order
        } for row in rows
    ]

@app.get("/v1/books/{book_id}/chapters") # https://fastapi.tiangolo.com/tutorial/path-params/
def get_chapters(book_id: int): # gives a 400-level error if the path parameter is not an integer
    try:
        with engine.connect() as conn:
            rows = conn.execute(text("""
                SELECT
                    c.id 
                    , c.chapter_number 
                FROM books b 
                INNER JOIN chapters c
                    ON c.book_id = b.id 
                WHERE b.id = :book_id
                ORDER BY
                    c.id
                ;
            """), {
                "book_id": book_id
            }).fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return [
        {
            "id": row.id,
            "number": row.chapter_number
        } for row in rows
    ]


@app.get("/v1/books/{book_id}/chapters/{chapter_number}/verses")
def get_verses(book_id: int, chapter_number: int):
    try:
        with engine.connect() as conn:
            rows = conn.execute(text("""
                SELECT
                    v.id 
                    , v.verse_number 
                    , v.verse_text 
                FROM books b 
                INNER JOIN chapters c
                    ON c.book_id = b.id 
                INNER JOIN verses v
                    ON v.chapter_id = c.id 
                WHERE b.id = :book_id
                    AND c.chapter_number = :chapter_number
                ORDER BY
                    v.id
                ;
            """), {
                "book_id": book_id,
                "chapter_number": chapter_number
            }).fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return [
        {
            "id": row.id,
            "number": row.verse_number,
            "text": row.verse_text
        } for row in rows
    ]