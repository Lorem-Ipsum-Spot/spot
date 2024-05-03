import cv2
import numpy as np
from bosdyn.api import image_pb2
from bosdyn.api.image_pb2 import Image
from bosdyn.client.image import ImageClient
from scipy import ndimage
from bosdyn.api import image_pb2
from bosdyn.client.image import ImageClient, build_image_request

import argparse
import sys

from spot.cli.command import Command

from spot.vision.image_recognition import detect_text
from paddleocr import PaddleOCR, draw_ocr
import bosdyn.client
import bosdyn.client.util
from bosdyn.client.image import ImageClient
import pkg_resources
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


def set_derection(x,view, lenght):
    if view == 1 and x > 300:
        return Command.ROTATE_RIGHT
    elif view == 0 and x <100:
        return Command.ROTATE_LEFT
    elif lenght <130:
        return Command.FORWARD
    else:
        return Command.STOP


def dynamic_follow(image_client:ImageClient):
    pic1=get_image_from_spot(image_client, "frontleft_fisheye_image")
    if pic1 is not None:
        x,lenght=detect_text(pic1,ocr)
        if int(x) != int(-1):
            return set_derection(int(x), 1, lenght)
        else:
            pic2 =get_image_from_spot(image_client, "frontright_fisheye_image")
            x,lenght=detect_text(pic2,ocr)
            return set_derection(int(x), 1, lenght)
    else:
        print("Nepodařilo se získat obrázek.")
        return Command.STOP

ocr = PaddleOCR(use_angle_cls=True, lang='en')  # Nastavení jazyka a detekce orientace textu

def main():
    # Analýza argumentů
    parser = argparse.ArgumentParser()
    bosdyn.client.util.add_base_arguments(parser)
    parser.add_argument('--to-depth',
                        help='Převést na obrázek hloubky. Výchozí je převést na vizuální.',
                        action='store_true')
    parser.add_argument('--camera1', help='Kamera pro získání obrázku.', default='frontleft',
                        choices=['frontleft', 'frontright', 'left', 'right', 'back',
                        ])
    parser.add_argument('--camera2', help='Kamera pro získání obrázku.', default='frontright',
                        choices=['frontleft', 'frontright', 'left', 'right', 'back',
                        ])
    parser.add_argument('--auto-rotate', help='otočit obrázky vpravo a vpředu, aby byly vzpřímené',
                        action='store_true')
    options = parser.parse_args()

    # Definice rozsahu pro modrou barvu v RGB
    blue_min = np.array([100, 100, 0], np.uint8)
    blue_max = np.array([200, 255, 255], np.uint8)

    sdk = bosdyn.client.create_standard_sdk('image_depth_plus_visual')
    robot = sdk.create_robot("192.168.80.3")
    bosdyn.client.util.authenticate(robot)
    image_client = robot.ensure_client(ImageClient.default_service_name)
    #vloozit do mainu!!!!!!
    ocr = PaddleOCR(use_angle_cls=True, lang='en')  # Nastavení jazyka a detekce orientace textu
    #!!!!!!!!!!
    #
    while True:
        pic1=get_image_from_spot(image_client, "frontleft_fisheye_image")
        if pic1 is not None:
            x,lenght=detect_text(pic1,ocr)
            if int(x) != int(-1):
                print(set_derection(int(x), 1, lenght))
                print(lenght)
                cv2.imshow('Image', pic1)
                key = cv2.waitKey(1)
            else:
                pic2 =get_image_from_spot(image_client, "frontright_fisheye_image")
                x,lenght=detect_text(pic2,ocr)
                print(set_derection(int(x), 0, lenght))
                print(lenght)
                cv2.imshow('Image', pic2)
                key = cv2.waitKey(1)

            if key == ord('q'):
                break
            #cv2.imshow('Depth', depth)
            # Výpočet procentuálního zastoupení modré barvy
            #blue_percentage = calculate_color_percentage(depth, blue_min, blue_max)
            #print(f"Procentuální zastoupení modré barvy v obrázku je: {blue_percentage:.2f}%")
            #cv2.imshow('depth clean', depth_clean)
        else:
            print("Nepodařilo se získat obrázek.")
            sys.exit(1)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

