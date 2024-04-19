import os
import bosdyn.client
import bosdyn.client.lease
import bosdyn.client.util

from bosdyn.api import image_pb2
from bosdyn.client.image import ImageClient, build_image_reguest

import numpy as np
import cv2

import matplotlib.pyplot as plt


def get_image(camera:str, im_res:int):
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

#testovaci main
def main():
    bosdyn.client.util.setup_logging()
    sdk = bosdyn.client.create_standart_sdk("MyStreamImageClient")

    hostname = os.environ.get("SPOT_IP", None)
    robot = sdk.create_robot(hostname)

    username = "user"
    password = os.environ.get("SPOT_USER_PASSWORD", None)
    robot.authenticate(username, password)
    robot.time_sync.wait_for_sync()

    #vytvoreni clienta 
    image_client = robot.ensure_client(ImageClient.default_service_name)

    img = get_image("right_fisheye_image", 70)
