from sqlalchemy import text
from sqlalchemy.orm import Session
from src.etl.drop_bible_db_tables import drop_bible_db_tables


def test_drop_bible_db_tables(test_db_engine):
    # Create tables
    table_names = ["books", "chapters", "verses", "verse_references"]

    with test_db_engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
        for table in table_names:
            conn.execute(text(f"CREATE TABLE {table} (id SERIAL PRIMARY KEY);"))
           
    with test_db_engine.connect() as conn:
        tables_before = conn.execute(text("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public';
        """)).fetchall()
        
    assert {t[0] for t in tables_before} == set(table_names), "Setup failed to create the expected tables."
        
    with test_db_engine.begin() as conn:
        drop_bible_db_tables(conn, table_names_ordered=['verse_references', 'verses', 'chapters', 'books'])

    with test_db_engine.connect() as conn:
        tables_after = conn.execute(text("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public';
        """)).fetchall()
    
    assert len(tables_after) == 0
