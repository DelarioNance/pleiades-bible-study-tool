from sqlalchemy import text

def create_or_replace_function(conn, function_creation_sql_str):
    conn.execute(text(function_creation_sql_str))