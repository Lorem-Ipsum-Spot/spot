from bosdyn.api.image_pb2 import Image
from bosdyn.api import image_pb2
from bosdyn.api import image_pb2
from bosdyn.client.image import ImageClient, build_image_request
from scipy import ndimage
from spot.cli.command import Command
from spot.vision.image_recognition import detect_text
import cv2
import numpy as np


def get_complete_image(image_client: ImageClient) -> np.ndarray:
    """
    Get the complete image from the spot camera.

    Parameters
    ----------
    image_client : ImageClient
        The image client to get the image from.

    Returns
    -------
    np.ndarray
        The complete image from the spot camera.

    """
    return get_image_from_spot(image_client, "frontleft_fisheye_image")


def pixel_format_string_to_enum(enum_string: str) -> image_pb2.Image.PixelFormat:
    return dict(image_pb2.Image.PixelFormat.items()).get(enum_string)


ROTATION_ANGLE = {
    "back_fisheye_image": 0,
    "frontleft_fisheye_image": -78,
    "frontright_fisheye_image": -102,
    "left_fisheye_image": 0,
    "right_fisheye_image": 180,
}


def get_image_from_spot(image_client: ImageClient, image_source: str):
    pixel_format = pixel_format_string_to_enum(None)
    image_request = [
        build_image_request(image_source, pixel_format=pixel_format),
    ]

    (image,) = image_client.get_image(image_request)

    num_bytes = 1  # Assume a default of 1 byte encodings.
    if image.shot.image.pixel_format == image_pb2.Image.PIXEL_FORMAT_DEPTH_U16:
        dtype = np.uint16
    else:
        if image.shot.image.pixel_format == image_pb2.Image.PIXEL_FORMAT_RGB_U8:
            num_bytes = 3
        elif image.shot.image.pixel_format == image_pb2.Image.PIXEL_FORMAT_RGBA_U8:
            num_bytes = 4
        elif image.shot.image.pixel_format == image_pb2.Image.PIXEL_FORMAT_GREYSCALE_U8:
            num_bytes = 1
        elif (
            image.shot.image.pixel_format == image_pb2.Image.PIXEL_FORMAT_GREYSCALE_U16
        ):
            num_bytes = 2
        dtype = np.uint8

    img = np.frombuffer(image.shot.image.data, dtype=dtype)
    if image.shot.image.format == image_pb2.Image.FORMAT_RAW:
        try:
            # Attempt to reshape array into an RGB rows X cols shape.
            img = img.reshape((image.shot.image.rows, image.shot.image.cols, num_bytes))
        except ValueError:
            # Unable to reshape the image data, trying a regular decode.
            img = cv2.imdecode(img, -1)
    else:
        img = cv2.imdecode(img, -1)

    return ndimage.rotate(img, ROTATION_ANGLE[image.source.name])


def set_direction(x: int, view: int, lenght: int):
    if view == 1 and x > 300:
        return Command.ROTATE_RIGHT
    elif view == 0 and x < 100:
        return Command.ROTATE_LEFT
    elif lenght < 130:
        return Command.FORWARD
    else:
        return Command.STOP


def dynamic_follow(image_client: ImageClient) -> Command:
    pic1 = get_image_from_spot(image_client, "frontleft_fisheye_image")
    if pic1 is not None:
        x, lenght = detect_text(pic1)

        if int(x) == -1:
            pic2 = get_image_from_spot(image_client, "frontright_fisheye_image")
            x, lenght = detect_text(pic2)

        return set_direction(int(x), 1, lenght)
    else:
        print("Nepodařilo se získat obrázek.")
        return Command.STOP
