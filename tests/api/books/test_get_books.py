from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_get_books():
    response = client.get("/v1/books")

    # status code check
    assert response.status_code == 200

    data = response.json()

    # shape checks
    assert isinstance(data, list)
    assert all(isinstance(item, dict) for item in data)

    first = data[0]

    # key checks
    assert "id" in first
    assert "name" in first
    assert "order" in first

    # type checks
    assert isinstance(first["id"], int)
    assert isinstance(first["name"], str)
    assert isinstance(first["order"], int)
    
    # minimal correctness check (to validate the DB-API mapping)
    assert first["name"] == "Genesis"
    assert first["order"] == 1