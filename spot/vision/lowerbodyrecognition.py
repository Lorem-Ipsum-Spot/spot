import cv2
import pathlib

import numpy as np


# cascade_path = pathlib.Path(cv2.__file__).parent.absolute( )/ "data/haarcascade_eye.xml"
cascade_path = (
    pathlib.Path(cv2.__file__).parent.absolute() / "data/haarcascade_lowerbody.xml"
)
# cascade_path = pathlib.Path(cv2.__file__).parent.absolute( )/ "data/haarcascade_frontalface_default.xml"

clf = cv2.CascadeClassifier(str(cascade_path))


def detect_faces(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = clf.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE,
    )

    areas = [w * h for x, y, w, h in faces]
    if len(areas) > 0:
        i_biggest = np.argmax(areas)
        biggest = faces[i_biggest]
        x, y, width, height = biggest
        cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 245, 0), 2)
        x_center = x + width // 2

        if x_center < (frame.shape[1] // 3):
            return -1
        elif x_center > (frame.shape[1] // 3) and x_center < frame.shape[1] // 3 * 2:
            return 0
        else:
            return 1
    return 0
