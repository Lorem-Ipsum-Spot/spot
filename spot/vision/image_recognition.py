import pathlib
from enum import IntEnum

import cv2
import numpy as np
from paddleocr import PaddleOCR, draw_ocr


ocr = PaddleOCR(
    use_angle_cls=True, lang="en"
)  # Nastavení jazyka a detekce orientace textu


def detect_text(frame: MatLike) -> tuple[int, int] | None:
    # ocr = PaddleOCR(use_angle_cls=True, lang='en')  # Nastavení jazyka a detekce orientace textu
    result = ocr.ocr(frame, cls=True)
    for line in result:
        if line is not None:
            points = line[0][0]
            toplx = points[3][0]
            toply = points[3][1]
            botdx = points[1][0]
            botdy = points[1][1]
            delka = int(points[1][0]) - int(points[0][0])
            text = line[0][1]
            if text[0] in ["FOLLOW", "follow"]:
                print(f"x: {toplx} y: {toply}")
                cv2.rectangle(
                    frame,
                    (int(toplx), int(toply)),
                    (int(botdx), int(botdy)),
                    (255, 245, 0),
                    2,
                )
                return int(toplx), int(delka)
        return -1, 1000

    return None
