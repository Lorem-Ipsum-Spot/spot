import time
from argparse import ArgumentParser
from multiprocessing import Process
from typing import Callable, TypeVar

import bosdyn.client
from bosdyn.client import BaseClient, Robot
from bosdyn.client.gripper_camera_param import GripperCameraParamClient
from bosdyn.client.image import ImageClient
from bosdyn.client import util as bosdyn_util
from bosdyn.client.lease import LeaseClient, LeaseKeepAlive
from bosdyn.client.robot_command import RobotCommandClient
from bosdyn.client.robot_state import RobotStateClient

from spot.audio.main import listen_microphone
from spot.cli.curses import run_curses_gui
from spot.cli.server import run_http_server
from spot.communication.estop import Estop
from spot.movement.move import Move
from spot.vision.get_image import get_complete_image
from spot.vision.image_recognition import detect_lowerbody


def main():
    parser = ArgumentParser()
    bosdyn_util.add_base_arguments(parser)
    parser.add_argument(
        "-t", "--timeout", type=float, default=5, help="Timeout in seconds"
    )
    parser.add_argument(
        "-c", "--credentials", type=str, default=None, help="Credentials file"
    )
    options = parser.parse_args()

    sdk = bosdyn.client.create_standard_sdk("estop_nogui")
    robot = sdk.create_robot(options.hostname)

    if options.credentials:
        name, password = load_credentials_from_file(options.credentials)
        robot.authenticate(name, password)
    else:
        bosdyn_util.authenticate(robot)

    print("Authenticated")

    assert robot.time_sync
    print("Waiting for time sync")
    robot.time_sync.wait_for_sync()
    print("Synchronized")

    print("Initializing Estop")
    estop_client = Estop(robot, options.timeout, "Estop NoGUI")
    print("Estop initialized")

    ensure_client = robot_client_ensurer(robot)

    def f():
        import time

        print("Starting Curses GUI")
        time.sleep(1)
        return run_curses_gui(estop_client, state_client)
    state_client = ensure_client(RobotStateClient)
    command_client = ensure_client(RobotCommandClient)
    lease_client = ensure_client(LeaseClient)
    image_client = ensure_client(ImageClient)
    # gripper_camera_param_client = ensure_client(GripperCameraParamClient)

    p = Process(target=f)
    p.start()

    # TODO: run in background
    # run_http_server()

    with LeaseKeepAlive(lease_client, must_acquire=True, return_at_exit=True):
        print("Powering on robot... This may take several seconds.")
        # robot.power_on(timeout_sec=20)
        # assert robot.is_powered_on(), "Robot power on failed."
        print("Robot powered on.")

        print("Creating movement controller")
        mover = Move(command_client)
        print("Movement controller ready")

        main_event_loop(mover, image_client)

        print("Powering off...")
        robot.power_off(cut_immediately=False, timeout_sec=20)
        assert not robot.is_powered_on(), "Robot power off failed."
        print("Robot safely powered off.")

    p.join()


def main_event_loop(mover: Move, image_client):
    print("Commanding robot to stand...")
    # mover.stand()
    print("Robot standing.")
    time.sleep(3)
    print("STARTING")

    """
    mover.forward()
    time.sleep(3)

    mover.backward()
    time.sleep(3)
    """
    while True:
        command: str = listen_microphone()

        switch = {
            "dopředu": mover.forward,
            "dozadu": mover.backward,
            "sedni": mover.lay,
            "lehni": mover.lay,
            "stoupni": mover.stand,
            "následuj": follow(mover, image_client),
        }
        # Get the function corresponding to the command, or default to command_not_recognized
        command_function = switch.get(command, command_not_recognized)
        # Execute the function
        command_function()


def follow(mover: Move, image_client):
    while True:
        command: str = listen_microphone()
        if command == "stuj":
            print("zastaven")
            return

        frame = get_complete_image(image_client)  # TODO try buildin solution
        destination = detect_lowerbody(frame)
        if destination is not None:
            mover.move_to_destination(destination)

C = TypeVar("C", bound=BaseClient)

def command_not_recognized():
    print("Příkaz nerozpoznán")

def robot_client_ensurer(robot: Robot) -> Callable[[type[C]], C]:
    def inner(client: type[C]) -> C:
        print(f"Initializing {client.__name__}")
        service_name = getattr(client, "default_service_name")
        result = robot.ensure_client(service_name)
        print(f"{client.__name__} initialized")
        return result

    return inner


def load_credentials_from_file(credentials: str) -> tuple[str, str]:
    with open(credentials, "r") as file:
        print(f"Using credentials file: {credentials}")
        name, password = file.read().splitlines()
        print(f"User: {name}")
        print(f"Password: {'*' * len(password)}")
        return name, password
