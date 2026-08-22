from sqlalchemy import text
from tests.backend.utils.constants import (
    NUM_CHAPTERS,
    NUM_VERSES_PER_ASCENDING_CHAPTER,
)


def test_correct_number_of_chapters(conn_from_etl_run):
    query = text("SELECT COUNT(id) FROM chapters;")
    (count,) = conn_from_etl_run.execute(query).one()

    assert count == NUM_CHAPTERS, (
        f"Expected {NUM_CHAPTERS} total chapters, but ETL produced {count}"
    )


def test_correct_number_of_verses_per_chapter(conn_from_etl_run):
    query = text("""
        SELECT b.common_name, c.chapter_number, COUNT(v.id) AS verse_count
        FROM books b
        JOIN chapters c ON c.book_id = b.id
        JOIN verses v ON v.chapter_id = c.id
        GROUP BY b.common_name, c.chapter_number
        ;
    """)

    rows = conn_from_etl_run.execute(query).fetchall()

    for book_name, chapter_number, verse_count in rows:
        expected = NUM_VERSES_PER_ASCENDING_CHAPTER[book_name][chapter_number - 1]
        assert verse_count == expected, (
            f"{book_name} chapter {chapter_number} should have {expected} verses, "
            f"but ETL produced {verse_count}"
        )


def test_verses_are_contiguous_and_start_at_one(conn_from_etl_run):
    query = text("""
        WITH numbered AS (
            SELECT
                b.common_name,
                c.chapter_number,
                v.verse_number,
                ROW_NUMBER() OVER (
                    PARTITION BY b.id, c.chapter_number
                    ORDER BY v.verse_number
                ) AS rn
            FROM books b
            JOIN chapters c ON c.book_id = b.id
            JOIN verses v ON v.chapter_id = c.id
        )
        SELECT common_name, chapter_number, verse_number, rn
        FROM numbered
        WHERE verse_number != rn;
    """)

    mismatches = conn_from_etl_run.execute(query).fetchall()

    assert mismatches == [], (
        "Found chapters with non‑contiguous or non‑starting‑at‑1 verse numbers: "
        f"{mismatches}"
    )
