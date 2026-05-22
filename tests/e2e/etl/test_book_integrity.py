from sqlalchemy import text

def test_no_duplicate_book_names(conn_from_etl_run):
    query = text("""
        SELECT common_name, COUNT(*) AS cnt
        FROM books
        GROUP BY common_name
        HAVING COUNT(*) > 1;
    """)

    duplicates = conn_from_etl_run.execute(query).fetchall()

    assert duplicates == [], f"Duplicate book names found: {duplicates}"


def test_no_missing_book_name(conn_from_etl_run):
    query = text("""
        SELECT id, common_name
        FROM books
        WHERE COALESCE(TRIM(common_name), '') = ''
    """)

    missing = conn_from_etl_run.execute(query).fetchall()

    assert missing == [], f"Books with missing or blank names found: {missing}"
