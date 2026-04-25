import pytest
from unittest.mock import patch, Mock

from bible_ingestion.extract_books import extract_books
from .cases_extract_books import ExtractCases


@pytest.mark.parametrize("case", ExtractCases.VALID)
@patch("requests.get")
def test_extract_books_valid(mock_get, case):
    mock_response = Mock()
    mock_response.json.return_value = case["api_output"]
    mock_get.return_value = mock_response

    assert extract_books("fake-url") == case["expected"]


@pytest.mark.parametrize("case", ExtractCases.EDGE)
@patch("requests.get")
def test_extract_books_edge(mock_get, case):
    mock_response = Mock()
    mock_response.json.return_value = case["api_output"]
    mock_get.return_value = mock_response

    assert extract_books("fake-url") == case["expected"]


@pytest.mark.parametrize("case", ExtractCases.ERROR)
@patch("requests.get")
def test_extract_books_error(mock_get, case):
    mock_response = Mock()
    mock_response.json.return_value = case["api_output"]
    mock_get.return_value = mock_response

    with pytest.raises(case["expected_exception"]):
        extract_books("fake-url")
