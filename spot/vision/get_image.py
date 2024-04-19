import numpy as np
from bosdyn.api import image_pb2
import cv2
from scipy import ndimage

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


def get_complete_image(image_client):
    """
    take image_client
    return jpg
    """
    image_from_spot = get_image_from_spot(
        image_client=image_client, camera="frontleft_fisheye_image"
    )
    image_in_cv = image_to_opencv(image_from_spot)
    return image_in_cv


ROTATION_ANGLE = {
    "back_fisheye_image": 0,
    "frontleft_fisheye_image": -78,
    "frontright_fisheye_image": -102,
    "left_fisheye_image": 0,
    "right_fisheye_image": 180,
}


def image_to_opencv(image, auto_rotate=True):
    """Convert an image proto message to an openCV image."""
    num_channels = 1  # Assume a default of 1 byte encodings.
    if image.shot.image.pixel_format == image_pb2.Image.PIXEL_FORMAT_DEPTH_U16:
        dtype = np.uint16
    else:
        dtype = np.uint8
        if image.shot.image.pixel_format == image_pb2.Image.PIXEL_FORMAT_RGB_U8:
            num_channels = 3
        elif image.shot.image.pixel_format == image_pb2.Image.PIXEL_FORMAT_RGBA_U8:
            num_channels = 4
        elif image.shot.image.pixel_format == image_pb2.Image.PIXEL_FORMAT_GREYSCALE_U8:
            num_channels = 1
        elif (
            image.shot.image.pixel_format == image_pb2.Image.PIXEL_FORMAT_GREYSCALE_U16
        ):
            num_channels = 1
            dtype = np.uint16

    img = np.frombuffer(image.shot.image.data, dtype=dtype)
    if image.shot.image.format == image_pb2.Image.FORMAT_RAW:
        try:
            # Attempt to reshape array into an RGB rows X cols shape.
            img = img.reshape(
                (image.shot.image.rows, image.shot.image.cols, num_channels)
            )
        except ValueError:
            # Unable to reshape the image data, trying a regular decode.
            img = cv2.imdecode(img, -1)
    else:
        img = cv2.imdecode(img, -1)

    if auto_rotate:
        img = ndimage.rotate(img, ROTATION_ANGLE[image.source.name])

    return img


def get_image_from_spot(image_client, camera="frontleft_fisheye_image", im_res=100):
    image_request = image_pb2.ImageRequest(
        image_source_name=camera, quality_percent=im_res
    )
    image_responses = image_client.get_image([image_request])
    return image_responses[0]


"""
def get_spot_camera_image(image_client):
    sources = image_client.list_image_sources()
    camera_source = next((src for src in sources if src.name == 'frontleft_fisheye_image'), None)
    image_response = image_client.get_image_from_sources([image_pb2.ImageRequest(image_source_name=camera_source.name)])
    if image_response and image_response[0].shot.image.pixel_format == image_pb2.Image.PIXEL_FORMAT_RGB_U8:
        nparr = np.frombuffer(image_response[0].shot.image.data, dtype=np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return frame
    return None


def get_image_from_spot_B(image_client, camera:str, im_res:int = 100):
    #vrati obraz z vybrane kamery (camera), ve evolenem rozliseni (im_res(0-100%))
    #obraz je vrchni casti dolu
    #dostupne kamery
    #'back_depth', 'back_depth_in_visual_frame', 'back_fisheye_image', 'frontleft_depth', 'frontleft_depth_in_visual_frame', 'frontleft_fisheye_image', 'frontright_depth', 'frontright_depth_in_visual_frame', 'frontright_fisheye_image', 'left_depth', 'left_depth_in_visual_frame', 'left_fisheye_image', 'right_depth', 'right_depth_in_visual_frame', 'right_fisheye_image'
    image_request = image_pb2.ImageRequest(image_source_name=camera, quality_percent=im_res)
    image_response = image_client.get_image([image_request])

    for image in image_response:
        num_bytes = 1
        if image.shot.pixel_format == image_pb2.Image.PIXEL_FORMAT_DEPTH_U16:
            dtype = np.uint16
            extension = ".jpg" #mozna .png ?
        else:
            if image.shot.pixel_format == image_pb2.Image.PIXEL_FORMAT_RGB_U8:
                num_bytes = 3
            elif image.shot.pixel_format == image_pb2.Image.PIXEL_FORMAT_RGBA_U8:
                num_bytes = 4
            elif image.shot.pixel_format == image_pb2.Image.PIXEL_FORMAT_GRAYSCALE_U8:
                num_bytes = 1
            elif image.shot.pixel_format == image_pb2.Image.PIXEL_FORMAT_GRAYSCALE_U16:
                num_bytes = 2
            dtype = np.uint8
            extension = ".jpg"

        img = np.frombuffer(image.shot.image.data, dtype=dtype)
        if image.shot.image.format == image_pb2.Image.FORMAT_RAW:
            try: 
                img = img.reshape((image.shot.image.rows, image.shot.image.cols, num_bytes))
            except ValueError:
                img = cv2.imdecode(img, -1)
        else:
            img = cv2.imdecode(img, -1)

        return img

"""
