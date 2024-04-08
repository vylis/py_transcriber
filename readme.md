# PY_TRANSCRIBER

Record your voice, transcribe it, translate in another language and transform the translation into speech.

## Getting Started

1. **Add Vosk models**: Download your Vosk models [here](https://alphacephei.com/vosk/models) and place them into the `models/` directory.

2. **Install dependencies**: Run `pip install -r requirements.txt` in your terminal to install the necessary dependencies.

3. **Launch the API**: Use the command `uvicorn main:app --reload` to start the application.

## Usage

- **Swagger UI**: Use `localhost:8000/docs` to access the Swagger where you can test the API routes.

- **HTTP files**: Use the HTTP files in the `requests/` directory to test the API routes.

- **Tests**: Run `pytest` in the terminal to execute the tests.
