import pathlib
from enum import IntEnum

import cv2
from cv2.typing import MatLike

detection_type = "lowerbody"
detection_type = "frontalface_default"
detection_type = "eye"

cascade_path = (
    pathlib.Path(cv2.__file__).parent.absolute()
    / "data"
    / f"haarcascade_{detection_type}.xml"
)

clf = cv2.CascadeClassifier(str(cascade_path))


class Direction(IntEnum):
    LEFT = -1
    CENTER = 0
    RIGHT = 1


def detect_lowerbody(frame: MatLike) -> Direction | None:
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect areas
    areas = clf.detectMultiScale(
        frame,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE,
    )

    if not areas:
        return None

    # Find the biggest area
    x, y, width, height = max(areas, key=lambda x: x[2] * x[3])

    # Draw a rectangle around the area
    cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 245, 0), 2)

    x_center = x + width // 2
    third_width = frame.shape[1] // 3

    if x_center < third_width:
        return Direction.LEFT

    if x_center > third_width * 2:
        return Direction.RIGHT

    return None if target_reached() else Direction.CENTER


def target_reached() -> bool:
    return False
