import pytest

from src.etl.transform_crossrefs import normalize_ref
from .cases_normalize_ref import NormalizeRefCases

# ---------------------------------------------------------
# Valid cases
# ---------------------------------------------------------
@pytest.mark.parametrize("case", NormalizeRefCases.VALID)
def test_normalize_ref_valid(case):
    assert normalize_ref(case['input']) == case["expected"]


# ---------------------------------------------------------
# Edge cases
# ---------------------------------------------------------
@pytest.mark.parametrize("case", NormalizeRefCases.EDGE)
def test_normalize_ref_edge(case):
    assert normalize_ref(case['input']) == case["expected"]


# ---------------------------------------------------------
# Error cases
# ---------------------------------------------------------
@pytest.mark.parametrize("case", NormalizeRefCases.ERROR)
@pytest.mark.asyncio
def test_normalize_ref_error(case):
    pass