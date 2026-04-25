from unittest.mock import (
    Mock, # used to create fake objects which custom methods and attributes
    patch # used to replace a real object with a Mock object during testing; the fake object must be named as the test function arg
) 
import pytest
from bible_ingestion.extract_books import extract_books
from .extract_test_cases import EXTRACT_BOOKS_CASES


@pytest.mark.parametrize("api_input, expected", EXTRACT_BOOKS_CASES)
@patch('requests.get')
def test_extract_books(
    mock_get,
    api_input,
    expected
 ):
    mock_response = Mock()
    mock_response.json.return_value = api_input
    mock_get.return_value = mock_response

    result = extract_books('https://fake-url')

    assert result == expected