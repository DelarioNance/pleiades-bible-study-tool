from src.api.queries.utils import fetch_all, fetch_one


def get_chapters_from_book_id(book_id):
    sql = """
        SELECT
            c.id 
            , c.chapter_number 
        FROM books b 
        INNER JOIN chapters c
            ON c.book_id = b.id 
        WHERE b.id = :book_id
        ;
    """
    params = {"book_id": book_id}
    rows = fetch_all(sql, params)

    return [{"chapter_id": row.id, "chapter_number": row.chapter_number} for row in rows]


def get_chapter_from_book_id_and_chapter_number(book_id, chapter_number):
    sql = """
        SELECT
            c.id 
            , c.chapter_number 
        FROM books b 
        INNER JOIN chapters c
            ON c.book_id = b.id 
        WHERE b.id = :book_id
            AND c.chapter_number = :chapter_number
        ;
    """
    params = {"book_id": book_id, "chapter_number": chapter_number}
    row = fetch_one(sql, params)

    return {"chapter_id": row.id, "chapter_number": row.chapter_number}
