import cv2
from cv2.typing import MatLike
import pathlib
from enum import IntEnum

PATH_TO_MODEL = (
    pathlib.Path(cv2.__file__).parent.absolute() / "data" / "haarcascade_lowerbody.xml"
)
"""
"lowerbody"
"frontalface_default"
"eye"
"""

# compensate for camera direction
# TODO: figure out best value
X_DIRECTION_OFFSET = 0


class Direction(IntEnum):
    LEFT = -1
    CENTER = 0
    RIGHT = 1


clf = cv2.CascadeClassifier(str(PATH_TO_MODEL))


def detect_lowerbody(frame: MatLike) -> Direction | None:
    # TODO: mozna zbytecny
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    legs = clf.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE,
    )

    if len(legs) == 0:
        return None

    # TODO: mozna vybrat ten nejvetsi
    x, _, width, _ = legs[0]
    legs_center_x = x + width // 2

    if target_reached():
        return None

    third_width = frame.shape[1] // 3

    if legs_center_x < (third_width + X_DIRECTION_OFFSET):
        return Direction.LEFT
    elif legs_center_x > third_width * 2:
        return Direction.RIGHT
    else:
        return Direction.CENTER


# TODO: implement
def target_reached() -> bool:
    return False
