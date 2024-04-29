import speech_recognition as sr

recognizer = sr.Recognizer()


def listen_microphone() -> str | None:
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        # TODO: look into using `listen_background`
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_vosk(audio, language="cs-CZ").lower()
    except sr.UnknownValueError:
        return None
