from sqlalchemy import text

def create_table(conn, table_creation_sql_str):
    conn.execute(text(table_creation_sql_str))