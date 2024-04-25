import cv2
from cv2.typing import MatLike
import pathlib
from bosdyn.client.math_helpers import SE2Pose, Vec2

PATH_TO_MODEL = (
    pathlib.Path(cv2.__file__).parent.absolute() / "data" / "haarcascade_lowerbody.xml"
)
"""
"lowerbody"
"frontalface_default"
"eye"
"""

clf = cv2.CascadeClassifier(str(PATH_TO_MODEL))


def detect_lowerbody(frame: MatLike) -> SE2Pose | None:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # mozna zbytecny
    legs = clf.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE,
    )

    if len(legs) == 0:
        return None

    x, y, width, height = legs[0]
    legs_center_x = x + width // 2
    legs_center_y = y + height // 2
    X, Y, Z = pixel_to_world(legs_center_x, legs_center_y)  # , depth)
    destination = Vec2(x=X / 1000, y=Y / 1000)  # Převod mm na metry
    se2_pose = SE2Pose(*destination, angle=0)
    return se2_pose


CENTER_X = 1
CENTER_Y = 2
DEPTH = 3
FOCAL_LENGTH = 4


def pixel_to_world(x_pixel, y_pixel, depth=DEPTH):
    X = (x_pixel - CENTER_X) * depth / FOCAL_LENGTH
    Y = (y_pixel - CENTER_Y) * depth / FOCAL_LENGTH
    Z = depth
    return X, Y, Z
