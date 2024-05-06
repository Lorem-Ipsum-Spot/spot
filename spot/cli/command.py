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
    FOLLOWING_PAUSED = 7
    STOP = 8
    ROTATE_LEFT = 9
    ROTATE_RIGHT = 10


_COMMANDS_MAP = {
    "dozadu": Command.BACKWARD,
    "následuj": Command.FOLLOWING,
    "dopředu": Command.FORWARD,
    "vlevo": Command.LEFT,
    "lehnout": Command.SIT,
    "vpravo": Command.RIGHT,
    "otočit vlevo": Command.ROTATE_LEFT,
    "otočit vpravo": Command.ROTATE_RIGHT,
    "sednout": Command.SIT,
    "stát": Command.STAND,
    "stop": Command.STOP,
}


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
    print(command)
    return _COMMANDS_MAP.get(command)
