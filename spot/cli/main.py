import time
from argparse import ArgumentParser
from threading import Thread
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

    state_client = ensure_client(RobotStateClient)
    command_client = ensure_client(RobotCommandClient)
    lease_client = ensure_client(LeaseClient)
    image_client = ensure_client(ImageClient)
    # gripper_camera_param_client = ensure_client(GripperCameraParamClient)

    ncurses_thread = create_ncurses_thread(estop_client, state_client)
    http_process = create_http_thread()

    with LeaseKeepAlive(lease_client, must_acquire=True, return_at_exit=True):
        print("Powering on robot... This may take several seconds.")
        robot.power_on(timeout_sec=20)
        assert robot.is_powered_on(), "Robot power on failed."
        print("Robot powered on.")

        print("Creating movement controller")
        mover = Move(command_client)
        print("Movement controller ready")

        main_event_loop(mover, image_client)

        print("Powering off...")
        robot.power_off(cut_immediately=False, timeout_sec=20)
        assert not robot.is_powered_on(), "Robot power off failed."
        print("Robot safely powered off.")

    ncurses_thread.join()
    http_process.join()


def main_event_loop(mover: Move, image_client):
    print("Commanding robot to stand...")
    mover.stand()
    print("Robot standing.")

    time.sleep(3)
    print("STARTING")

    def follow():
        while True:
            command = listen_microphone()
            if command == "stuj":
                print("zastaven")
                return

            # TODO: try the builtin solution
            frame = get_complete_image(image_client)
            destination = detect_lowerbody(frame)
            if destination is not None:
                mover.move_to_destination(destination)

    while True:
        command = listen_microphone()

        commands = {
            "dopředu": mover.forward,
            "dozadu": mover.backward,
            "sedni": mover.lay,
            "lehni": mover.lay,
            "stoupni": mover.stand,
            "následuj": follow,
        }

        if command is None or command not in commands:
            print(f"Command not recognized: {command}")
            continue

        commands[command]()


C = TypeVar("C", bound=BaseClient)


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


def create_http_thread() -> Thread:
    def wrapper():
        print("Starting HTTP server")
        time.sleep(1)
        return run_http_server()

    process = Thread(target=wrapper)
    process.start()

    return process


def create_ncurses_thread(estop: Estop, state: RobotStateClient) -> Thread:
    def wrapper():
        print("Starting Curses GUI")
        time.sleep(3)
        return run_curses_gui(estop, state)

    process = Thread(target=wrapper)
    process.start()

    return process
