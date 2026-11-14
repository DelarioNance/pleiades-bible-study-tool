import pytest

from src.etl.transform.transform_crossrefs import get_chapter_from_normalized_ref

from .cases_get_chapter_from_normalized_ref import GetChapterCases


# ---------------------------------------------------------
# Valid cases
# ---------------------------------------------------------
@pytest.mark.parametrize("case", GetChapterCases.VALID)
def test_get_chapter_valid(case):
    assert get_chapter_from_normalized_ref(case["input"]) == case["expected"]


# ---------------------------------------------------------
# Edge cases
# ---------------------------------------------------------
@pytest.mark.parametrize("case", GetChapterCases.EDGE)
def test_get_chapter_edge(case):
    assert get_chapter_from_normalized_ref(case["input"]) == case["expected"]


# ---------------------------------------------------------
# Error cases
# ---------------------------------------------------------
@pytest.mark.parametrize("case", GetChapterCases.ERROR)
def test_get_chapter_error(case):
    with pytest.raises(Exception):
        get_chapter_from_normalized_ref(case["input"])
