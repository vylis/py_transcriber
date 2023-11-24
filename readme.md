PYTHON TRANSCRIBER

- add your vosk models into the models/ folder
- install requirements using ``pip install -r requirements.txt`
- launch the api using `uvicorn main:app --reload`
- you can record your voice with requests/record_module.http or with the route /audio_record
- get the audio_data of your recording in output/recorded_audio_data.txt
- you can transcribe with requests/speech_recognition_language.http or with the route speech_recogniton
- you can record and transcribe at the same time with requests/record_and_transcribe or with the route record_and_transcribe
