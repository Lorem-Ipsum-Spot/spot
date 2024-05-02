from enum import Enum


class Command(Enum):
    """Enum representing different commands that can be executed."""

    LEFT = 0
    RIGHT = 1
    FORWARD = 2
    BACKWARD = 3
    STAND = 4
    SIT = 5
    FOLLOWING = 6
    STOP = 7
    ROTATE_LEFT = 8
    ROTATE_RIGHT = 9


_COMMANDS_MAP = {
    "backward": Command.BACKWARD,
    "follow": Command.FOLLOWING,
    "forward": Command.FORWARD,
    "left": Command.LEFT,
    "lie": Command.SIT,
    "right": Command.RIGHT,
    "rotate left": Command.ROTATE_LEFT,
    "rotate right": Command.ROTATE_RIGHT,
    "sit": Command.SIT,
    "stand": Command.STAND,
    "stop": Command.STOP,
}

# Keywords for speech recognition
KEYWORDS = [(command, 1e-15) for command in _COMMANDS_MAP]


def str_to_command(command: str) -> Command | None:
    """
    Convert a string to a Command.

    Parameters
    ----------
    command : str
        The string to convert.

    Returns
    -------
    Command | None
        The Command object or None if the command is not recognized.

    """
    return _COMMANDS_MAP.get(command)
