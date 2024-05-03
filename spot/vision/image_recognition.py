import pathlib
from enum import IntEnum

import cv2
import numpy as np
from paddleocr import PaddleOCR, draw_ocr

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


# TODO: implement
def target_reached() -> bool:
    return False
