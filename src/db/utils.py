import os

from dotenv import load_dotenv
from sqlalchemy import Engine, create_engine

load_dotenv()


def get_db_url(env_alias: str) -> str:
    # Local development
    if env_alias == "sandbox":
        user = os.getenv("DB_USER_SANDBOX")
        password = os.getenv("DB_PASSWORD_SANDBOX")
        name = os.getenv("DB_NAME_SANDBOX")
        host = os.getenv("DB_HOST_SANDBOX")

    # Used by ETL test suite to test the creation and
    # dropping of database tables.
    elif env_alias == "admin":
        user = os.getenv("DB_USER_ADMIN")
        password = os.getenv("DB_PASSWORD_ADMIN")
        name = os.getenv("DB_NAME_ADMIN")
        host = os.getenv("DB_HOST_ADMIN")

    # Used by Continuous Integration (CI) testing in GitHub 
    # Actions. GitHub Actions injects values for the "test" 
    # environment variables.
    elif env_alias == "test":
        user = os.getenv("DB_USER_TEST")
        password = os.getenv("DB_PASSWORD_TEST")
        name = os.getenv("DB_NAME_TEST")
        host = os.getenv("DB_HOST_TEST")

    # If ran locally from the command line with, the .env 
    # file will be used to provide the staging database 
    # credentials. If ran in FastAPI Cloud Staging, the 
    # .env file is not included in version control, and 
    # FastAPI Cloud Staging will inject its environment 
    # variables for the staging database.
    elif env_alias == "staging":
        user = os.getenv("DB_USER_STAGING")
        password = os.getenv("DB_PASSWORD_STAGING")
        name = os.getenv("DB_NAME_STAGING")
        host = os.getenv("DB_HOST_STAGING")

    elif env_alias == "prod":
        user = os.getenv("DB_USER_PROD")
        password = os.getenv("DB_PASSWORD_PROD")
        name = os.getenv("DB_NAME_PROD")
        host = os.getenv("DB_HOST_PROD")

    else:
        raise ValueError(f"Invalid environment alias '{env_alias}'.")

    return f"postgresql+psycopg2://{user}:{password}@{host}/{name}"


def get_db_engine(env_alias: str) -> "Engine":
    db_url = get_db_url(env_alias)
    return create_engine(db_url)


def get_current_engine() -> "Engine":
    env = os.getenv("PLEIADES_ENV", "sandbox")
    return get_db_engine(env)
