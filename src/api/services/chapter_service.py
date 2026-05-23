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