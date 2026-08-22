from fastapi.testclient import TestClient
from src.api.main import app
from fastapi import status 
import pytest
from unittest.mock import patch

client = TestClient(app)


@pytest.mark.parametrize("case", [
    {
        "chapter_id": 1,
        "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
    },
])
def test_get_verses_from_chapter_id_server_error(case):
    with patch("src.api.services.chapter_service.engine.connect", side_effect=Exception("Database error")):
        response = client.get(f"/v1/chapters/{case['chapter_id']}/verses")
        assert response.status_code == case["status_code"]
