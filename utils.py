# ------------------------------------------------------------
# Standard library
# ------------------------------------------------------------
import os
from dotenv import load_dotenv

# ------------------------------------------------------------
# Third‑party packages
# ------------------------------------------------------------
from sqlalchemy import create_engine

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