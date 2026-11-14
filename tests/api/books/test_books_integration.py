from fastapi.testclient import TestClient
from src.api.main import app
from tests.etl.constants import BOOKS_IN_NUMBER_ORDER
from tests.api.utils import get_books, get_verses_by_book_id_and_chapter_number
from tests.api.utils import get_book_by_order, get_chapters_by_book_id
from tests.etl.constants import BOOKS_IN_NUMBER_ORDER, NUM_CHAPTERS_PER_BOOK
import pytest
from tests.etl.constants import NUM_VERSES_PER_ASCENDING_CHAPTER

client = TestClient(app)


def test_get_books_integration():
    books = get_books(client)

    orders = [book["order"] for book in books]    
    assert orders == list(range(1, len(BOOKS_IN_NUMBER_ORDER) + 1))

    names = [book["name"] for book in books]
    assert names == BOOKS_IN_NUMBER_ORDER


@pytest.mark.parametrize("case", [
    {
        "book_order": 1,
    },
    {
        "book_order": 66,
    },
])
def test_get_chapters_from_book_id_existing_integration(case):
    chosen_book = get_book_by_order(client, case["book_order"])
    chapters = get_chapters_by_book_id(client, chosen_book["id"])

    chapter_numbers = [chapter["number"] for chapter in chapters]
    assert chapter_numbers == list(range(1, NUM_CHAPTERS_PER_BOOK[chosen_book["name"]] + 1))


@pytest.mark.parametrize("case", [
    {
        "book_id": -1,
    },
])
def test_get_chapters_from_book_id_nonexistent_integration(case):
    chapters = get_chapters_by_book_id(client, case["book_id"])

    assert chapters == []


@pytest.mark.parametrize("case", [
    {
        "book_order": 1,
        "chapter_number": 1,
        "first_verse_text": "In the beginning God created the heaven and the earth.",
        "last_verse_text": "And God saw every thing that he had made, and, behold, it was very good. And the evening and the morning were the sixth day.",
    },
    {
        "book_order": 1,
        "chapter_number": 50,
        "first_verse_text": "And Joseph fell upon his father’s face, and wept upon him, and kissed him.",
        "last_verse_text": "So Joseph died, being an hundred and ten years old: and they embalmed him, and he was put in a coffin in Egypt.",
    },
    {
        "book_order": 66,
        "chapter_number": 1,
        "first_verse_text": "The Revelation of Jesus Christ, which God gave unto him, to shew unto his servants things which must shortly come to pass; and he sent and signified it by his angel unto his servant John:",
        "last_verse_text": "The mystery of the seven stars which thou sawest in my right hand, and the seven golden candlesticks. The seven stars are the angels of the seven churches: and the seven candlesticks which thou sawest are the seven churches.",
    },
    {
        "book_order": 66,
        "chapter_number": 22,
        "first_verse_text": "And he shewed me a pure river of water of life, clear as crystal, proceeding out of the throne of God and of the Lamb.",
        "last_verse_text": "The grace of our Lord Jesus Christ be with you all. Amen.",
    },
])
def test_get_verses_from_book_id_and_chapter_number_existing(case):
    chosen_book = get_book_by_order(client, case["book_order"])
    verses = get_verses_by_book_id_and_chapter_number(client, chosen_book["id"], case["chapter_number"])

    verse_numbers = [verse["number"] for verse in verses]
    assert verse_numbers == list(range(1, NUM_VERSES_PER_ASCENDING_CHAPTER[chosen_book["name"]][case['chapter_number']-1] + 1))

    first_verse_text = verses[0]["text"]
    assert first_verse_text == case["first_verse_text"]

    last_verse_text = verses[-1]["text"]
    assert last_verse_text == case["last_verse_text"]


@pytest.mark.parametrize("case", [
    {
        "book_id": -1,
        "chapter_number": 1,
    },
    {
        "book_id": 1,
        "chapter_number": -1,
    },
])
def test_get_verses_from_book_id_and_chapter_number_nonexistent_integration(case):
    verses = get_verses_by_book_id_and_chapter_number(client, case["book_id"], case["chapter_number"])

    assert verses == []
