import speech_recognition as sr

# Initialize the recognizer
recognizer = sr.Recognizer()


# Function to listen to microphone input
def listen_microphone() -> str | None:
    with sr.Microphone() as source:
        print("Řekněte něco:")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for noise
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_vosk(audio, language="cs-CZ").lower()
        print("Řekli jste:", command)
        return command
    except sr.UnknownValueError:
        print("Nerozumím zvuku")
        return None
