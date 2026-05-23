from fastapi.testclient import TestClient
from src.api.main import app
from tests.utils.constants import BOOKS_IN_NUMBER_ORDER
from tests.api.utils import get_books

client = TestClient(app)


def test_get_books():
    books = get_books(client)

    orders = [book["order"] for book in books]    
    assert orders == list(range(1, len(BOOKS_IN_NUMBER_ORDER) + 1))

    names = [book["name"] for book in books]
    assert names == BOOKS_IN_NUMBER_ORDER
