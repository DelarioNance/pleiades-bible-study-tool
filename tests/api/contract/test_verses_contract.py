import pytest
from fastapi import status
from fastapi.testclient import TestClient

from src.api.main import app
from tests.api.utils import get_verse_bfs_response, get_verse_by_text

client = TestClient(app)


@pytest.mark.parametrize(
    "case",
    [
        {"chapter_id": 1, "status_code": status.HTTP_200_OK},
        {"chapter_id": -999, "status_code": status.HTTP_200_OK},
        {"chapter_id": 1.0, "status_code": status.HTTP_200_OK},
    ],
)
def test_get_verses_from_chapter_id_contract(case):
    response = client.get(f"/v1/chapters/{case['chapter_id']}/verses")

    # status code check
    assert response.status_code == case["status_code"]

    data = response.json()

    # shape checks
    assert isinstance(data, list)
    assert all(isinstance(item, dict) for item in data)

    # key + type checks
    for item in data:
        assert "verse_id" in item
        assert "verse_number" in item
        assert "verse_text" in item

        assert isinstance(item["verse_id"], int)
        assert isinstance(item["verse_number"], int)
        assert isinstance(item["verse_text"], str)

    # ordering check
    orders = [item["verse_number"] for item in data]
    assert orders == sorted(orders)


@pytest.mark.parametrize(
    "case",
    [
        {"book_id": 1, "chapter_number": 1, "status_code": status.HTTP_200_OK},
        {"book_id": -999, "chapter_number": 1, "status_code": status.HTTP_200_OK},
        {"book_id": 1.0, "chapter_number": 1, "status_code": status.HTTP_200_OK},
    ],
)
def test_get_verses_from_book_id_and_chapter_number_contract(case):
    response = client.get(
        f"/v1/books/{case['book_id']}/chapters/{case['chapter_number']}/verses"
    )

    # status code check
    assert response.status_code == 200

    data = response.json()

    # shape checks
    assert isinstance(data, list)
    assert all(isinstance(item, dict) for item in data)

    # key + type checks
    for item in data:
        assert "verse_id" in item
        assert "verse_number" in item
        assert "verse_text" in item

        assert isinstance(item["verse_id"], int)
        assert isinstance(item["verse_number"], int)
        assert isinstance(item["verse_text"], str)

    # ordering check
    orders = [item["verse_number"] for item in data]
    assert orders == sorted(orders)


# will want to remove the hardcoded verse ids
@pytest.mark.parametrize(
    "case",
    [
        {
            "verse_id": get_verse_by_text(client, "TEST ROOT: No children"),
            "status_code": status.HTTP_200_OK,
        },
        {
            "verse_id": get_verse_by_text(client, "TEST ROOT: Dense at layers 0-2"),
            "status_code": status.HTTP_200_OK,
        },
        {
            "verse_id": get_verse_by_text(
                client, "TEST ROOT: Dense at layers 0-1; sparse as layer 2"
            ),
            "status_code": status.HTTP_200_OK,
        },
        {
            "verse_id": get_verse_by_text(client, "TEST ROOT: 1 child"),
            "status_code": status.HTTP_200_OK,
        },
        {
            "verse_id": get_verse_by_text(
                client, "TEST ROOT: 3 children, middle has children"
            ),
            "status_code": status.HTTP_200_OK,
        },
        {
            "verse_id": get_verse_by_text(
                client, "TEST ROOT: Chain past depth limit (4 layers)"
            ),
            "status_code": status.HTTP_200_OK,
        },
    ],
)
def test_verse_bfs_contract(case):
    response = get_verse_bfs_response(client, case["verse_id"])

    # status code check
    assert response.status_code == case["status_code"]

    data = response.json()

    # shape checks
    assert isinstance(data, dict)

    assert 1 <= len(data) <= 3, (
        "The number of levels in the response should be between 1 and 3."
    )

    # key + type checks
    for level in data:
        assert isinstance(level, str)

        # Verse list checks
        verse_list = data[level]
        assert isinstance(verse_list, list)

        sorted_verse_list = sorted(
            verse_list,
            key=lambda x: (
                x["book_canonical_order"],
                x["chapter_number"],
                x["verse_number"],
            ),
        )

        assert verse_list == sorted_verse_list, (
            f"Verse list for level {level} is not sorted correctly."
        )

        # Single verse checks
        for verse_dict in verse_list:
            assert isinstance(verse_dict, dict)
            assert "verse_id" in verse_dict
            assert "book_canonical_order" in verse_dict
            assert "book_name" in verse_dict
            assert "chapter_number" in verse_dict
            assert "verse_number" in verse_dict
            assert "verse_text" in verse_dict
            assert "parent_id" in verse_dict
            assert "link_strength" in verse_dict

            assert isinstance(verse_dict["verse_id"], int)
            assert isinstance(verse_dict["book_canonical_order"], int)
            assert isinstance(verse_dict["book_name"], str)
            assert isinstance(verse_dict["chapter_number"], int)
            assert isinstance(verse_dict["verse_number"], int)
            assert isinstance(verse_dict["verse_text"], str)
            assert isinstance(verse_dict["parent_id"], (int, type(None)))
            assert isinstance(verse_dict["link_strength"], (int, type(None)))
