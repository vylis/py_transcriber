import base64
import pyaudio
import wave
import time
from datetime import datetime


def audio_record(file_name: str, duration: int) -> str:
    try:
        # record parameters
        audio = pyaudio.PyAudio()
        format_ = pyaudio.paInt16
        channels = 1
        rate = 44100
        chunk = 1024

        # record audio
        stream = audio.open(
            format=format_,
            channels=channels,
            rate=rate,
            input=True,
            frames_per_buffer=chunk,
        )

        frames = []
        start_time = time.time()

        print("Recording audio...")
        while (time.time() - start_time) < duration:
            data = stream.read(chunk)
            frames.append(data)

        stream.stop_stream()
        stream.close()

        print("Recording complete.")

        if len(frames) == 0:
            raise ValueError("No audio frames recorded.")

        # get current date
        current_date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

        # save audio to wav file
        file_path = f"./output/{file_name}_{current_date}.wav"
        with wave.open(file_path, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(audio.get_sample_size(format_))
            wf.setframerate(rate)
            wf.writeframes(b"".join(frames))

        # encode audio to base64
        with open(file_path, "rb") as wav_file:
            audio_bytes = wav_file.read()
            encoded_audio = base64.b64encode(audio_bytes).decode("utf-8")

        # save audio data to txt file
        output_path = f"./output/{file_name}_{current_date}_data.txt"
        with open(output_path, "w") as output_file:
            output_file.write(encoded_audio)

        print(f"Audio data saved to {output_path}")
        return output_path

    except Exception as e:
        print(f"Error occurred while recording audio: {e}")
        return None
