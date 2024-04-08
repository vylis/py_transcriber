import os
from datetime import datetime
from gtts import gTTS


def text_to_speech(text_data: str, language: str) -> None:
    try:
        # create folder
        os.makedirs("./output/translated", exist_ok=True)

        # text to speech
        tts = gTTS(text=text_data, lang=language)

        # get current date
        current_date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

        # save translated  to wav file
        file_path = f"./output/translated/{language}_translated_{current_date}.wav"
        tts.save(file_path)

        print(f"Audio translated saved to {file_path}")
        return file_path
    except Exception as e:
        print(f"Error occurred during text to speech: {e}")
        return None
