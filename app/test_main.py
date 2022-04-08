from fastapi.testclient import TestClient
from .main import app


client = TestClient(app)


def test_cambridge():
    response = client.get("/cambridge/")
    assert response.status_code == 200
    assert response.json() == {"response": "No result"}
