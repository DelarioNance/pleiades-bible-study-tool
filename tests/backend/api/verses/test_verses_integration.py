from fastapi.testclient import TestClient
import pytest
from src.api.main import app
from tests.backend.api.utils import get_verse_bfs_response, get_verse_by_text
from tests.backend.api.verses.test_verses_integration_correct_data import expected_bfs_results

client = TestClient(app)

# will want to remove the hardcoded verse ids
@pytest.mark.parametrize("case", [
    {
        "verse_id": get_verse_by_text(client, "TEST ROOT: No children"),
        "expected_result": expected_bfs_results["TEST ROOT: No children"]
    },
    {
        "verse_id": get_verse_by_text(client, "TEST ROOT: Dense at layers 0-2"),
        "expected_result": expected_bfs_results["TEST ROOT: Dense at layers 0-2"]
    },
    {
        "verse_id": get_verse_by_text(client, "TEST ROOT: Dense at layers 0-1; sparse as layer 2"),
        "expected_result": expected_bfs_results["TEST ROOT: Dense at layers 0-1; sparse as layer 2"]
    },
    {
        "verse_id": get_verse_by_text(client, "TEST ROOT: 1 child"),
        "expected_result": expected_bfs_results["TEST ROOT: 1 child"]
    },
    {
        "verse_id": get_verse_by_text(client, "TEST ROOT: 3 children, middle has children"),
        "expected_result": expected_bfs_results["TEST ROOT: 3 children, middle has children"]
    },
    {
        "verse_id": get_verse_by_text(client, "TEST ROOT: Chain past depth limit (4 layers)"),
        "expected_result": expected_bfs_results["TEST ROOT: Chain past depth limit (4 layers)"]
    }
])
def test_verse_bfs_integration(case):
    response = get_verse_bfs_response(client, case["verse_id"])
    data = response.json()

    expected_result = case["expected_result"]
    normalized_data = _normalize_response_json(data, expected_result)

    assert normalized_data == expected_result, f"Expected {expected_result}, but got {normalized_data}"


def _normalize_response_json(data, expected):
    verse_id_to_verse_text = {verse["verse_id"]: verse["verse_text"] for level in data.values() for verse in level}
    filtered_verse_fields = {field for verses in expected.values() for verse in verses for field in verse.keys()}

    return {
        level: [_normalize_verse(verse, verse_id_to_verse_text, filtered_verse_fields) for verse in verses]
        for level, verses in data.items()
    }


def _normalize_verse(verse, verse_id_to_verse_text, filtered_verse_fields):
    verse_with_parent_text = {**verse, "parent_text": verse_id_to_verse_text.get(verse["parent_id"], None)}
    return {
        field: verse_with_parent_text[field]
        for field in filtered_verse_fields
    }