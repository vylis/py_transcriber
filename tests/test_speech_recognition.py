from fastapi.testclient import TestClient
from main import app
from payloads.speech_recognition_payload import speech_recognition_payload

client = TestClient(app)


def test_speech_recognition():
    response = client.post("/speech_recognition", json=speech_recognition_payload)
    assert response.status_code == 200
