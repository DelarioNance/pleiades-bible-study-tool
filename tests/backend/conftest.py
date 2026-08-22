import pytest

from tests.backend.utils.helpers import create_random_test_db, dispose_random_test_db


@pytest.fixture(scope="function") # function is default scope, but explicitly stating it here to contrast with session-scoped fixtures
def fresh_test_db_engine():
   test_db_engine = create_random_test_db()
   yield test_db_engine
   dispose_random_test_db(test_db_engine)