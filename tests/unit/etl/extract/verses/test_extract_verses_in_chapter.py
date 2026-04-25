import pytest
from unittest.mock import patch, Mock

from etl.extract_verses import extract_all_verses_async
from .cases_extract_verses_in_chapter import ExtractCases


# ---------------------------------------------------------
# Valid cases
# ---------------------------------------------------------
@pytest.mark.parametrize("case", ExtractCases.VALID)
@patch("requests.get")
def test_extract_verses_in_chapter_valid(mock_get, case):
    mock_response = Mock()
    mock_response.json.return_value = case["api_output"]
    mock_get.return_value = mock_response

    assert extract_verses_in_chapter(
        case["book_id"], 
        case["chapter"], 
        "fake-url"
    ) == case["expected"]


# ---------------------------------------------------------
# Edge cases
# ---------------------------------------------------------
@pytest.mark.parametrize("case", ExtractCases.EDGE)
@patch("requests.get")
def test_extract_verses_in_chapter_edge(mock_get, case):
    mock_response = Mock()
    mock_response.json.return_value = case["api_output"]
    mock_get.return_value = mock_response

    assert extract_verses_in_chapter(
        case["book_id"], 
        case["chapter"], 
        "fake-url"
    ) == case["expected"]


# ---------------------------------------------------------
# Error cases
# ---------------------------------------------------------
@pytest.mark.parametrize("case", ExtractCases.ERROR)
@patch("requests.get")
def test_extract_verses_in_chapter_error(mock_get, case):
    mock_response = Mock()
    mock_response.json.return_value = case["api_output"]
    mock_get.return_value = mock_response

    with pytest.raises(case["expected_exception"]):
        extract_verses_in_chapter(
            case["book_id"], 
            case["chapter"], 
            "fake-url"
        )
