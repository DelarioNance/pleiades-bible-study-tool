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
def test_get_chapters_invalid_input(case):
    response = client.get(f"/v1/books/{case['book_id']}/chapters")
    assert response.status_code == case["status_code"]
