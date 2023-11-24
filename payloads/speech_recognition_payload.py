from pathlib import Path


with open(Path(__file__).parent / "audio_data_example.txt") as f:
    audio_data_example = f.read()

speech_recognition_payload = {"audio_data": audio_data_example, "language": "en-us"}
