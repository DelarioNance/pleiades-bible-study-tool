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


# Test DB Setup
engine = get_db_engine('test')

print("Creating test database")
asyncio.run(initialize_bible_content(engine, log_mode=False)) # asyncio is needed to run async functions from a main function
print("Test database created!")

def test_canonical_book_count():
    sql = text("""
            SELECT
                count(b.id) AS num_books
            FROM books b
            ;
        """)
    
    with engine.connect() as conn:
        num_books = conn.execute(sql).scalar()
    
    assert num_books == 66, f"Expected 66 books, but got {num_books}." 