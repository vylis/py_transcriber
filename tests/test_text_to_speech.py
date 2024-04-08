from fastapi.testclient import TestClient
from main import app
from payloads.text_to_speech_payload import text_to_speech_payload

client = TestClient(app)


def test_text_to_speech():
    response = client.post("/text_to_speech", json=text_to_speech_payload)
    assert response.status_code == 200
