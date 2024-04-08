from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.audio_recorder import audio_record
from src.speech_recognizer import speech_recognition
from src.text_translater import text_translate
from src.text_to_speech import text_to_speech

from payloads.audio_record_payload import audio_record_payload
from payloads.speech_recognition_payload import speech_recognition_payload
from payloads.record_and_translate_payload import record_and_translate_payload
from payloads.text_translate_payload import text_translate_payload
from payloads.text_to_speech_payload import text_to_speech_payload


class AudioRecordModel(BaseModel):
    duration: int = Query(..., description="Duration of the recording")
    model_config = {"json_schema_extra": {"examples": [audio_record_payload]}}


class SpeechRecognitionModel(BaseModel):
    audio_data: str = Query(..., description="Audio encoded in base64")
    language: str = Query(..., description="Locale language of the audio")
    model_config = {"json_schema_extra": {"examples": [speech_recognition_payload]}}


class TextTranslateModel(BaseModel):
    text_data: str = Query(..., description="Text data to be translated")
    language: str = Query(..., description="Locale language of the text")
    model_config = {"json_schema_extra": {"examples": [text_translate_payload]}}


class TextToSpeechModel(BaseModel):
    text_data: str = Query(..., description="Text data to be converted to speech")
    language: str = Query(..., description="Locale language of the text")
    model_config = {"json_schema_extra": {"examples": [text_to_speech_payload]}}


class RecordAndTranscribeModel(BaseModel):
    duration: int = Query(..., description="Duration of the recording")
    language: str = Query(..., description="Locale language of the audio")
    target_language: str = Query(..., description="Target language for translation")
    model_config = {"json_schema_extra": {"examples": [record_and_translate_payload]}}


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
        response = audio_record(input.duration)

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


# text_translate
@app.post("/text_translate")
async def text_translate_route(input: TextTranslateModel):
    try:
        response = text_translate(input.text_data, input.language)
        return JSONResponse(status_code=200, content=response)
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})


# text_to_speech
@app.post("/text_to_speech")
async def text_to_speech_route(input: TextToSpeechModel):
    try:
        response = text_to_speech(input.text_data, input.language)
        return JSONResponse(status_code=200, content=response)
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})


# record_and_translate
@app.post("/record_and_translate")
async def record_and_translate_route(input: RecordAndTranscribeModel):
    try:
        # record audio
        audio_data_path = audio_record(input.duration)

        if audio_data_path:
            # read audio data
            with open(audio_data_path, "rb") as audio_file:
                audio_data = audio_file.read()

            # transcribe audio data
            response = speech_recognition(audio_data, input.language)
            response_text = response["word"]

            if response:
                # translate the transcribed text
                translated = text_translate(response_text, input.target_language)
                translated_text = translated["translated_text"]

                # convert the translated text to speech
                speech_response = text_to_speech(translated_text, input.target_language)

                return JSONResponse(
                    status_code=200,
                    content={
                        "recognized": response,
                        "translated": translated_text,
                        "speech": speech_response,
                    },
                )
            else:
                return JSONResponse(
                    status_code=400, content={"error": "Transcription failed."}
                )
        else:
            return JSONResponse(status_code=400, content={"error": "Recording failed."})
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
