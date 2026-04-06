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
    # Dynamically generate URL to avoid
    # storing an URL repo variable 
    # alongside the corresponding 
    # name, user, and password repo
    # variables in Bitbucket
    if env_alias == 'test':
        user = os.getenv("DB_USER_TEST")
        password = os.getenv("DB_PASSWORD_TEST")
        name = os.getenv("DB_NAME_TEST")
        suffix = '_test'
    elif env_alias == 'prod':
        user = os.getenv("DB_USER_PROD")
        password = os.getenv("DB_PASSWORD_PROD")
        name = os.getenv("DB_NAME_PROD")
        suffix = '_prod'
    else:
        raise ValueError(f"Invalid environment alias '{env_alias}'.")

    assert name.endswith(suffix), f"The {env_alias} DB name does not end in '{suffix}'" # at one point, the test and prod credentials were flip-flopped in the .env file
    
    return f"postgresql+psycopg2://{user}:{password}@localhost/{name}"


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
    sql_text = text(sql) # could possibly abstract the "SELECT 1 as existence_placeholder" pattern into this function, but this logic suffices for now
    exceptions = conn.execute(sql_text).fetchall()
    assert len(exceptions) == 0, f"Expected no exceptions, but got {len(exceptions)}: {exceptions}"
    