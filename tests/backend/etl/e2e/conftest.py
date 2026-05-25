import pytest
import asyncio
from src.etl.pipeline import pipeline
from tests.backend.utils.helpers import create_random_test_db, dispose_random_test_db


@pytest.fixture(scope="session") # so tests in the same pytest run can share the same ETL result instead of each running the ETL pipeline separately
def db_engine_from_etl_run():
    test_db_engine = create_random_test_db()
    asyncio.run(pipeline(
        bible_api_url="https://bible.helloao.org/api/eng_kjv", 
        engine=test_db_engine
    ))
    yield test_db_engine
    
    dispose_random_test_db(test_db_engine)

@pytest.fixture(scope="session") # so tests in the same pytest run can share the same ETL result instead of each running the ETL pipeline separately
def conn_from_etl_run(db_engine_from_etl_run):
    with db_engine_from_etl_run.connect() as conn:
        yield conn
