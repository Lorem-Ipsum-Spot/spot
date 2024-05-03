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

import image_recognition
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

def combine_images(img1, img2):
    height, width = img1.shape[:2]
    cropped1 = img1[0:580, MID:]
    cropped2 = img2[20:600,:width-MID-30]

    combined_frame = cv2.hconcat([cropped2, cropped1])
    return combined_frame


# Vytvoření globální proměnné pro klienta
image_client = None

def get_depth(options):
    global image_client

    if options.to_depth:
        sources1 = [options.camera1 + '_depth', options.camera1 + '_visual_in_depth_frame']
        sources2 = [options.camera2 + '_depth', options.camera2 + '_visual_in_depth_frame']
    else:
        sources1 = [options.camera1 + '_depth_in_visual_frame', options.camera1 + '_fisheye_image']
        sources2 = [options.camera2 + '_depth_in_visual_frame', options.camera2 + '_fisheye_image']

    if image_client is None:
        sdk = bosdyn.client.create_standard_sdk('image_depth_plus_visual')
        robot = sdk.create_robot("192.168.80.3")
        bosdyn.client.util.authenticate(robot)
        image_client = robot.ensure_client(ImageClient.default_service_name)

    # Zachytit obrázky
    image_responses1 = image_client.get_image_from_sources(sources1)
    image_responses2 = image_client.get_image_from_sources(sources2)

    if len(image_responses1) < 2 or len(image_responses2) < 2:
        print('Chyba: nepodařilo se získat obrázky.')
        return None

    # Hloubka je raw bytestream
    cv_depth1 = np.frombuffer(image_responses1[0].shot.image.data, dtype=np.uint16)
    cv_depth1 = cv_depth1.reshape(image_responses1[0].shot.image.rows, image_responses1[0].shot.image.cols)
    cv_depth2 = np.frombuffer(image_responses2[0].shot.image.data, dtype=np.uint16)
    cv_depth2 = cv_depth2.reshape(image_responses2[0].shot.image.rows, image_responses2[0].shot.image.cols)

    # Přidání informací o hloubce, pokud je vyžadováno
    depth8_rgb1 = cv2.applyColorMap(cv2.cvtColor(cv2.convertScaleAbs(cv_depth1, alpha=0.15), cv2.COLOR_GRAY2BGR), cv2.COLORMAP_JET)
    depth8_rgb2 = cv2.applyColorMap(cv2.cvtColor(cv2.convertScaleAbs(cv_depth2, alpha=0.15), cv2.COLOR_GRAY2BGR), cv2.COLORMAP_JET)
    depth8_rgb1 = cv2.rotate(depth8_rgb1, cv2.ROTATE_90_CLOCKWISE)
    depth8_rgb2 = cv2.rotate(depth8_rgb2, cv2.ROTATE_90_CLOCKWISE)
    cropped_d1 = depth8_rgb1[80:300,120:380]    #[60:530,120:380]    
    cropped_d2 = depth8_rgb2[60:280,90:380]     #[60:530,90:380]
    depth_combined = cv2.hconcat([cropped_d2,cropped_d1])

    return depth_combined

def calculate_color_percentage(image, color_min, color_max):
    if image is None:
        print("Obrázek nebyl načten. Zkontrolujte cestu k souboru.")
        return

    # Vytvoření masky pro vybranou barvu
    mask = cv2.inRange(image, color_min, color_max)

    # Výpočet procentuálního zastoupení barvy
    count_color_pixels = np.sum(mask == 255)
    total_pixels = image.shape[0] * image.shape[1]
    percentage = (count_color_pixels / total_pixels) * 100

    return percentage

def check_distance(img):
    
    # Definování prahové hodnoty pro "bezpečnou" vzdálenost
    # Předpokládáme, že modrá (blízkost) má hodnoty RGB blízké (0, 0, 255)
    # Zde nastavíme, že jakákoli hodnota modré složky pod 100 je považována za příliš blízko
    blue_threshold = 100
    
    # Najdeme všechny pixely, které mají hodnotu modré složky nad prahovou hodnotu
    safe_distance = np.all(img[:, :, 2] > blue_threshold, axis=-1)
    
    # Kontrola, zda jsou nějaké pixely příliš blízko
    if np.any(safe_distance == False):
        return False  # Některé pixely jsou příliš blízko
    else:
        return True  # Všechny pixely jsou v bezpečné vzdálenosti

def set_derection(x,view):
    if view == 1 and x > 300:
        return "turn_right"
    elif view == 0 and x <100:
        return "turn_left"
    
    else:
        return "nothing"


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
    ocr = PaddleOCR(use_angle_cls=True, lang='en')  # Nastavení jazyka a detekce orientace textu
    while True:
        pic1=get_image_from_spot(image_client, "frontleft_fisheye_image")
        if pic1 is not None:
            x=image_recognition.detect_text(pic1,ocr)
            if int(x) != int(-1):
                print(set_derection(int(x), 1))
                cv2.imshow('Image', pic1)
                key = cv2.waitKey(1)
            else:
                pic2 =get_image_from_spot(image_client, "frontright_fisheye_image")
                x=image_recognition.detect_text(pic2,ocr)
                print(set_derection(int(x), 0))
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


"""python get_image.py ROBOT_IP"""
"""6k1ad7psb2a5"""
"""python /Users/adam/ZPP/spot/spot/vision/get_image.py ROBOT_IP"""