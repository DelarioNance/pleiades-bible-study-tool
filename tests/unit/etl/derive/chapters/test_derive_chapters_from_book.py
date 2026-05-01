import pytest

from src.etl.derive_chapters import derive_chapters_from_books
from .cases_derive_chapters_from_book import DeriveChapterCases


# ---------------------------------------------------------
# Valid cases
# ---------------------------------------------------------
@pytest.mark.parametrize("case", DeriveChapterCases.VALID)
def test_derive_chapters_from_book_valid(case):
    assert derive_chapters_from_books(case["books"]) == case["expected"]


# ---------------------------------------------------------
# Edge cases
# ---------------------------------------------------------
@pytest.mark.parametrize("case", DeriveChapterCases.EDGE)
def test_derive_chapters_from_book_edge(case):
    assert derive_chapters_from_books(case["books"]) == case["expected"]


# ---------------------------------------------------------
# Error cases
# ---------------------------------------------------------
@pytest.mark.parametrize("case", DeriveChapterCases.ERROR)
def test_derive_chapters_from_book_error(case):
    pass
