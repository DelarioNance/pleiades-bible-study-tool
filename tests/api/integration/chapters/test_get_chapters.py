from fastapi.testclient import TestClient
import pytest
from src.api.main import app
from tests.utils.constants import BOOKS_IN_NUMBER_ORDER, NUM_CHAPTERS_PER_BOOK


client = TestClient(app)

@pytest.mark.parametrize("case", [
    {
        "book_order": 1,
    },
    {
        "book_order": 66,
    },
])
def test_get_chapters_in_existing_book(case):
    books = client.get("/v1/books/").json()
    first_book = next(book for book in books if book["order"] == case["book_order"])

    chapters = client.get(f"/v1/books/{first_book['id']}/chapters").json()

    chapter_numbers = [chapter["number"] for chapter in chapters]

    assert chapter_numbers == list(range(1, NUM_CHAPTERS_PER_BOOK[first_book["name"]] + 1))


@pytest.mark.parametrize("case", [
    {
        "book_id": -1,
    },
])
def test_get_chapters_in_nonexisting_book(case):
    chapters = client.get(f"/v1/books/{case['book_id']}/chapters").json()

    assert chapters == []
