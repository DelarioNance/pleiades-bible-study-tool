from fastapi.testclient import TestClient
import pytest
from src.api.main import app
from fastapi import status 

client = TestClient(app)


@pytest.mark.parametrize("case", [
    {
        "chapter_id": 1,
        "status_code": status.HTTP_200_OK
    },
    {
        "chapter_id": -999,
        "status_code": status.HTTP_200_OK
    },
    {
        "chapter_id": 1.0,
        "status_code": status.HTTP_200_OK
    }
])
def test_get_verses_from_chapter_id_contract(case):
    response = client.get(f"/v1/chapters/{case['chapter_id']}/verses")

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
        assert "text" in item
        
        assert isinstance(item["id"], int)
        assert isinstance(item["number"], int)
        assert isinstance(item["text"], str)

    # ordering check
    orders = [item["number"] for item in data]
    assert orders == sorted(orders)