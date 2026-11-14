from fastapi.testclient import TestClient

from src.api.main import app
from tests.api.utils import (
    get_books,
)
from tests.etl.constants import (
    BOOKS_IN_NUMBER_ORDER,
)

client = TestClient(app)


def test_get_books_integration():
    books = get_books(client)

    orders = [book["book_order"] for book in books]
    assert orders == list(range(1, len(BOOKS_IN_NUMBER_ORDER) + 1))

    names = [book["book_name"] for book in books]
    assert names == BOOKS_IN_NUMBER_ORDER
