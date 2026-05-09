"""
Database test fixtures for pytest.

This module provides pytest fixtures for test functions. Pytest fixtures 
act as dependency-injected resources: when a test function declares a 
parameter with the same name as a fixture, pytest automatically calls 
the fixture and passes its return (or yield) value into the test.

Fixtures that use `yield` are split into three phases:

1. Setup phase (code before `yield`)
   Pytest runs this before the test begins.

2. Yield phase
   The test uses the object yielded by the fixture as its parameter.

3. Teardown phase (code after `yield`)
   Pytest runs this after the test finishes, even if the test fails. This
   is helpful for cleaning up resources like database connections, 
   temporary files, etc.
"""

import pytest
import uuid # used to generate random test database names
from sqlalchemy import text

from src.utils.db import get_db_engine, create_engine

@pytest.fixture 
def test_db_engine():
    # To create a new database, we need to connect to an existing database.
    # The admin database was chosen to avoid damaging the test or prod database.
    admin_db_engine = get_db_engine("admin")
    test_db_name = f'test_{uuid.uuid4().hex}' # hex is used to remove dashes from the UUID string, which are not allowed in Postgres DB names

    # AUTOCOMMIT is needed to allow CREATE DATABASE and DROP DATABASE commands to run
    # in what is a transaction by default.
    with admin_db_engine.connect().execution_options(isolation_level='AUTOCOMMIT') as conn:
        conn.execute(text(f"DROP DATABASE IF EXISTS {test_db_name};"))
        conn.execute(text(f"CREATE DATABASE {test_db_name};"))

    admin_db_user = admin_db_engine.url.username
    admin_db_password = admin_db_engine.url.password

    test_db_engine = create_engine(f"postgresql+psycopg2://{admin_db_user}:{admin_db_password}@localhost/{test_db_name}")

    yield test_db_engine

    with admin_db_engine.connect().execution_options(isolation_level='AUTOCOMMIT') as conn:
        conn.execute(text(f"DROP DATABASE IF EXISTS {test_db_name};"))