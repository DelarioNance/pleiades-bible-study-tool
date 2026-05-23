from fastapi.testclient import TestClient
from src.api.main import app
from fastapi import status 
import pytest

client = TestClient(app)


def test_get_books_contract():
    response = client.get("/v1/books")

    # status code check
    assert response.status_code == 200

    data = response.json()

    # shape checks
    assert isinstance(data, list)
    assert all(isinstance(item, dict) for item in data)

    # key + type checks
    for item in data:
        assert "id" in item
        assert "name" in item
        assert "order" in item

        assert isinstance(item["id"], int)
        assert isinstance(item["name"], str)
        assert isinstance(item["order"], int)

    # ordering check
    orders = [item["order"] for item in data]
    assert orders == sorted(orders)


@pytest.mark.parametrize("case", [
    {
        "book_id": 1,
        "status_code": status.HTTP_200_OK
    },
    {
        "book_id": -999,
        "status_code": status.HTTP_200_OK
    },
    {
        "book_id": 1.0,
        "status_code": status.HTTP_200_OK
    }
])
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
        assert "id" in item
        assert "number" in item
        
        assert isinstance(item["id"], int)
        assert isinstance(item["number"], int)

    # ordering check
    orders = [item["number"] for item in data]
    assert orders == sorted(orders)


@pytest.mark.parametrize("case", [
    {
        "book_id": 1,
        "chapter_number": 1,
        "status_code": status.HTTP_200_OK
    },
    {
        "book_id": -999,
        "chapter_number": 1,
        "status_code": status.HTTP_200_OK
    },
    {
        "book_id": 1.0,
        "chapter_number": 1,
        "status_code": status.HTTP_200_OK
    }
])
def test_get_verses_from_book_id_and_chapter_number_contract(case):
    response = client.get(f"/v1/books/{case['book_id']}/chapters/{case['chapter_number']}/verses")

    # status code check
    assert response.status_code == 200

    data = response.json()

    # shape checks
    assert isinstance(data, list)
    assert all(isinstance(item, dict) for item in data)

    # key + type checks
    for item in data:
        assert "id" in item
        assert "number" in item
        assert "text" in item

        assert isinstance(item["id"], int)
        assert isinstance(item["number"], int)
        assert isinstance(item["text"], str)

    # ordering check
    orders = [item["number"] for item in data]
    assert orders == sorted(orders)