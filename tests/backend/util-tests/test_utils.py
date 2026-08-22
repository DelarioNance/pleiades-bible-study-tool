import pytest
from src.db.utils import get_db_url
from cases_utils import GetDbUrlCases


# ---------------------------------------------------------
# Valid aliases
# ---------------------------------------------------------
@pytest.mark.parametrize("case", GetDbUrlCases.VALID)
def test_get_db_url_valid_alias(monkeypatch, case):
    # Inject environment variables
    monkeypatch.setenv(f"DB_USER_{case['alias'].upper()}", case["user"])
    monkeypatch.setenv(f"DB_PASSWORD_{case['alias'].upper()}", case["password"])
    monkeypatch.setenv(f"DB_NAME_{case['alias'].upper()}", case["name"])
    monkeypatch.setenv(f"DB_HOST_{case['alias'].upper()}", case["host"])

    result = get_db_url(case["alias"])
    assert result == case["expected"]


# ---------------------------------------------------------
# Invalid aliases
# ---------------------------------------------------------
@pytest.mark.parametrize("case", GetDbUrlCases.INVALID)
def test_get_db_url_invalid_alias(case):
    with pytest.raises(ValueError):
        get_db_url(case["alias"])