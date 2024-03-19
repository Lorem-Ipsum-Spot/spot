import speech_recognition as sr  # type: ignore

# Initialize the recognizer
recognizer = sr.Recognizer()

# Define actions for each command
def come_here():
    print("Jdu sem...")

def forward():
    print("Jdu dopředu...")

def backward():
    print("Jdu dozadu...")

def sit_down():
    print("Sedím...")

def lie_down():
    print("Ležím...")

# Function to process recognized commands using a switch-like approach
def process_command(command):
    actions = {
        "k noze": come_here,
        "dopředu": forward,
        "dozadu": backward,
        "sedni": sit_down,
        "lehni": lie_down
    }
    action = actions.get(command, None)
    if action:
        action()
    else:
        print("Příkaz nerozpoznán")

# Function to listen to microphone input
def listen_microphone():
    with sr.Microphone() as source:
        print("Řekněte něco:")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for noise
        audio = recognizer.listen(source)

    try:
        # Recognize speech using Google Speech Recognition with Czech language
        command = recognizer.recognize_google(audio, language="cs-CZ")
        print("Řekli jste:", command)
        process_command(command.lower())
    except sr.UnknownValueError:
        print("Nerozumím zvuku")
    except sr.RequestError as e:
        print("Nelze požádat o výsledky služby Google Speech Recognition; {0}".format(e))

# Continuous listening loop
while True:
    listen_microphone()
