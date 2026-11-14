
import asyncio

import pytest

from src.db.utils import get_current_engine
from src.etl.pipeline import pipeline


@pytest.fixture(scope="session") # so tests in the same pytest run can share the same ETL result instead of each running the ETL pipeline separately
def db_engine_from_etl_run():
    engine = get_current_engine()
    asyncio.run(pipeline(
        engine=engine,
        load_test_data=True,
    ))
    yield engine


@pytest.fixture(scope="session") # so tests in the same pytest run can share the same ETL result instead of each running the ETL pipeline separately
def conn_from_etl_run(db_engine_from_etl_run):
    with db_engine_from_etl_run.connect() as conn:
        yield conn
