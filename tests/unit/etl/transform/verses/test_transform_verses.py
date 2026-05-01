import pytest

from src.etl.transfom_verses import transform_verses
from .cases_transform_verses import TransformCases

# ---------------------------------------------------------
# Valid cases
# ---------------------------------------------------------
@pytest.mark.parametrize("case", TransformCases.VALID)
def test_transform_verses_valid(case):
    assert transform_verses(case['input']) == case["expected"]


# ---------------------------------------------------------
# Edge cases
# ---------------------------------------------------------
@pytest.mark.parametrize("case", TransformCases.EDGE)
def test_transform_verses_edge(case):
    assert transform_verses(case['input']) == case["expected"]


# ---------------------------------------------------------
# Error cases
# ---------------------------------------------------------
@pytest.mark.parametrize("case", TransformCases.ERROR)
@pytest.mark.asyncio
def test_transform_verses_error(case):
    pass