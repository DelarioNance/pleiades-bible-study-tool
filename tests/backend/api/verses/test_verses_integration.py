from fastapi.testclient import TestClient
import pytest
from src.api.main import app
from tests.backend.api.utils import get_verse_bfs_response, get_verse_by_text

client = TestClient(app)

# will want to remove the hardcoded verse ids
@pytest.mark.parametrize("case", [
    {
        "verse_id": get_verse_by_text(client, "TEST ROOT: No children"),
    },
    {
        "verse_id": get_verse_by_text(client, "TEST ROOT: Dense at layers 0-2"),
    },
    {
        "verse_id": get_verse_by_text(client, "TEST ROOT: Dense at layers 0-1; sparse as layer 2"),
    },
    {
        "verse_id": get_verse_by_text(client, "TEST ROOT: 1 child"),
    },
    {
        "verse_id": get_verse_by_text(client, "TEST ROOT: 3 children, middle has children"),
    },
])
def test_verse_bfs_integration(case):
    response = get_verse_bfs_response(client, case["verse_id"])