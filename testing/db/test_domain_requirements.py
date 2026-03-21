# ------------------------------------------------------------
# Standard library
# ------------------------------------------------------------

# ------------------------------------------------------------
# Third‑party packages
# ------------------------------------------------------------
from sqlalchemy import create_engine, text # not sure why text is needed, but SQLAlchemy's documentation recommends it.
import asyncio # essentially an async version of requests

# ------------------------------------------------------------
# Local modules
# ------------------------------------------------------------
from ingest_bible import initialize_bible_content
from utils import get_db_url


# Test DB Setup
db_url = get_db_url('test')
engine = create_engine(db_url)

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