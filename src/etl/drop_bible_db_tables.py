from sqlalchemy import text


def drop_bible_db_tables(conn, table_names_ordered): # should be ordered in drop order
    for table_name in table_names_ordered: # order matters here due to foreign key constraints
        conn.execute(text(f'DROP TABLE IF EXISTS {table_name};'))