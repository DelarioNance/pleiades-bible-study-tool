from fastapi.testclient import TestClient
import pytest
from src.api.main import app
from tests.utils.constants import NUM_VERSES_PER_ASCENDING_CHAPTER


client = TestClient(app)

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
def test_get_verses_in_existing_chapter(case):
    books = client.get("/v1/books/").json()
    chosen_book = next(book for book in books if book["order"] == case["book_order"])

    verses = client.get(f"/v1/books/{chosen_book['id']}/chapters/{case['chapter_number']}/verses").json()

    verse_numbers = [verse["number"] for verse in verses]
    chosen_book_name = chosen_book["name"]
    assert verse_numbers == list(range(1, NUM_VERSES_PER_ASCENDING_CHAPTER[chosen_book_name][case['chapter_number']-1] + 1))

    first_verse_text = verses[0]["text"]
    last_verse_text = verses[-1]["text"]
    assert first_verse_text == case["first_verse_text"]
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
def test_get_verses_in_nonexisting_chapter(case):
    verses = client.get(f"/v1/books/{case['book_id']}/chapters/{case['chapter_number']}/verses").json()

    assert verses == []
