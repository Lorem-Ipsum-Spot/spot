from collections.abc import Callable

from speech_recognition import AudioData, Microphone, Recognizer, UnknownValueError

from spot.cli.stopper import Stop


class Listener:
    """A class to listen for speech commands."""

    recognizer: Recognizer
    microphone: Microphone
    stop_function: Callable[[bool], None]
    keywords: list[tuple[str, float]]

    def __init__(self, keywords: list[tuple[str, float]]) -> None:
        """
        Initialize the Listener object.

        Parameters
        ----------
        keywords:
            List of (keyword, weight) pairs. Weight should be between

        """
        self.recognizer = Recognizer()
        self.microphone = Microphone()
        self.keywords = keywords

    def run(self, stopper: Stop, callback: Callable[[str], None]) -> None:
        """
        Start listening for speech commands.

        Parameters
        ----------
        stopper : Stop
            The Stop object to monitor for stop request.
        callback : Callable[[str], None]
            The callback function to call when a speech is recognized.

        """
        self.stopper = stopper

        def callback_wrapper(recognizer: Recognizer, audio: AudioData) -> None:
            if self.stopper.flag:
                self.stop_function(True)
                return

            try:
                text = recognizer.recognize_sphinx(
                    audio,
                    language="en-US",
                    keyword_entries=self.keywords,
                ).lower()

                callback(text)
            except UnknownValueError:
                print("Nothing recognized")

        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)

        self.stop_function = self.recognizer.listen_in_background(
            source,
            callback_wrapper,
        )
