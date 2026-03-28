# ------------------------------------------------------------
# Standard library
# ------------------------------------------------------------

# ------------------------------------------------------------
# Third‑party packages
# ------------------------------------------------------------
import asyncio # essentially an async version of requests
from sqlalchemy import text

# ------------------------------------------------------------
# Local modules
# ------------------------------------------------------------
from ingest_bible import initialize_bible_content
from utils import get_db_engine, query_scalar
import bible_canonical_data as canon


# Test DB Setup
engine = get_db_engine('test')
asyncio.run(initialize_bible_content(engine, log_mode=False)) # asyncio is needed to run async functions from a main function


def test_canonical_book_count():    
    with engine.connect() as conn:
        num_books = query_scalar(conn, """
            SELECT
                count(b.id) as num_books
            FROM books b
            ;
        """)
    
    assert num_books == canon.NUM_BOOKS, f"Expected 66 books, but got {num_books}." 


def test_canonical_chapter_count():    
    with engine.connect() as conn:
        num_chapters = query_scalar(conn, """
            SELECT
                count(c.id) as num_chapters
            FROM chapters c
            ;
        """)
    
    assert num_chapters == canon.NUM_CHAPTERS, f"Expected 1189 chapters, but got {num_chapters}." 


def test_canonical_verse_count():
    with engine.connect() as conn:
        num_verses = query_scalar(conn, """
            SELECT
                count(v.id) as num_verses
            FROM verses v
            ;
        """)
    
    assert num_verses == canon.NUM_VERSES, f"Expected 31102 verses, but got {num_verses}." 


def test_canonical_book_list():
    sql = text("""
            SELECT
                b.common_name 
            FROM books b
            ORDER BY
                b.canonical_order  
            ;
        """)
    
    with engine.connect() as conn:
        db_books_in_num_order_raw = conn.execute(sql).fetchall()
        db_books_in_num_order = [row[0] for row in db_books_in_num_order_raw]
    
    assert db_books_in_num_order == canon.BOOKS_IN_NUMBER_ORDER # pytest automatically handles list equality and will show a helpful diff if the assertion fails 


def test_chapter_count_per_book():
    sql = text("""
            SELECT
                b.common_name 
                , count(c.id) AS num_chapters
            FROM books b
            INNER JOIN chapters c
                ON c.book_id = b.id 
            GROUP BY 
                b.common_name
            ;
        """)
    
    with engine.connect() as conn:
        db_chapter_count_per_book = dict(conn.execute(sql).fetchall())
    
    assert db_chapter_count_per_book == canon.BOOK_TO_NUM_CHAPTERS # pytest automatically handles list equality and will show a helpful diff if the assertion fails 


def test_chapter_sequencing():
    sql = text("""
            WITH chapter_sequences_against_expected AS (
                SELECT
                    c.chapter_number AS actual_chapter_num
                    , ROW_NUMBER() OVER (
                        PARTITION BY b.id
                        ORDER BY c.chapter_number 
                    ) AS expected_chapter_num
                FROM books b
                LEFT JOIN chapters c
                    ON c.book_id = b.id 
            )
            SELECT 1 AS col_placeholder
            FROM chapter_sequences_against_expected versus
            WHERE coalesce(versus.actual_chapter_num, -1) <> expected_chapter_num
            ;
        """) # coalesce is used to handle the case where a book has no chapters
    
    with engine.connect() as conn:
        exceptions = conn.execute(sql).fetchall()
    
    assert len(exceptions) == 0, f"Found {len(exceptions)} chapters with incorrect sequencing." # pytest automatically handles list equality and will show a helpful diff if the assertion fails 


def test_verse_sequencing():
    sql = text("""
            WITH verse_sequences_against_expected AS (
                SELECT
                    v.verse_number AS actual_verse_num
                    , ROW_NUMBER() OVER (
                        PARTITION BY c.id
                        ORDER BY v.verse_number 
                    ) AS expected_verse_num
                FROM chapters c
                LEFT JOIN verses v
                    ON v.chapter_id = c.id
            )
            SELECT 1 AS col_placeholder
            FROM verse_sequences_against_expected versus
            WHERE coalesce(versus.actual_verse_num, -1) <> expected_verse_num
            ;
        """) # coalesce is used to handle the case where a chapter has no verses
    
    with engine.connect() as conn:
        exceptions = conn.execute(sql).fetchall()
    
    assert len(exceptions) == 0, f"Found {len(exceptions)} verses with incorrect sequencing." # pytest automatically handles list equality and will show a helpful diff if the assertion fails 


