import pytest

from src.etl.transform.transform_crossrefs import get_verse_from_normalized_ref

from .cases_get_verse_from_normalized_ref import GetVerseCases


# ---------------------------------------------------------
# Valid cases
# ---------------------------------------------------------
@pytest.mark.parametrize("case", GetVerseCases.VALID)
def test_get_verse_valid(case):
    assert get_verse_from_normalized_ref(case["input"]) == case["expected"]


# ---------------------------------------------------------
# Edge cases
# ---------------------------------------------------------
@pytest.mark.parametrize("case", GetVerseCases.EDGE)
def test_get_verse_edge(case):
    assert get_verse_from_normalized_ref(case["input"]) == case["expected"]


# ---------------------------------------------------------
# Error cases
# ---------------------------------------------------------
@pytest.mark.parametrize("case", GetVerseCases.ERROR)
def test_get_verse_error(case):
    with pytest.raises(Exception):
        get_verse_from_normalized_ref(case["input"])
