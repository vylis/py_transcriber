from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pathlib import Path
from dotenv import load_dotenv

from src.audio_recorder import audio_record
from src.speech_recognizer import speech_recognition

from payloads.audio_record_payload import audio_record_payload
from payloads.speech_recognition_payload import speech_recognition_payload
from payloads.record_and_transcribe_payload import record_and_transcribe_payload

load_dotenv(Path(__file__).parent / ".env")


class AudioRecordModel(BaseModel):
    file_name: str = Query(..., description="Name of the file to be saved")
    duration: int = Query(..., description="Duration of the recording")
    model_config = {"json_schema_extra": {"examples": [audio_record_payload]}}


class SpeechRecognitionModel(BaseModel):
    audio_data: str = Query(..., description="Audio encoded in base64")
    language: str = Query(..., description="Locale language of the audio")
    model_config = {"json_schema_extra": {"examples": [speech_recognition_payload]}}


class RecordAndTranscribeModel(BaseModel):
    file_name: str = Query(..., description="Name of the file to be saved")
    duration: int = Query(..., description="Duration of the recording")
    language: str = Query(..., description="Locale language of the audio")
    model_config = {"json_schema_extra": {"examples": [record_and_transcribe_payload]}}


app = FastAPI(
    swagger_ui_parameters=[
        {"name": "validatorUrl", "value": None},
    ]
)


@app.get("/")
async def root():
    return {"message": "Goodnight World!"}


# audio_record
@app.post("/audio_record")
async def audio_record_route(input: AudioRecordModel):
    try:
        response = audio_record(input.file_name, input.duration)

        if response:
            return JSONResponse(
                status_code=200,
                content={"message": f"Audio recorded and saved to {response}"},
            )
        else:
            return JSONResponse(status_code=400, content={"error": "Recording failed."})
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})


# speech_recognition
@app.post("/speech_recognition")
async def speech_recognition_route(input: SpeechRecognitionModel):
    try:
        response = speech_recognition(input.audio_data, input.language)
        return JSONResponse(status_code=200, content=response)
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})


@app.post("/record_and_transcribe")
async def record_and_transcribe_route(input: RecordAndTranscribeModel):
    try:
        # record audio
        audio_data_path = audio_record(input.file_name, input.duration)

        print(audio_data_path)

        if audio_data_path:
            # read audio data
            with open(audio_data_path, "rb") as audio_file:
                audio_data = audio_file.read()

            # transcribe audio data
            response = speech_recognition(audio_data, input.language)

            if response:
                return JSONResponse(status_code=200, content=response)
            else:
                return JSONResponse(
                    status_code=400, content={"error": "Transcription failed."}
                )
        else:
            return JSONResponse(status_code=400, content={"error": "Recording failed."})
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
