import pytest
from fastapi.testclient import TestClient

from src.api.main import app
from tests.api.utils import (
    get_book_by_order,
    get_chapters_by_book_id,
)
from tests.etl.constants import (
    NUM_CHAPTERS_PER_BOOK,
)

client = TestClient(app)


@pytest.mark.parametrize(
    "case",
    [
        {
            "book_order": 1,
        },
        {
            "book_order": 66,
        },
    ],
)
def test_get_chapters_from_book_id_existing_integration(case):
    chosen_book = get_book_by_order(client, case["book_order"])
    chapters = get_chapters_by_book_id(client, chosen_book["book_id"])

    chapter_numbers = [chapter["chapter_number"] for chapter in chapters]
    assert chapter_numbers == list(
        range(1, NUM_CHAPTERS_PER_BOOK[chosen_book["book_name"]] + 1)
    )


@pytest.mark.parametrize(
    "case",
    [
        {
            "book_id": -1,
        },
    ],
)
def test_get_chapters_from_book_id_nonexistent_integration(case):
    chapters = get_chapters_by_book_id(client, case["book_id"])

    assert chapters == []
