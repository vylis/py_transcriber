import vosk
import wave
import base64


class VoskModule:
    # disable vosk logs
    vosk.SetLogLevel(-1)

    @staticmethod
    def save_audio_data_to_wav(audio_data: str, file_path: str):
        try:
            # decode base64 audio_data
            wav_audio = base64.b64decode(audio_data)

            # set wav file parameters and save the audio
            with wave.open(file_path, "wb") as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(44100)
                wav_file.writeframes(wav_audio)
        except Exception as e:
            print(f"Error occurred while saving audio: {e}")

    @staticmethod
    def transcribe(model_path: str, audio_data: str):
        try:
            # decode base64 audio_data
            audio = base64.b64decode(audio_data)

            # create recognizer
            recognizer = vosk.KaldiRecognizer(vosk.Model(model_path), 44100)

            recognizer.AcceptWaveform(audio)
            recognizer.SetWords(True)
            recognizer.SetPartialWords(True)

            # get final result
            result = recognizer.FinalResult()

            return result
        except Exception as e:
            print(f"Error occurred while transcribing audio: {e}")
            return None
