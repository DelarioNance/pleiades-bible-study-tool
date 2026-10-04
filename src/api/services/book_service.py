from fastapi import HTTPException
from src.api.db import engine
from sqlalchemy import text


def fetch_books(is_test: bool=False):
    with engine.connect() as conn:
        rows = conn.execute(text("""
            SELECT
                b.id
                , b.common_name
                , b.canonical_order
            FROM books b
            WHERE b.is_test = :is_test
            ORDER BY 
                b.canonical_order
            ;
        """), {
            "is_test": is_test
        }).fetchall()

    return [
        {
            "id": row.id,
            "name": row.common_name,
            "order": row.canonical_order
        } for row in rows
    ]


def fetch_chapters_from_book_id(book_id):
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


def fetch_verses_from_book_id_and_chapter_number(book_id, chapter_number):
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

def get_book_info_from_book_name(book_name):
    try:
        with engine.connect() as conn:
            row = conn.execute(text("""
                SELECT
                    b.id
                    , b.common_name
                    , b.canonical_order
                FROM books b 
                WHERE b.common_name = :book_name
                ;
            """), {
                "book_name": book_name
            }).fetchone()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    if row is None:
        raise HTTPException(status_code=404, detail=f"Book with name {book_name} not found")
    
    return {
        "id": row.id,
        "name": row.common_name,
        "order": row.canonical_order
    }