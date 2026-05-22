from fastapi.testclient import TestClient
from src.api.main import app
from fastapi import status 
from unittest.mock import patch
import pytest

client = TestClient(app)


@pytest.mark.parametrize("case", [
    {
        "book_id": 1,
        "chapter_number": 1,
        "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
    },
])
def test_get_chapters_verses_error(case):
    with patch("src.api.main.engine.connect", side_effect=Exception("Database error")):
        response = client.get(f"/v1/books/{case['book_id']}/chapters/{case['chapter_number']}/verses")
        assert response.status_code == case["status_code"]
