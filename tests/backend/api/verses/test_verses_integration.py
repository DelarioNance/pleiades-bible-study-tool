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
])
def test_verse_bfs_integration(case):
    response = get_verse_bfs_response(client, case["verse_id"])
    data = response.json()

    assert data == case["expected_result"], f"Expected {case['expected_result']}, but got {data}"