import speech_recognition as sr

# Initialize the recognizer
recognizer = sr.Recognizer()


# Function to listen to microphone input
def listen_microphone() -> str | None:
    """
    Listen to the microphone and return the recognized speech as a string.

    Returns
    -------
        str: The recognized speech.
        None: If the speech could not be recognized.

    """
    with sr.Microphone() as source:
        print("Řekněte něco:")
        recognizer.adjust_for_ambient_noise(source)
        # TODO: look into using `listen_background`
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_vosk(audio, language="cs-CZ").lower()

    except sr.UnknownValueError:
        print("Nerozumím zvuku")
        return None
    else:
        print("Řekli jste:", command)
        return command
