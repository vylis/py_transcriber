from deep_translator import GoogleTranslator


def text_translate(text_data: str, language: str) -> dict:
    try:
        # translate text
        result = GoogleTranslator(source="auto", target=language).translate(text_data)

        if result is not None:
            return {
                "original_text": text_data,
                "translated_text": result,
                "language": language,
            }
        else:
            raise Exception("Translation failed")

    except Exception as e:
        print(f"Error occurred during translation: {e}")
        return None
