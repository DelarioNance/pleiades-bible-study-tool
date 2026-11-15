import pytest
from fastapi import status
from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


@pytest.mark.parametrize(
    "case",
    [
        {"book_id": 1, "status_code": status.HTTP_200_OK},
        {"book_id": -999, "status_code": status.HTTP_200_OK},
        {"book_id": 1.0, "status_code": status.HTTP_200_OK},
    ],
)
def test_get_chapters_from_book_id_contract(case):
    response = client.get(f"/v1/books/{case['book_id']}/chapters")

    # status code check
    assert response.status_code == case["status_code"]

    data = response.json()

    # shape checks
    assert isinstance(data, list)
    assert all(isinstance(item, dict) for item in data)

    # key + type checks
    for item in data:
        assert "chapter_id" in item
        assert "chapter_number" in item

        assert isinstance(item["chapter_id"], int)
        assert isinstance(item["chapter_number"], int)

    # ordering check
    orders = [item["chapter_number"] for item in data]
    assert orders == sorted(orders)
