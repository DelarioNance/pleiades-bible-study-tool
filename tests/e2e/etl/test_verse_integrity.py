from sqlalchemy import text

def test_no_duplicate_verse_numbers(conn_from_etl_run):
    query = text("""
        SELECT chapter_id, verse_number, COUNT(*) AS cnt
        FROM verses
        GROUP BY chapter_id, verse_number
        HAVING COUNT(*) > 1;
    """)

    duplicates = conn_from_etl_run.execute(query).fetchall()

    assert duplicates == [], f"Duplicate verse numbers found: {duplicates}"


def test_every_verse_has_chapter(conn_from_etl_run):
    query = text("""
        SELECT v.id, v.chapter_id
        FROM verses v
        LEFT JOIN chapters c ON v.chapter_id = c.id
        WHERE c.id IS NULL;
    """)

    orphans = conn_from_etl_run.execute(query).fetchall()

    assert orphans == [], f"Verses referencing non‑existent chapters found: {orphans}"


def test_no_missing_verse_text(conn_from_etl_run):
    query = text("""
        SELECT id, verse_text
        FROM verses
        WHERE COALESCE(TRIM(verse_text), '') = '';
    """)

    missing = conn_from_etl_run.execute(query).fetchall()

    assert missing == [], f"Verses with missing or blank text found: {missing}"
