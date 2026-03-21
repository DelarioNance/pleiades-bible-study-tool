# ------------------------------------------------------------
# Standard library
# ------------------------------------------------------------

# ------------------------------------------------------------
# Third‑party packages
# ------------------------------------------------------------
from sqlalchemy import text # not sure why text is needed, but SQLAlchemy's documentation recommends it.
import asyncio # essentially an async version of requests

# ------------------------------------------------------------
# Local modules
# ------------------------------------------------------------
from ingest_bible import initialize_bible_content
from utils import get_db_engine
import bible_canonical_data as canon

# Test DB Setup
engine = get_db_engine('test')
asyncio.run(initialize_bible_content(engine, log_mode=False)) # asyncio is needed to run async functions from a main function

def test_canonical_book_count():
    sql = text("""
            SELECT
                count(b.id) AS num_books
            FROM books b
            ;
        """)
    
    with engine.connect() as conn:
        num_books = conn.execute(sql).scalar()
    
    assert num_books == canon.NUM_BOOKS, f"Expected 66 books, but got {num_books}." 


def test_canonical_chapter_count():
    sql = text("""
            SELECT
                count(c.id) AS num_chapters
            FROM chapters c
            ;
        """)
    
    with engine.connect() as conn:
        num_chapters = conn.execute(sql).scalar()
    
    assert num_chapters == canon.NUM_CHAPTERS, f"Expected 1189 chapters, but got {num_chapters}." 


def test_canonical_verse_count():
    sql = text("""
            SELECT
                count(v.id) AS num_verses
            FROM verses v
            ;
        """)
    
    with engine.connect() as conn:
        num_verses = conn.execute(sql).scalar()
    
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
    
    assert db_books_in_num_order == canon.BOOKS_IN_NUMBER_ORDER