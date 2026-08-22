from fastapi.testclient import TestClient
from src.api.main import app
from fastapi import status 
import pytest
from unittest.mock import patch

client = TestClient(app)

@pytest.mark.parametrize("case", [
    {
        "book_id": 1,
        "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
    },
])
def test_get_chapters_from_book_id_server_error(case):
    with patch("src.api.services.book_service.engine.connect", side_effect=Exception("Database error")):
        response = client.get(f"/v1/books/{case['book_id']}/chapters")
        assert response.status_code == case["status_code"]


@pytest.mark.parametrize("case", [
    {
        "book_id": 1,
        "chapter_number": 1,
        "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
    },
])
def test_get_verses_from_book_id_and_chapter_number_server_error(case):
    with patch("src.api.services.chapter_service.engine.connect", side_effect=Exception("Database error")):
        response = client.get(f"/v1/books/{case['book_id']}/chapters/{case['chapter_number']}/verses")
        assert response.status_code == case["status_code"]
