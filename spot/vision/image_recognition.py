from cv2.typing import MatLike
from paddleocr import PaddleOCR

ocr = PaddleOCR(lang="en")


def detect_text(frame: MatLike) -> tuple[int, int] | None:
    result = ocr.ocr(frame, cls=False)
    for line in result:
        if line is not None:
            points = line[0][0]
            toplx = points[3][0]
            length = int(points[1][0]) - int(points[0][0])
            text = line[0][1]
            if text[0] in ["FOLLOW", "follow"]:
                return int(toplx), int(length)
        return -1, 1000

    return None
