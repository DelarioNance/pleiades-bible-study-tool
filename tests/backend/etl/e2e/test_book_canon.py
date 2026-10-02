from sqlalchemy import text
from tests.backend.utils.constants import (
    NUM_BOOKS,
    BOOKS_IN_NUMBER_ORDER,
    NUM_CHAPTERS_PER_BOOK,
)

def test_correct_number_of_books(conn_from_etl_run):
    query = text("""
        SELECT COUNT(id) 
        FROM books
        WHERE is_test = FALSE;
    """)
    (count,) = conn_from_etl_run.execute(query).one() # one is used instead of scalar to error if the query does not return exactly 1 row

    assert count == NUM_BOOKS, f"Expected {NUM_BOOKS} books, found {count}"


def test_books_in_correct_order(conn_from_etl_run):
    query = text("""
        SELECT common_name
        FROM books
        WHERE is_test = FALSE
        ORDER BY id;
    """)

    db_books = [row[0] for row in conn_from_etl_run.execute(query).fetchall()]

    assert db_books == BOOKS_IN_NUMBER_ORDER, (
        "Books are not in canonical order.\n"
        f"Expected: {BOOKS_IN_NUMBER_ORDER}\n"
        f"Found:    {db_books}"
    )


def test_correct_chapter_count_per_book(conn_from_etl_run):
    query = text("""
        SELECT b.common_name, COUNT(c.id) AS chapter_count
        FROM books b
        LEFT JOIN chapters c ON c.book_id = b.id and c.is_test = FALSE
        WHERE b.is_test = FALSE
        GROUP BY b.common_name
    """)

    results = conn_from_etl_run.execute(query).fetchall()

    for book_name, chapter_count in results:
        expected = NUM_CHAPTERS_PER_BOOK[book_name]
        assert chapter_count == expected, (
            f"Book '{book_name}' should have {expected} chapters, "
            f"but ETL produced {chapter_count}"
        )


def test_chapters_are_contiguous_and_start_at_one(conn_from_etl_run):
    query = text("""
        WITH numbered AS (
            SELECT
                b.common_name,
                c.chapter_number,
                ROW_NUMBER() OVER (
                    PARTITION BY b.id
                    ORDER BY c.chapter_number
                ) AS rn
            FROM books b
            JOIN chapters c ON c.book_id = b.id and c.is_test = FALSE
            WHERE b.is_test = FALSE
        )
        SELECT common_name, chapter_number, rn
        FROM numbered
        WHERE chapter_number != rn;
    """)

    mismatches = conn_from_etl_run.execute(query).fetchall()

    assert mismatches == [], (
        "Found books with non‑contiguous or non‑starting‑at‑1 chapter numbers: "
        f"{mismatches}"
    )


def test_no_book_has_surrounding_whitespace(conn_from_etl_run):
    query = text("""
        SELECT id, common_name
        FROM books
        WHERE common_name != TRIM(common_name);
    """)

    bad_names = conn_from_etl_run.execute(query).fetchall()

    assert bad_names == [], (
        f"Books with leading/trailing whitespace found: {bad_names}"
    )
