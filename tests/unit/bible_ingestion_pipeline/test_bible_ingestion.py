from unittest.mock import patch, Mock
import pytest
from bible_ingestion.extract_books import extract_books

@pytest.fixture
def raw_book_data_fixture():
    return {
        'books': [
            {'id': 'GEN', 'commonName': 'Genesis', 'order': 1},
            {'id': 'EXO', 'commonName': 'Exodus', 'order': 2},
        ]
    }

@pytest.fixture
def extracted_book_data_fixture():
    return {
        'GEN': {'commonName': 'Genesis', 'order': 1},
        'EXO': {'commonName': 'Exodus', 'order': 2},
    }


@patch('requests.get') # used to replace all calls to requests.get in the test function with a mock object
def test_extract_books(mock_get, raw_book_data_fixture, extracted_book_data_fixture): # mock_get is the patched version of requests.get
    mock_response = Mock()
    mock_response.json.return_value = raw_book_data_fixture # creating a fake object that mimics the behavior of a real response object from requests.get
    mock_get.return_value = mock_response # configures the patched object to return the mock response

    result = extract_books('https://fake-url')

    assert result == extracted_book_data_fixture