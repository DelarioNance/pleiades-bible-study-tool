import pytest

from src.etl.transform.transform_crossrefs import get_book_from_normalized_ref

from .cases_get_book_from_normalized_ref import GetBookCases


# ---------------------------------------------------------
# Valid cases
# ---------------------------------------------------------
@pytest.mark.parametrize("case", GetBookCases.VALID)
def test_get_book_valid(case):
    assert get_book_from_normalized_ref(case["input"]) == case["expected"]


# ---------------------------------------------------------
# Edge cases
# ---------------------------------------------------------
@pytest.mark.parametrize("case", GetBookCases.EDGE)
def test_get_book_edge(case):
    assert get_book_from_normalized_ref(case["input"]) == case["expected"]


# ---------------------------------------------------------
# Error cases
# ---------------------------------------------------------
@pytest.mark.parametrize("case", GetBookCases.ERROR)
def test_get_book_error(case):
    with pytest.raises(Exception):
        get_book_from_normalized_ref(case["input"])
