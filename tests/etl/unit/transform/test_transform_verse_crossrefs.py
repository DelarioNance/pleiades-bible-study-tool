import pytest

from src.etl.transform.transform_crossrefs import transform_verse_crossrefs

from .cases_transform_verse_crossrefs import TransformVerseCrossrefsCases


# ---------------------------------------------------------
# Valid cases
# ---------------------------------------------------------
@pytest.mark.parametrize("case", TransformVerseCrossrefsCases.VALID)
def test_transform_verse_crossrefs_valid(case):
    assert transform_verse_crossrefs(case["input"]) == case["expected"]


# ---------------------------------------------------------
# Edge cases
# ---------------------------------------------------------
@pytest.mark.parametrize("case", TransformVerseCrossrefsCases.EDGE)
def test_transform_verse_crossrefs_edge(case):
    assert transform_verse_crossrefs(case["input"]) == case["expected"]


# ---------------------------------------------------------
# Error cases
# ---------------------------------------------------------
@pytest.mark.parametrize("case", TransformVerseCrossrefsCases.ERROR)
def test_transform_verse_crossrefs_error(case):
    with pytest.raises(Exception):
        transform_verse_crossrefs(case["input"])
