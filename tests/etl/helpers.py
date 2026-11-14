import os
import uuid  # used to generate random test database names

from sqlalchemy import text

from src.db.utils import create_engine, get_db_engine


def create_random_test_db():
    # To create a new database, we need to connect to an existing database.
    # The admin database was chosen to avoid damaging the test or prod database.
    admin_db_engine = get_db_engine("admin")
    test_db_name = f"test_{uuid.uuid4().hex}"  # hex is used to remove dashes from the UUID string, which are not allowed in Postgres DB names

    import os

    print("ADMIN HOST =", repr(admin_db_engine.url.host))
    print("ENV HOST   =", repr(os.getenv("DB_HOST_ADMIN")))

    # AUTOCOMMIT is needed to allow CREATE DATABASE and DROP DATABASE commands to run
    # in what is a transaction by default.
    with admin_db_engine.connect().execution_options(
        isolation_level="AUTOCOMMIT"
    ) as conn:
        conn.execute(text(f"DROP DATABASE IF EXISTS {test_db_name};"))
        conn.execute(text(f"CREATE DATABASE {test_db_name};"))

    admin_db_user = admin_db_engine.url.username
    admin_db_password = admin_db_engine.url.password
    admin_db_host = admin_db_engine.url.host

    test_db_engine = create_engine(
        f"postgresql+psycopg2://{admin_db_user}:{admin_db_password}@{admin_db_host}/{test_db_name}"
    )

    return test_db_engine


def dispose_random_test_db(test_db_engine):
    admin_db_engine = get_db_engine("admin")

    # We can't drop the database while there are active connections to it.
    # Even though transactions/connections used by Python appear to be closed,
    # they are still used in a connection pool. The dispose method is used
    # to forcefully close all connections in the pool.
    test_db_engine.dispose()

    with admin_db_engine.connect().execution_options(
        isolation_level="AUTOCOMMIT"
    ) as conn:
        conn.execute(text(f"DROP DATABASE IF EXISTS {test_db_engine.url.database};"))
