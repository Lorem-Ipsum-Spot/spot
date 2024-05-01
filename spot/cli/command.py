from enum import StrEnum


class Command(StrEnum):
    LEFT = "left"
    RIGHT = "right"
    FORWARD = "forward"
    BACKWARD = "backward"
    STAND = "stand"
    SIT = "sit"
    STOP = "stop"
    FOLLOWING = "following"


commands_map = {
    "dopředu": Command.FORWARD,
    "dozadu": Command.BACKWARD,
    "sedni": Command.STAND,
    "lehni": Command.LEFT,
    "stoupni": Command.RIGHT,
    "následuj": Command.FOLLOWING,
    "stůj": Command.STOP,
}


def str_to_command(command: str) -> Command | None:
    return commands_map.get(command)
