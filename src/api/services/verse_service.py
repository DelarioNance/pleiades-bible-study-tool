from fastapi import HTTPException
from src.api.db import engine
from sqlalchemy import text


def get_verse_info_from_chapter_id_and_verse_number(chapter_id, verse_number):
    try:
        with engine.connect() as conn:
            row = conn.execute(text("""
                SELECT
                    v.id 
                    , v.verse_number 
                    , v.verse_text
                FROM chapters c 
                INNER JOIN verses v
                    ON v.chapter_id = c.id 
                WHERE c.id = :chapter_id
                    AND v.verse_number = :verse_number
                ;
            """), {
                "chapter_id": chapter_id,
                "verse_number": verse_number
            }).fetchone()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    if row is None:
        raise HTTPException(status_code=404, detail="Verse not found")
    
    return {
        "id": row.id,
        "number": row.verse_number,
        "text": row.verse_text
    }