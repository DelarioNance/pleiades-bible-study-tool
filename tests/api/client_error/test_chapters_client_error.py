import pytest
from fastapi import status
from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


@pytest.mark.parametrize(
    "case",
    [
        {
            "chapter_id": "example string",
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
        },
    ],
)
def test_get_verses_from_chapter_id_client_error(case):
    response = client.get(f"/v1/chapters/{case['chapter_id']}/verses")
    assert response.status_code == case["status_code"]
