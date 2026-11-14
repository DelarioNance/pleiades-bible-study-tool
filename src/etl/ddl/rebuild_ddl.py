from sqlalchemy import text

from src.etl.ddl.function_definitions import get_filtered_verse_reference_graph
from src.etl.ddl.table_definitions import books as book_creation
from src.etl.ddl.table_definitions import chapters as chapter_creation
from src.etl.ddl.table_definitions import verse_references as crossref_creation
from src.etl.ddl.table_definitions import verses as verse_creation


def rebuild_ddl(conn):
    rebuild_tables(conn)
    rebuild_functions(conn)


def rebuild_tables(conn):
    # Will want a cleaner/tighter way to manage tables (e.g., ORM models)
    execute_sql(conn, "DROP TABLE IF EXISTS verse_references;")
    execute_sql(conn, "DROP TABLE IF EXISTS verses;")
    execute_sql(conn, "DROP TABLE IF EXISTS chapters;")
    execute_sql(conn, "DROP TABLE IF EXISTS books;")
    execute_sql(conn, book_creation)
    execute_sql(conn, chapter_creation)
    execute_sql(conn, verse_creation)
    execute_sql(conn, crossref_creation)


def rebuild_functions(conn):
    execute_sql(conn, get_filtered_verse_reference_graph)


def execute_sql(conn, sql):
    conn.execute(text(sql))
