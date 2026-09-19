from fastapi.testclient import TestClient
from src.api.main import app
from fastapi import status 
import pytest
from unittest.mock import patch

from tests.backend.api.utils import get_verse_bfs_response

client = TestClient(app)


@pytest.mark.parametrize("case", [
    {
        "verse_id": 1,
        "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
    },
])
def test_verse_bfs_server_error(case):
    with patch("src.api.services.verse_service.engine.connect", side_effect=Exception("Database error")):
        response = get_verse_bfs_response(client, case["verse_id"])
        assert response.status_code == case["status_code"]
