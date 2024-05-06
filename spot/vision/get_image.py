import cv2
import numpy as np
from bosdyn.api import image_pb2
from bosdyn.api.image_pb2 import Image
from bosdyn.client.image import ImageClient, build_image_request
from scipy import ndimage

from spot.cli.command import Command
from spot.vision.image_recognition import detect_text


def get_complete_image(image_client: ImageClient) -> np.ndarray | None:
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
    return dict(Image.PixelFormat.items()).get(enum_string)


ROTATION_ANGLE = {
    "back_fisheye_image": 0,
    "frontleft_fisheye_image": -78,
    "frontright_fisheye_image": -102,
    "left_fisheye_image": 0,
    "right_fisheye_image": 180,
}


def get_image_from_spot(
    image_client: ImageClient,
    image_source: str,
) -> np.ndarray | None:
    pixel_format = pixel_format_string_to_enum(None)
    image_request = [build_image_request(image_source, pixel_format=pixel_format)]

    images = image_client.get_image(image_request)

    if not images:
        return None

    (image,) = images

    pixel_format_map = {
        Image.PIXEL_FORMAT_DEPTH_U16: (1, np.uint16),
        Image.PIXEL_FORMAT_RGB_U8: (3, np.uint8),
        Image.PIXEL_FORMAT_RGBA_U8: (4, np.uint8),
        Image.PIXEL_FORMAT_GREYSCALE_U8: (1, np.uint8),
        Image.PIXEL_FORMAT_GREYSCALE_U16: (2, np.uint8),
    }

    shot_image = image.shot.image

    num_bytes, dtype = pixel_format_map.get(shot_image.pixel_format, (1, np.uint8))

    img = np.frombuffer(shot_image.data, dtype=dtype)
    if shot_image.format == image_pb2.Image.FORMAT_RAW:
        try:
            # Attempt to reshape array into an RGB rows X cols shape.
            img = img.reshape((shot_image.rows, shot_image.cols, num_bytes))
        except ValueError:
            # Unable to reshape the image data, trying a regular decode.
            img = cv2.imdecode(img, -1)
    else:
        img = cv2.imdecode(img, -1)

    return ndimage.rotate(img, ROTATION_ANGLE[image.source.name])


def set_direction(x: int, view: int, lenght: int) -> Command:
    """
    Choose the direction of movement based on the recognized text.

    Parameters
    ----------
    x : int
        The x-coordinate of the detected text in the image.
    view : int
        The view from which the image was taken. 1 for front right and 0 for front left.
    lenght : int
        The approximate distance of the detected text from the camera.

    Returns
    -------
    Command
        The command to be executed next. This can be ROTATE_RIGHT, ROTATE_LEFT, FORWARD,
        or STOP if the target is reached.

    """
    if view == 1 and x > 300:
        return Command.ROTATE_RIGHT
    elif view == 0 and x < 100:
        return Command.ROTATE_LEFT
    elif lenght < 130:
        return Command.FORWARD
    else:
        return Command.STOP


MAX_TEXT_DETECTION_FAIL_COUNT = 3
fail_count = 0


def dynamic_follow(image_client: ImageClient) -> Command:
    """
    Dynamically follow a text.

    This function dynamically follows a target by detecting text in images from two
    front cameras. It stops if it fails to get an image or if it fails to detect text
    more than a maximum allowed times as dictated by `MAX_TEXT_DETECTION_FAIL_COUNT`.

    Parameters
    ----------
    image_client : ImageClient
        The client to use for getting images.

    Returns
    -------
    Command
        The command to be executed next. This can be STOP if it fails to get an image
        or if it fails to detect text more than a maximum allowed times,
        FOLLOWING_PAUSED if no text is detected, or a command to follow if text is
        detected.

    Notes
    -----
    This function uses a global variable `fail_count` to keep track of the number
    of times it fails to detect text.

    """
    for source in ["frontleft_fisheye_image", "frontright_fisheye_image"]:
        pic = get_image_from_spot(image_client, source)
        if pic is None:
            print("Failed to get image, stopping")
            return Command.STOP

        text = detect_text(pic)

        if not text:
            continue

        x, lenght = text

        return set_direction(x, 1, lenght)

    global fail_count
    if fail_count > MAX_TEXT_DETECTION_FAIL_COUNT:
        print("Failed to detect text 3 times, stopping")
        return Command.STOP

    fail_count += 1
    print("No text detected, pausing")
    return Command.FOLLOWING_PAUSED
