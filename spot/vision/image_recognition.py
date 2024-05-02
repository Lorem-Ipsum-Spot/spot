import pathlib
from enum import IntEnum

import cv2
import numpy as np
from paddleocr import PaddleOCR, draw_ocr

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


def detect_text(frame):
    ocr = PaddleOCR(
        use_angle_cls=True, lang="en"
    )  # Nastavení jazyka a detekce orientace textu
    while True:
        result = ocr.ocr(frame, cls=True)
        for line in result:
            if line != None:
                points = line[0][0]
                toplx = points[3][0]
                toply = points[3][1]
                botdx = points[1][0]
                botdy = points[1][1]
                print(points[0])
                print(points[3])
                text = line[0][1]
                if text[0] == "FOLLOW" or text[0] == "follow":
                    cv2.rectangle(
                        frame,
                        (int(toplx), int(toply)),
                        (int(botdx), int(botdy)),
                        (255, 245, 0),
                        2,
                    )
            cv2.imshow("Faces", frame)
        if cv2.waitKey(1) == ord("q"):
            break
    cv2.destroyAllWindows()


                        (int(toplx), int(toply)),
                        (int(botdx), int(botdy)),
                        (255, 245, 0),
                        2,
                    )
            cv2.imshow("Faces", frame)
        if cv2.waitKey(1) == ord("q"):
            break
    cv2.destroyAllWindows()


# TODO: implement
def target_reached() -> bool:
    return False
