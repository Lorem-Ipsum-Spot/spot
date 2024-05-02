import get_image
import image_recognition

import argparse
import sys

import pathlib
import cv2
import numpy as np
from scipy import ndimage

import bosdyn.client
import bosdyn.client.util
from bosdyn.api import image_pb2
from bosdyn.client.image import ImageClient, build_image_request


def connect():
    # Parse args
    parser = argparse.ArgumentParser()
    bosdyn.client.util.add_base_arguments(parser)
    parser.add_argument('--list', help='list image sources', action='store_true')
    parser.add_argument('--auto-rotate', help='rotate right and front images to be upright',
                        action='store_true')
    parser.add_argument('--image-service', help='Name of the image service to query.',
                        default=ImageClient.default_service_name)
    parser.add_argument(
        '--pixel-format', choices=image_pb2.Image.PixelFormat.keys()[1:],
        help='Requested pixel format of image. If supplied, will be used for all sources.')

    options = parser.parse_args()
    print(options)

    # Create robot object with an image client.
    sdk = bosdyn.client.create_standard_sdk('image_capture')
    robot = sdk.create_robot("192.168.80.3")
    bosdyn.client.util.authenticate(robot)
    robot.sync_with_directory()
    robot.time_sync.wait_for_sync()

    image_client = robot.ensure_client(options.image_service)

    return image_client

if __name__ == '__main__':
    client = get_image.connect()
    while True:
        frame = get_image.get_one_pic(client)
        image_recognition.detect_lowerbody(frame)
        

