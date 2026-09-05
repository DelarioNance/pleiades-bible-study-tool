import pytest
from pandas.testing import assert_frame_equal
from unittest.mock import patch

from src.etl.extract_crossrefs import extract_verse_crossrefs
from .cases_extract_verse_crossrefs import ExtractCases


@pytest.mark.parametrize("case", ExtractCases.VALID)
@patch("pandas.read_csv")
def test_extract_verse_crossrefs_valid(mock_read_csv, case):
    mock_read_csv.return_value = case["csv_read_output"]
    
    assert_frame_equal(extract_verse_crossrefs("fake-path"), case["expected"])

    mock_read_csv.assert_called_once_with(
        "fake-path",
        sep="\t",
        usecols=[
            "From Verse", 
            "To Verse", 
            "Votes"
        ],
        dtype=str
    )