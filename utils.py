# ------------------------------------------------------------
# Standard library
# ------------------------------------------------------------
import os
from dotenv import load_dotenv

# ------------------------------------------------------------
# Third‑party packages
# ------------------------------------------------------------
from sqlalchemy import create_engine, text # not sure why text is needed, but SQLAlchemy's documentation recommends it.

# ------------------------------------------------------------
# Local modules
# ------------------------------------------------------------


load_dotenv()


def get_db_url(env_alias):
    if env_alias == 'test':
        return os.getenv('DB_URL_TEST')
    elif env_alias == 'prod':
        return os.getenv('DB_URL_PROD')
    else:
        raise ValueError(f"Invalid environment alias '{env_alias}'.")


def get_db_engine(env_alias):
    db_url = get_db_url(env_alias)
    return create_engine(db_url)


def query_scalar(conn, sql):
    sql_text = text(sql)
    sql_result = conn.execute(sql_text)

    rows = sql_result.fetchall()
    
    if len(rows) != 1 or len(rows[0]) != 1:
        raise ValueError(f"Expected a single scalar value, but got {len(rows)} rows and {len(rows[0]) if rows else 0} columns.")
    
    return rows[0][0]


def assert_no_results(conn, sql):
    sql_text = text(sql)
    exceptions = conn.execute(sql_text).fetchall()
    assert len(exceptions) == 0, f"Expected no exceptions, but got {len(exceptions)}: {exceptions}"