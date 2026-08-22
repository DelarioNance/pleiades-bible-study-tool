from fastapi import HTTPException
from src.api.db import engine
from sqlalchemy import text


def fetch_verses_from_chapter_id(chapter_id):
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


def get_chapter_info_from_book_id_and_chapter_number(book_id, chapter_number):
    try:
        with engine.connect() as conn:
            row = conn.execute(text("""
                SELECT
                    c.id
                    , c.chapter_number
                FROM chapters c
                WHERE c.book_id = :book_id
                    AND c.chapter_number = :chapter_number
                ;
            """), {
                "book_id": book_id,
                "chapter_number": chapter_number
            }).fetchone()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if row is None:
        raise HTTPException(status_code=404, detail=f"Chapter with book ID {book_id} and chapter number {chapter_number} not found")

    return {
        "id": row.id,
        "number": row.chapter_number
    }