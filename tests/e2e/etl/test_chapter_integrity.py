from sqlalchemy import text


def test_no_duplicate_chapter_numbers(conn_from_etl_run):
    query = text("""
        SELECT book_id, chapter_number, COUNT(*) AS cnt
        FROM chapters
        GROUP BY book_id, chapter_number
        HAVING COUNT(*) > 1;
    """)

    duplicates = conn_from_etl_run.execute(query).fetchall()

    assert duplicates == [], f"Duplicate chapter numbers found: {duplicates}"


def test_every_chapter_has_book(conn_from_etl_run):
    query = text("""
        SELECT c.id, c.book_id
        FROM chapters c
        LEFT JOIN books b ON c.book_id = b.id
        WHERE b.id IS NULL;
    """)

    orphans = conn_from_etl_run.execute(query).fetchall()

    assert orphans == [], f"Chapters referencing non‑existent books found: {orphans}"
