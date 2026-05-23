from fastapi.testclient import TestClient
import pytest
from src.api.main import app
from tests.api.utils import get_book_by_order, get_chapters_by_book
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
    chosen_book = get_book_by_order(client, case["book_order"])
    chapters = get_chapters_by_book(client, chosen_book["id"])

    chapter_numbers = [chapter["number"] for chapter in chapters]
    assert chapter_numbers == list(range(1, NUM_CHAPTERS_PER_BOOK[chosen_book["name"]] + 1))


@pytest.mark.parametrize("case", [
    {
        "book_id": -1,
    },
])
def test_get_chapters_in_nonexisting_book(case):
    chapters = get_chapters_by_book(client, case["book_id"])

    assert chapters == []
