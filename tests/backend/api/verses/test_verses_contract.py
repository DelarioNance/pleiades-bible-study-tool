from fastapi.testclient import TestClient
import pytest
from src.api.main import app
from fastapi import status 

client = TestClient(app)


@pytest.mark.parametrize("case", [
    {
        "verse_id": 10710, # sparsest possible tree (no neighbors)
        "status_code": status.HTTP_200_OK
    },
    {
        "verse_id": 4129, # densest possible tree (3 neighbors at each level)
        "status_code": status.HTTP_200_OK
    },
])
def test_verse_bfs_contract(case):
    response = client.get(f"/v1/verses/{case['verse_id']}/traversal_results")

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