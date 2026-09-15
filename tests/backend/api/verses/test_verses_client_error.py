from fastapi.testclient import TestClient
import pytest
from src.api.main import app
from fastapi import status 

client = TestClient(app)


@pytest.mark.parametrize("case", [
    {
        "verse_id": "example string",
        "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT
    },
])
def test_verse_bfs_client_error(case):
    response = client.get(f"/v1/verses/{case['verse_id']}/traversal_results")
    assert response.status_code == case["status_code"]
