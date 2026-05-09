import os
from sqlalchemy import create_engine
from dotenv import load_dotenv


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
    elif env_alias == 'admin':
        user = os.getenv("DB_USER_ADMIN")
        password = os.getenv("DB_PASSWORD_ADMIN")
        name = os.getenv("DB_NAME_ADMIN")
        suffix = '_admin'
    else:
        raise ValueError(f"Invalid environment alias '{env_alias}'.")

    # At one point, the test and prod credentials were flip-flopped in the .env file.
    # Maybe it's worth adding a regression unit test for this function which confirms
    # that the assert works as expected?
    assert name.endswith(suffix), f"The {env_alias} DB name does not end in '{suffix}'" 

    return f"postgresql+psycopg2://{user}:{password}@localhost/{name}"


def get_db_engine(env_alias):
    db_url = get_db_url(env_alias)
    return create_engine(db_url)