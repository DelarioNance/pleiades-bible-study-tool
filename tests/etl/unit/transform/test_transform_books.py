import pytest

from src.etl.transform.transform_books import transform_books

from .cases_transform_books import TransformCases


# ---------------------------------------------------------
# Valid cases
# ---------------------------------------------------------
@pytest.mark.parametrize("case", TransformCases.VALID)
def test_transform_books_valid(case):
    assert transform_books(case["input"]) == case["expected"]


# ---------------------------------------------------------
# Edge cases
# ---------------------------------------------------------
@pytest.mark.parametrize("case", TransformCases.EDGE)
def test_transform_books_edge(case):
    assert transform_books(case["input"]) == case["expected"]


# ---------------------------------------------------------
# Error cases
# ---------------------------------------------------------
@pytest.mark.parametrize("case", TransformCases.ERROR)
@pytest.mark.asyncio
def test_transform_books_error(case):
    pass
