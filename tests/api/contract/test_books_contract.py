from fastapi.testclient import TestClient

from src.api.main import app

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
        assert "book_id" in item
        assert "book_name" in item
        assert "book_order" in item

        assert isinstance(item["book_id"], int)
        assert isinstance(item["book_name"], str)
        assert isinstance(item["book_order"], int)

    # ordering check
    orders = [item["book_order"] for item in data]
    assert orders == sorted(orders)
