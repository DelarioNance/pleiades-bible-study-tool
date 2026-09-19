from fastapi.testclient import TestClient
import pytest
from src.api.main import app
from fastapi import status 
from tests.backend.api.utils import find_sparsest_verse_id, find_densest_verse_id, get_verse_bfs_response

client = TestClient(app)

# will want to remove the hardcoded verse ids
@pytest.mark.parametrize("case", [
    {
        "verse_id": find_sparsest_verse_id(client),
        "status_code": status.HTTP_200_OK
    },
    {
        "verse_id": find_densest_verse_id(client),
        "status_code": status.HTTP_200_OK
    },
])
def test_verse_bfs_contract(case):
    response = get_verse_bfs_response(client, case["verse_id"])

    # status code check
    assert response.status_code == case["status_code"]

    data = response.json()

    # shape checks
    assert isinstance(data, dict)

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
                x["verse_number"]
            )
        )

        assert verse_list == sorted_verse_list, f"Verse list for level {level} is not sorted correctly."

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