from cv2.typing import MatLike
from paddleocr import PaddleOCR

ocr = PaddleOCR(lang="en")


def detect_text(frame: MatLike, text: str) -> tuple[int, int] | None:
    """
    Detect text 'FOLLOW' in an image.

    Parameters
    ----------
    frame : MatLike
        The image in which to detect text.
    text : str
        The text to search for in uppercase.

    Returns
    -------
    tuple[int, int] | None
        X-coordinate of the detected text, and the length of the text or None if no text
        was found.

    """
    result = ocr.ocr(frame, cls=False)
    for line in result:
        if line is not None:
            points = line[0][0]
            toplx = points[3][0]
            length = int(points[1][0]) - int(points[0][0])
            text = line[0][1]
            if text[0].upper() == text:
                return int(toplx), int(length)
        return -1, 1000

    return None
