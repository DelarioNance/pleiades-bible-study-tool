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


class MockAsyncSession:
    """
    A simple mock for aiohttp.ClientSession that allows us to control the
    behavior of session.get() in our async tests.

    Why this exists:
        Some async functions receive an aiohttp.ClientSession as a parameter 
        and call session.get(url). Therefore, we need a fake (mock) session
        object that the test function can pass into the code under test. 
        
        Also, since our async functions call get(url) from the session object
        but we don't want to make real HTTP requests during unit tests, 
        this mock session must return a fake (mock) response object.
    """

    def __init__(self, mock_response):
        self.mock_response = mock_response

    def get(self, _):
        return self.mock_response
    

class MockPandasReadCSV:
    def __init__(self, dataframe):
        self.df = dataframe
    
    