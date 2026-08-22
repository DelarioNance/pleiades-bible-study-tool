import pytest
from unittest.mock import patch, Mock

from src.etl.extract_verses import extract_verses_in_chapter_async
from .cases_extract_verses_in_chapter_async import ExtractCases
from tests.backend.utils.mocks import MockAsyncResponse, MockAsyncSession

# ---------------------------------------------------------
# Valid cases
# ---------------------------------------------------------
@pytest.mark.parametrize("case", ExtractCases.VALID)
@pytest.mark.asyncio
async def test_extract_verses_in_chapter_async_valid(case):
    mock_response = MockAsyncResponse(case["api_output"])
    mock_session = MockAsyncSession(mock_response)

    assert await extract_verses_in_chapter_async(
        mock_session,
        case["book_id"], 
        case["chapter"], 
        "fake-url"
    ) == case["expected"]


# ---------------------------------------------------------
# Edge cases
# ---------------------------------------------------------
@pytest.mark.parametrize("case", ExtractCases.EDGE)
@pytest.mark.asyncio
async def test_extract_verses_in_chapter_async_edge(case):
    mock_response = MockAsyncResponse(case["api_output"])
    mock_session = MockAsyncSession(mock_response)

    assert await extract_verses_in_chapter_async(
        mock_session,
        case["book_id"], 
        case["chapter"], 
        "fake-url"
    ) == case["expected"]


# ---------------------------------------------------------
# Error cases
# ---------------------------------------------------------
@pytest.mark.parametrize("case", ExtractCases.ERROR)
@pytest.mark.asyncio
async def test_extract_verses_in_chapter_async_error(case):
    mock_response = MockAsyncResponse(case["api_output"])
    mock_session = MockAsyncSession(mock_response)

    with pytest.raises(case["expected_exception"]):
        await extract_verses_in_chapter_async(
            mock_session,
            case["book_id"], 
            case["chapter"], 
            "fake-url"
        )
