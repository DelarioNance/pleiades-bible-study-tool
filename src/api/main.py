from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from sqlalchemy import text
from src.utils.db import get_db_engine
import os


app = FastAPI() # fastapi dev src/api/main.py 
app.mount(
    "/src/frontend/static",
    StaticFiles(directory="src/frontend/static"),
)

env = os.getenv("PLEIADES_ENV", "sandbox")
engine = get_db_engine(env)


@app.get("/")
def read_index():
    return FileResponse("src/frontend/html/index.html")


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
def get_chapters_from_book_id(book_id: int): # gives a 400-level error if the path parameter is not an integer
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
                    c.chapter_number
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
def get_verses_from_book_id_and_chapter_number(book_id: int, chapter_number: int):
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
                    v.verse_number
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



@app.get("/v1/chapters/{chapter_id}/verses")
def get_verses_from_chapter_id(chapter_id: int):
    try:
        with engine.connect() as conn:
            rows = conn.execute(text("""
                SELECT
                    v.id 
                    , v.verse_number 
                    , v.verse_text 
                FROM chapters c
                INNER JOIN verses v
                    ON v.chapter_id = c.id 
                WHERE c.id = :chapter_id
                ORDER BY
                    v.verse_number
                ;
            """), {
                "chapter_id": chapter_id
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
