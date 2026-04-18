import pytest
from utils.db import get_db_url

@pytest.mark.parametrize("env_alias, user, password, name, expected", [
    (
        "test",
        "test_user",
        "test_pass",
        "mydb_test",
        "postgresql+psycopg2://test_user:test_pass@localhost/mydb_test",
    ),
    (
        "prod",
        "prod_user",
        "prod_pass",
        "mydb_prod",
        "postgresql+psycopg2://prod_user:prod_pass@localhost/mydb_prod",
    ),
])
def test_get_db_url_valid_alias(monkeypatch, env_alias, user, password, name, expected):
    # Inject the test environment variables into the 'os' environment
    monkeypatch.setenv(f"DB_USER_{env_alias.upper()}", user)
    monkeypatch.setenv(f"DB_PASSWORD_{env_alias.upper()}", password)
    monkeypatch.setenv(f"DB_NAME_{env_alias.upper()}", name)

    result = get_db_url(env_alias)
    assert result == expected


@pytest.mark.parametrize("env_alias", [
    ('TEST',),
    ('PROD',),
    ('other',),
])
def test_get_db_url_invalid_alias(env_alias):
    with pytest.raises(ValueError):
        get_db_url(env_alias)
