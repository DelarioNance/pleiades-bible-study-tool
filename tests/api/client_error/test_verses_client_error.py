import pytest
from fastapi import status
from fastapi.testclient import TestClient

from src.api.main import app
from tests.api.utils import get_verse_bfs_response

client = TestClient(app)


@pytest.mark.parametrize(
    "case",
    [
        {
            "verse_id": "example string",
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
        },
    ],
)
def test_verse_bfs_client_error(case):
    response = get_verse_bfs_response(client, case["verse_id"])
    assert response.status_code == case["status_code"]
