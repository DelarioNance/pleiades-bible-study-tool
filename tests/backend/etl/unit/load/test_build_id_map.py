import pytest
from src.etl.build_id_map import build_id_map
from .cases_build_id_map import BuildIdMapCases


# ---------------------------------------------------------
# VALID cases
# ---------------------------------------------------------
@pytest.mark.parametrize("case", BuildIdMapCases.VALID)
def test_build_id_map_valid(case):
    result = build_id_map(case["from_items"], case["to_ids"], case["key"])
    assert result == case["expected"]


# ---------------------------------------------------------
# EDGE cases
# ---------------------------------------------------------
@pytest.mark.parametrize("case", BuildIdMapCases.EDGE)
def test_build_id_map_edge(case):
    result = build_id_map(case["from_items"], case["to_ids"], case["key"])
    assert result == case["expected"]


# ---------------------------------------------------------
# ERROR cases
# ---------------------------------------------------------
@pytest.mark.parametrize("case", BuildIdMapCases.ERROR)
def test_build_id_map_error(case):
    with pytest.raises(case["expected_exception"]):
        build_id_map(case["from_items"], case["to_ids"], case["key"])
