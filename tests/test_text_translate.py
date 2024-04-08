from fastapi.testclient import TestClient
from main import app
from payloads.text_translate_payload import text_translate_payload

client = TestClient(app)


def test_text_translate():
    response = client.post("/text_translate", json=text_translate_payload)
    assert response.status_code == 200
