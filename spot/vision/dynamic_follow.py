import cv2
import numpy as np
from bosdyn.client import create_standard_sdk
from bosdyn.client.image import ImageClient
from bosdyn.api import image_pb2, geometry_pb2
from bosdyn.client.robot_command import RobotCommandClient, RobotCommandBuilder
from bosdyn.client.frame_helpers import BODY_FRAME_NAME
import bosdyn.client.util

# Konfigurace připojení k robotu
ROBOT_IP = '192.168.50.3'  # Zadejte IP adresu robota
USERNAME = 'admin'         # Zadejte uživatelské jméno
PASSWORD = 'password'      # Zadejte heslo

# Inicializace klienta SDK
sdk = create_standard_sdk('image_service')
robot = sdk.create_robot(ROBOT_IP)
robot.authenticate(USERNAME, PASSWORD)
image_client = robot.ensure_client(ImageClient.default_service_name)
robot_command_client = robot.ensure_client(RobotCommandClient.default_service_name)

# Nastavení detektoru obličejů
#cascade_path = "/path/to/haarcascade_frontalface_default.xml"  # Absolutní cesta k souboru XML
cascade_path = pathlib.Path(cv2.__file__).parent.absolute( )/ "data/haarcascade_lowerbody.xml"
clf = cv2.CascadeClassifier(cascade_path)

# Parametry kamery (upravit podle vaší kamery)
focal_length = 620  # Příklad fokální délky
center_x = 320      # Příklad středu obrazu x
center_y = 240      # Příklad středu obrazu y
depth = 2000        # Předpokládaná vzdálenost obličeje v mm (2 metry)

def pixel_to_world(x_pixel, y_pixel, depth):
    X = (x_pixel - center_x) * depth / focal_length
    Y = (y_pixel - center_y) * depth / focal_length
    Z = depth
    return X, Y, Z

def get_spot_camera_image():
    sources = image_client.list_image_sources()
    camera_source = next((src for src in sources if src.name == 'frontleft_fisheye_image'), None)
    image_response = image_client.get_image_from_sources([image_pb2.ImageRequest(image_source_name=camera_source.name)])
    if image_response and image_response[0].shot.image.pixel_format == image_pb2.Image.PIXEL_FORMAT_RGB_U8:
        nparr = np.frombuffer(image_response[0].shot.image.data, dtype=np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return frame
    return None

def main():
    prev_center_x, prev_center_y = None, None

    while True:
        frame = get_spot_camera_image()
        if frame is not None:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            legs = clf.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            if len(legs) > 0:
                x, y, width, height = legs[0]
                cv2.rectangle(frame, (x, y), (x+width, y+height), (255, 245, 0), 2)
                center_x = x + width // 2
                center_y = y + height // 2
                X, Y, Z = pixel_to_world(center_x, center_y, depth)
                destination = geometry_pb2.Vec2(x=X/1000, y=Y/1000)  # Převod mm na metry
                se2_pose = geometry_pb2.SE2Pose(position=destination, angle=0)
                command = RobotCommandBuilder.synchro_se2_trajectory_point_command(se2_pose, BODY_FRAME_NAME)
                robot_command_client.robot_command(command)

            cv2.imshow("Faces", frame)
            if cv2.waitKey(1) == ord("q"):
                break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()