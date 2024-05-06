import pathlib
from enum import IntEnum

import cv2
import numpy as np

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
    """Enum for direction."""

    LEFT = -1
    CENTER = 0
    RIGHT = 1


clf = cv2.CascadeClassifier(str(PATH_TO_MODEL))


def detect_lowerbody(frame: np.ndarray) -> Direction | None:
    """
    Detect the lower body in the frame.

    Parameters
    ----------
    frame : MatLike
        The frame to detect the lower body in.

    Returns
    -------
    Direction | None
        The direction of the lower body or None if not detected.

    """
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
