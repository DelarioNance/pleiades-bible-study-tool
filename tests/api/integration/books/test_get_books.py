from fastapi.testclient import TestClient
from src.api.main import app
from tests.utils.constants import BOOKS_IN_NUMBER_ORDER

client = TestClient(app)


def test_get_books():
    response = client.get("/v1/books")
    data = response.json()

    names = [book["name"] for book in data]
    orders = [book["order"] for book in data]

    assert names == BOOKS_IN_NUMBER_ORDER
    assert orders == list(range(1, len(BOOKS_IN_NUMBER_ORDER) + 1))
