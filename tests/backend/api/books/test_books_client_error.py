from fastapi.testclient import TestClient
import pytest
from src.api.main import app
from fastapi import status 

client = TestClient(app)


@pytest.mark.parametrize("case", [
    {
        "book_id": "example string",
        "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT
    },
])
def test_get_chapters_from_book_id_client_error(case):
    response = client.get(f"/v1/books/{case['book_id']}/chapters")
    assert response.status_code == case["status_code"]



@pytest.mark.parametrize("case", [
    {
        "book_id": "example string",
        "chapter_number": 1,
        "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT
    },
    {
        "book_id": 1,
        "chapter_number": "example string",
        "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT
    },
])
def test_get_verses_from_book_id_and_chapter_number_client_error(case):
    response = client.get(f"/v1/books/{case['book_id']}/chapters/{case['chapter_number']}/verses")
    assert response.status_code == case["status_code"]
