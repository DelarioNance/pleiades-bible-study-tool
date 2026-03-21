import os

from dotenv import load_dotenv

load_dotenv()


def get_db_url(env_alias):
    if env_alias == 'test':
        return os.getenv('DB_URL_TEST')
    elif env_alias == 'prod':
        return os.getenv('DB_URL_PROD')
    else:
        raise ValueError(f"Invalid environment alias '{env_alias}'.")
