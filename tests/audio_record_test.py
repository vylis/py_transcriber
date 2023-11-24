from fastapi.testclient import TestClient
from main import app
from payloads.audio_record_payload import audio_record_payload

client = TestClient(app)


def test_audio_record():
    response = client.post("/audio_record", json=audio_record_payload)
    assert response.status_code == 200
