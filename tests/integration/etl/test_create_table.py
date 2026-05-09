from sqlalchemy import text, inspect
from src.etl.create_tables import create_table


def test_create_table(test_db_engine):
    table_sql = """
        CREATE TABLE example_table (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            value INT NOT NULL
        );
    """
    table_name = "example_table"
    expected_columns = {"id", "name", "value"}

    with test_db_engine.begin() as conn:
        create_table(conn, table_sql)

        inspector = inspect(conn)

        assert table_name in inspector.get_table_names()

        cols = {col["name"] for col in inspector.get_columns(table_name)}
        assert expected_columns == cols