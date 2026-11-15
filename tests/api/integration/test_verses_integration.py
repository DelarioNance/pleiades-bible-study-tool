import pytest
from fastapi.testclient import TestClient

from src.api.main import app
from tests.api.integration.verses_integration_expected_results import (
    expected_bfs_results,
)
from tests.api.utils import (
    get_book_by_order,
    get_chapter_by_book_order_and_chapter_number,
    get_verse_bfs_response,
    get_verse_by_text,
    get_verses_by_book_id_and_chapter_number,
    get_verses_by_chapter_id,
)
from tests.etl.constants import NUM_VERSES_PER_ASCENDING_CHAPTER

client = TestClient(app)


@pytest.mark.parametrize(
    "case",
    [
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
    ],
)
def test_get_verses_from_chapter_id_existing_integration(case):
    chosen_book = get_book_by_order(client, case["book_order"])
    chosen_chapter = get_chapter_by_book_order_and_chapter_number(
        client, chosen_book["book_order"], case["chapter_number"]
    )
    verses = get_verses_by_chapter_id(client, chosen_chapter["chapter_id"])

    verse_numbers = [verse["verse_number"] for verse in verses]
    assert verse_numbers == list(
        range(
            1,
            NUM_VERSES_PER_ASCENDING_CHAPTER[chosen_book["book_name"]][
                case["chapter_number"] - 1
            ]
            + 1,
        )
    )

    first_verse_text = verses[0]["verse_text"]
    assert first_verse_text == case["first_verse_text"]

    last_verse_text = verses[-1]["verse_text"]
    assert last_verse_text == case["last_verse_text"]


@pytest.mark.parametrize(
    "case",
    [
        {
            "chapter_id": -1,
        },
    ],
)
def test_get_verses_from_chapter_id_nonexistent_integration(case):
    verses = get_verses_by_chapter_id(client, case["chapter_id"])

    assert verses == []


# will want to remove the hardcoded verse ids
@pytest.mark.parametrize(
    "case",
    [
        {
            "verse_id": get_verse_by_text(client, "TEST ROOT: No children"),
            "expected_result": expected_bfs_results["TEST ROOT: No children"],
        },
        {
            "verse_id": get_verse_by_text(client, "TEST ROOT: Dense at layers 0-2"),
            "expected_result": expected_bfs_results["TEST ROOT: Dense at layers 0-2"],
        },
        {
            "verse_id": get_verse_by_text(
                client, "TEST ROOT: Dense at layers 0-1; sparse as layer 2"
            ),
            "expected_result": expected_bfs_results[
                "TEST ROOT: Dense at layers 0-1; sparse as layer 2"
            ],
        },
        {
            "verse_id": get_verse_by_text(client, "TEST ROOT: 1 child"),
            "expected_result": expected_bfs_results["TEST ROOT: 1 child"],
        },
        {
            "verse_id": get_verse_by_text(
                client, "TEST ROOT: 3 children, middle has children"
            ),
            "expected_result": expected_bfs_results[
                "TEST ROOT: 3 children, middle has children"
            ],
        },
        {
            "verse_id": get_verse_by_text(
                client, "TEST ROOT: Chain past depth limit (4 layers)"
            ),
            "expected_result": expected_bfs_results[
                "TEST ROOT: Chain past depth limit (4 layers)"
            ],
        },
    ],
)
def test_verse_bfs_integration(case):
    response = get_verse_bfs_response(client, case["verse_id"])
    data = response.json()

    expected_result = case["expected_result"]
    normalized_data = _normalize_response_json(data, expected_result)

    assert normalized_data == expected_result, (
        f"Expected {expected_result}, but got {normalized_data}"
    )


def _normalize_response_json(data, expected):
    verse_id_to_verse_text = {
        verse["verse_id"]: verse["verse_text"]
        for level in data.values()
        for verse in level
    }
    filtered_verse_fields = {
        field
        for verses in expected.values()
        for verse in verses
        for field in verse
    }

    return {
        level: [
            _normalize_verse(verse, verse_id_to_verse_text, filtered_verse_fields)
            for verse in verses
        ]
        for level, verses in data.items()
    }


@pytest.mark.parametrize(
    "case",
    [
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
    ],
)
def test_get_verses_from_book_id_and_chapter_number_existing(case):
    chosen_book = get_book_by_order(client, case["book_order"])
    verses = get_verses_by_book_id_and_chapter_number(
        client, chosen_book["book_id"], case["chapter_number"]
    )

    verse_numbers = [verse["verse_number"] for verse in verses]
    assert verse_numbers == list(
        range(
            1,
            NUM_VERSES_PER_ASCENDING_CHAPTER[chosen_book["book_name"]][
                case["chapter_number"] - 1
            ]
            + 1,
        )
    )

    first_verse_text = verses[0]["verse_text"]
    assert first_verse_text == case["first_verse_text"]

    last_verse_text = verses[-1]["verse_text"]
    assert last_verse_text == case["last_verse_text"]


@pytest.mark.parametrize(
    "case",
    [
        {
            "book_id": -1,
            "chapter_number": 1,
        },
        {
            "book_id": 1,
            "chapter_number": -1,
        },
    ],
)
def test_get_verses_from_book_id_and_chapter_number_nonexistent_integration(case):
    verses = get_verses_by_book_id_and_chapter_number(
        client, case["book_id"], case["chapter_number"]
    )

    assert verses == []


def _normalize_verse(verse, verse_id_to_verse_text, filtered_verse_fields):
    verse_with_parent_text = {
        **verse,
        "parent_text": verse_id_to_verse_text.get(verse["parent_id"], None),
    }
    return {field: verse_with_parent_text[field] for field in filtered_verse_fields}
