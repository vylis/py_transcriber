import json
from pathlib import Path
from datetime import datetime
from src.vosk_module import VoskModule


def get_model_path(language: str) -> str:
    # get model per language
    models_dir = Path("./models")
    model_files = list(models_dir.glob(f"vosk-model-small-{language}-*"))
    # get latest model
    latest_model = max(
        model_files, key=lambda x: x.stem.split(f"vosk-model-small-{language}-")[1]
    )
    return str(latest_model.absolute()) if latest_model else None


def speech_recognition(audio_data: str, language: str) -> dict:
    try:
        # get model
        model_path = get_model_path(language)
        print("Currently using model:", model_path)

        if model_path is None:
            raise Exception(f"Model not found for language {language}")

        # get current date
        current_date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

        # save audio to wav file
        output_wav_file = f"./output/{language}_audio_data_to_wav_{current_date}.wav"
        VoskModule.save_audio_data_to_wav(audio_data, output_wav_file)

        # transcribe audio data
        result = VoskModule.transcribe(model_path, audio_data)
        print("transcribe_audio_data", result)

        if result is not None:
            result_json = json.loads(result)
            confidence = result_json["result"][0]["conf"]
            word = result_json["text"]

            return {"confidence": confidence, "word": word, "language": language}
        else:
            raise Exception("Speech recognition failed")

    except Exception as e:
        print(f"Error occurred during speech recognition: {e}")
        return None
