import pytest
from unittest.mock import patch, Mock

from src.etl.extract_verses import extract_verses_in_chapter_async
from .cases_extract_verses_in_chapter import ExtractCases


class MockAsyncResponse:
    """
    A lightweight stand‑in for aiohttp's ClientResponse object, used for
    unit testing async HTTP code without making real network calls.

    Why this exists:
        In aiohttp, `session.get(url)` returns an object that is both:
        - an asynchronous context manager (used with `async with`)
        - a response object with coroutine methods like `.json()` or `.text()`

        Example real code under test:
            async with http_session.get(url) as response:
                data = await response.json()

        To unit test this without hitting the network, we need a mock object
        that behaves the same way. That means implementing the async context
        manager protocol and any coroutine methods our code calls.

    What this class provides:
        - async json(): mocks the real JSON method
        - async __aenter__(): returns `self` so it can be used in `async with`
        - async __aexit__(): required by the async context manager protocol

    Notes for future me:
        - Context managers are just classes with __enter__/__exit__ methods.
          Async context managers are the same idea, but with async versions
          (__aenter__/__aexit__) that Python awaits automatically.
        - aiohttp responses do a lot internally (connection pooling, cleanup),
          but for unit tests we only need to mimic the parts our code touches.
        - If the production code ever starts calling response.text(),
          response.status, or response.headers, add those attributes/methods
          here so tests remain isolated and deterministic.
    """

    def __init__(self, json_data):
        self._json_data = json_data

    async def json(self):
        return self._json_data

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb): # Python needs 3 parameters for __aexit__, even if we don't use them
        pass


# ---------------------------------------------------------
# Valid cases
# ---------------------------------------------------------
@pytest.mark.parametrize("case", ExtractCases.VALID)
@patch("aiohttp.ClientSession.get")
@pytest.mark.asyncio
async def test_extract_verses_in_chapter_async_valid(mock_async_get, case):
    mock_response = MockAsyncResponse(case["api_output"])
    mock_async_get.return_value = mock_response

    assert await extract_verses_in_chapter_async(
        case["book_id"], 
        case["chapter"], 
        "fake-url"
    ) == case["expected"]


# ---------------------------------------------------------
# Edge cases
# ---------------------------------------------------------
@pytest.mark.parametrize("case", ExtractCases.EDGE)
@patch("requests.get")
@pytest.mark.asyncio
async def test_extract_verses_in_chapter_async_edge(mock_get, case):
    mock_response = Mock()
    mock_response.json.return_value = case["api_output"]
    mock_get.return_value = mock_response

    assert await extract_verses_in_chapter_async(
        case["book_id"], 
        case["chapter"], 
        "fake-url"
    ) == case["expected"]


# ---------------------------------------------------------
# Error cases
# ---------------------------------------------------------
@pytest.mark.parametrize("case", ExtractCases.ERROR)
@patch("requests.get")
@pytest.mark.asyncio
async def test_extract_verses_in_chapter_async_error(mock_get, case):
    mock_response = Mock()
    mock_response.json.return_value = case["api_output"]
    mock_get.return_value = mock_response

    with pytest.raises(case["expected_exception"]):
        await extract_verses_in_chapter_async(
            case["book_id"], 
            case["chapter"], 
            "fake-url"
        )
