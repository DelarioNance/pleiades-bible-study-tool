from api.queries.utils import fetch_all, fetch_one


def get_verses_from_chapter_id(chapter_id):
    sql = """
        SELECT
            v.id 
            , v.verse_number 
            , v.verse_text 
        FROM chapters c
        INNER JOIN verses v
            ON v.chapter_id = c.id 
        WHERE c.id = :chapter_id
        ;
    """
    params = {"chapter_id": chapter_id}
    rows = fetch_all(sql, params)

    return [
        {"id": row.id, "number": row.verse_number, "text": row.verse_text}
        for row in rows
    ]


def get_verses_from_book_id_and_chapter_number(book_id, chapter_number):
    sql = """
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
        ;
    """
    params = {"book_id": book_id, "chapter_number": chapter_number}
    rows = fetch_all(sql, params)

    return [
        {"id": row.id, "number": row.verse_number, "text": row.verse_text}
        for row in rows
    ]


def get_verse_from_chapter_id_and_verse_number(chapter_id, verse_number):
    sql = """
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
    """
    params = {"chapter_id": chapter_id, "verse_number": verse_number}
    row = fetch_one(sql, params)

    return {"id": row.id, "number": row.verse_number, "text": row.verse_text}


def get_verses_from_verse_text(verse_text: str):
    sql = """
        SELECT
            v.id
        FROM verses v
        WHERE v.verse_text ILIKE :verse_text
        ;
    """
    params = {"verse_text": verse_text}
    rows = fetch_all(sql, params)

    return [{"id": row.id} for row in rows]
