import speech_recognition as sr  # type: ignore

# Initialize the recognizer
recognizer = sr.Recognizer()


# Function to listen to microphone input
def listen_microphone()->str:
    with sr.Microphone() as source:
        print("Řekněte něco:")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for noise
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_vosk(audio, language="cs-CZ").lower()
        print("Řekli jste:", command)
        return command #process_command(command)
    except sr.UnknownValueError:
        print("Nerozumím zvuku")
        return "nerozpoznan zvuk"
