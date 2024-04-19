import speech_recognition as sr  # type: ignore

# Initialize the recognizer
recognizer = sr.Recognizer()

'''
# Function to process recognized commands
def process_command(command):
    if "noze" in command:
        come_here()
        return

    switch = {
        "dopředu": move_forward,
        "dozadu": move_backward,
        "sedni": sit_down,
        "lehni": lie_down,
        "následuj": follow,
    }
    # Get the function corresponding to the command, or default to command_not_recognized
    command_function = switch.get(command, command_not_recognized)
    # Execute the function
    command_function()


# Command functions
def come_here():
    print("Jdu sem...")


def move_forward():
    print("Jdu dopředu...")


def move_backward():
    print("Jdu dozadu...")


def sit_down():
    print("Sedím...")


def lie_down():
    print("Ležím...")


def follow():
    print("Následuji...")


def command_not_recognized():
    print("Příkaz nerozpoznán")

'''
# Function to listen to microphone input
def listen_microphone()->str:
    with sr.Microphone() as source:
        print("Řekněte něco:")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for noise
        audio = recognizer.listen(source)

    try:
        # Recognize speech using Google Speech Recognition with Czech language
        # ignore the error, the library is poorly type hinted
        command = recognizer.recognize_vosk(audio, language="cs-CZ").lower()
        print("Řekli jste:", command)
        return command #process_command(command)
    except sr.UnknownValueError:
        print("Nerozumím zvuku")
        return "nerozpoznan zvuk"
    #except sr.RequestError as e:
    #    print(f"Nelze požádat o výsledky služby Google Speech Recognition; {e}")
