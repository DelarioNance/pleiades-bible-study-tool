from fastapi.testclient import TestClient
import pytest
from src.api.main import app

client = TestClient(app)


@pytest.mark.parametrize("case", [
    {
        "book_id": 1,
        "chapter_id": 1,
    }
])
def test_get_verses_contract(case):
    response = client.get(f"/v1/books/{case['book_id']}/chapters/{case['chapter_id']}/verses")

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