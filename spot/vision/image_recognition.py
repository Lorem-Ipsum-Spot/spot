import pathlib
from enum import IntEnum

import cv2
import numpy as np
from paddleocr import PaddleOCR, draw_ocr

def detect_text(frame,ocr):

    #ocr = PaddleOCR(use_angle_cls=True, lang='en')  # Nastavení jazyka a detekce orientace textu
    result = ocr.ocr(frame, cls=True)
    for line in result:
        if line != None:
            points = line[0][0]
            toplx = points[3][0]
            toply = points[3][1]
            botdx = points[1][0]
            botdy = points[1][1]
            delka = int(points[1][0]) - int(points[0][0])
            text = line[0][1]
            if text[0] == "FOLLOW" or text[0] == "follow":
                print(f"x: {toplx} y: {toply}")
                cv2.rectangle(frame,(int(toplx),int(toply)),(int(botdx),int(botdy)),(255,245,0),2)
                return int(toplx),int(delka)
        return int(-1), int(1000)
    #         cv2.imshow("follow", frame)
    #     if cv2.waitKey(1) == ord("q"):
    #         break
    # cv2.destroyAllWindows()

# TODO: implement
def target_reached() -> bool:
    return False

