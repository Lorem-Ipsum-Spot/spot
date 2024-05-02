import cv2
import numpy as np
from bosdyn.api import image_pb2
from bosdyn.api.image_pb2 import Image
from bosdyn.client.image import ImageClient
from scipy import ndimage
from bosdyn.api import image_pb2
from bosdyn.client.image import ImageClient, build_image_request
"""
'back_depth'
'back_depth_in_visual_frame'
'back_fisheye_image'
'frontleft_depth'
'frontleft_depth_in_visual_frame'
'frontleft_fisheye_image'
'frontright_depth'
'frontright_depth_in_visual_frame'
'frontright_fisheye_image'
'left_depth'
'left_depth_in_visual_frame'
'left_fisheye_image'
'right_depth'
'right_depth_in_visual_frame'
'right_fisheye_image'
"""

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
    image_from_spot = get_image_from_spot(image_client, "frontleft_fisheye_image")
    return image_from_spot

def pixel_format_string_to_enum(enum_string):
    return dict(image_pb2.Image.PixelFormat.items()).get(enum_string)

def get_image_from_spot(image_client,image_source):
    ROTATION_ANGLE = {
    'back_fisheye_image': 0,
    'frontleft_fisheye_image': -78,
    'frontright_fisheye_image': -102,
    'left_fisheye_image': 0,
    'right_fisheye_image': 180
    }

    pixel_format = pixel_format_string_to_enum(None)
    image_request = [
        build_image_request(image_source, pixel_format=pixel_format),
    ]
    
    image_responses = image_client.get_image(image_request)

    for image in image_responses:
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
            elif image.shot.image.pixel_format == image_pb2.Image.PIXEL_FORMAT_GREYSCALE_U16:
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
        img = ndimage.rotate(img, ROTATION_ANGLE[image.source.name])
    return img


