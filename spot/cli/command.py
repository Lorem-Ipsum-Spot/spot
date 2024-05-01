from enum import Enum


class Command(Enum):
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


commands_map = {
    "dopředu": Command.FORWARD,
    "dozadu": Command.BACKWARD,
    "sedni": Command.SIT,
    "zvedni": Command.STAND,
    "lehni": Command.SIT,
    "stoupni": Command.STAND,
    "následuj": Command.FOLLOWING,
    "stůj": Command.STOP,
    "otoc vlevo": Command.ROTATE_LEFT,
    "otoc vpravo": Command.ROTATE_RIGHT,
    "doleva": Command.LEFT,
    "doprava": Command.RIGHT,
}


def str_to_command(command: str) -> Command | None:
    return commands_map.get(command)
