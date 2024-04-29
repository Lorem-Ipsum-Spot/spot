from typing import Callable
import speech_recognition as sr

from spot.cli.stopper import Stop


class Listener:
    recognizer: sr.Recognizer
    microphone: sr.Microphone
    stop_function: Callable[[bool], None]

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def run(self, stopper: Stop, callback: Callable[[str], None]):
        self.stopper = stopper

        def callback_wrapper(recognizer: sr.Recognizer, audio: sr.AudioData) -> None:
            if self.stopper.flag:
                self.stop_function(True)
                return

            try:
                text = recognizer.recognize_vosk(audio, language="cs-CZ").lower()
            except sr.UnknownValueError:
                return

            callback(text)

        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)

        self.stop_function = self.recognizer.listen_in_background(
            source, callback_wrapper
        )
