# This script will possibly error out if the environment is neither SANDBOX nor TEST, 
# because the test data is only loaded in those environments. The tests will fail if 
# the test data is not present in the database. This currently is not an issue because
# the ETL tests are only run in the SANDBOX (local dev) and TEST CI environments (GitHub Actions). 
from sqlalchemy import text
from src.etl.data_test_seed import TEST_BOOKS, TEST_CHAPTERS, TEST_VERSES, TEST_VERSE_REFERENCES

def test_correct_number_of_seed_books(conn_from_etl_run):
    query = text("""
        SELECT COUNT(id) 
        FROM books
        WHERE is_test = TRUE;
    """)
    (count,) = conn_from_etl_run.execute(query).one() # one is used instead of scalar to error if the query does not return exactly 1 row

    expected_num_books = len(TEST_BOOKS)

    assert count == expected_num_books, f"Expected {expected_num_books} books, found {count}"


def test_correct_number_of_seed_chapters(conn_from_etl_run):
    query = text("""
        SELECT COUNT(id) 
        FROM chapters
        WHERE is_test = TRUE;
    """)
    (count,) = conn_from_etl_run.execute(query).one() # one is used instead of scalar to error if the query does not return exactly 1 row

    expected_num_chapters = len(TEST_CHAPTERS)

    assert count == expected_num_chapters, f"Expected {expected_num_chapters} chapters, found {count}"

def test_correct_number_of_seed_verses(conn_from_etl_run):
    query = text("""
        SELECT COUNT(id) 
        FROM verses
        WHERE is_test = TRUE;
    """)
    (count,) = conn_from_etl_run.execute(query).one() # one is used instead of scalar to error if the query does not return exactly 1 row

    expected_num_verses = len(TEST_VERSES)

    assert count == expected_num_verses, f"Expected {expected_num_verses} verses, found {count}"


def test_correct_number_of_seed_verse_references(conn_from_etl_run):
    query = text("""
        SELECT COUNT(id) 
        FROM verse_references
        WHERE is_test = TRUE;
    """)
    (count,) = conn_from_etl_run.execute(query).one() # one is used instead of scalar to error if the query does not return exactly 1 row

    expected_num_verse_references = len(TEST_VERSE_REFERENCES)

    assert count == expected_num_verse_references, f"Expected {expected_num_verse_references} verse references, found {count}"