import time
from argparse import ArgumentParser
from collections.abc import Callable
from threading import Thread
from typing import TypeVar

import bosdyn.client
from bosdyn.client import BaseClient, Robot
from bosdyn.client import util as bosdyn_util
from bosdyn.client.image import ImageClient
from bosdyn.client.lease import LeaseClient, LeaseKeepAlive
from bosdyn.client.robot_command import RobotCommandClient
from bosdyn.client.robot_state import RobotStateClient

from spot.audio.main import Listener
from spot.cli.command import Command, str_to_command
from spot.cli.curses import run_curses_gui
from spot.cli.server import run_http_server
from spot.cli.stopper import Stop
from spot.communication.estop import Estop
from spot.movement.move import Move
from spot.vision.get_image import dynamic_follow

active_command = Command.STOP


def handler(command: Command) -> None:
    """Change active command."""
    global active_command
    active_command = command


def main() -> None:
    """Initialize the robot and run the main event loop."""
    parser = ArgumentParser()
    bosdyn_util.add_base_arguments(parser)
    parser.add_argument(
        "-t",
        "--timeout",
        type=float,
        default=5,
        help="Timeout in seconds",
    )
    parser.add_argument(
        "-c",
        "--credentials",
        type=str,
        default=None,
        help="Credentials file",
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

    stopper = Stop()

    # create_ncurses_thread(estop_client, state_client, stopper)

    with LeaseKeepAlive(lease_client, must_acquire=True, return_at_exit=True):
        print("Powering on robot... This may take several seconds.")
        robot.power_on(timeout_sec=20)
        assert robot.is_powered_on(), "Robot power on failed."
        print("Robot powered on.")

        print("Creating movement controller")
        mover = Move(command_client)
        print("Movement controller ready")

        create_http_thread()

        main_event_loop(mover, image_client, stopper)

        print("Powering off...")
        robot.power_off(cut_immediately=False, timeout_sec=20)
        assert not robot.is_powered_on(), "Robot power off failed."
        print("Robot safely powered off.")

    stopper.flag = True


def main_event_loop(
    mover: Move,
    image_client: ImageClient,
    stopper: Stop,
) -> None:
    """
    Run a loop and process the commands from the user.

    Parameters
    ----------
    mover : Move
        The Move object to control the robot movement.
    image_client : ImageClient
        The ImageClient object to get the robot camera image.
    stopper : Stop
        The Stop object to monitor for stop request.

    """
    print("Commanding robot to stand...")
    mover.stand()
    print("Robot standing.")

    time.sleep(0.5)
    print("STARTING")

    global active_command

    def follow_cycle() -> None:
        global active_command
        active_command = dynamic_follow(image_client)

    def listener_callback(command_smth: object) -> None:
        import re

        string = str(command_smth).replace("\n", "")

        command_matched = re.match(r"[^:]*:\s*\"([\w\s]*)\".*", string)

        assert command_matched is not None, f"'{string}' is in weird format"

        command_parsed = command_matched.group(1)

        command = str_to_command(command_parsed)

        if command is None:
            print(f"Command not recognized: {command_parsed}")
            return

        print(f"Command recognized: {command}")

        global active_command
        active_command = command

    listener = Listener()
    listener.run(stopper, listener_callback)

    following = False

    while not stopper.flag:
        if following:
            follow_cycle()

        match active_command:
            case Command.STOP:
                following = False
                continue
            case Command.FORWARD:
                mover.forward()
            case Command.BACKWARD:
                mover.backward()
            case Command.LEFT:
                mover.left()
            case Command.RIGHT:
                mover.right()
            case Command.STAND:
                mover.stand()
                active_command = Command.STOP
            case Command.SIT:
                mover.sit()
                active_command = Command.STOP
            case Command.ROTATE_LEFT:
                mover.rotate_left()
            case Command.ROTATE_RIGHT:
                mover.rotate_right()
            case Command.FOLLOWING:
                following = True
                continue
            case Command.FOLLOWING_PAUSED:
                following = True
            case _:
                print(f"Command not recognized: {active_command}")

        time.sleep(0.4)


C = TypeVar("C", bound=BaseClient)


def robot_client_ensurer(robot: Robot) -> Callable[[type[C]], C]:
    """
    Create curried function that ensure a client is loaded.

    Parameters
    ----------
    robot : Robot
        The Robot object to initialize the client.

    Returns
    -------
    Callable[[type[C]], C]
        The decorator function.

    """

    def inner(client: type[C]) -> C:
        print(f"Initializing {client.__name__}")
        service_name = client.default_service_name
        result = robot.ensure_client(service_name)
        print(f"{client.__name__} initialized")
        return result

    return inner


def load_credentials_from_file(credentials: str) -> tuple[str, str]:
    """
    Load the credentials from the file.

    Parameters
    ----------
    credentials : str
        The path to the credentials file.

    Returns
    -------
    tuple[str, str]
        The tuple with the username and password.

    """
    with open(credentials) as file:
        print(f"Using credentials file: {credentials}")
        name, password = file.read().splitlines()
        print(f"User: {name}")
        print(f"Password: {'*' * len(password)}")
        return name, password


def create_http_thread() -> Thread:
    """
    Create a thread to run the HTTP server.

    Parameters
    ----------
    stopper : Stop
        The Stop object to monitor for stop request.
    mover : Move
        The Move object to control the robot movement.

    Returns
    -------
    Thread
        The thread object.

    """

    def wrapper() -> None:
        print("Starting HTTP server")
        time.sleep(1)
        return run_http_server(handler)

    process = Thread(target=wrapper)
    process.start()

    return process


def create_ncurses_thread(
    estop: Estop,
    state: RobotStateClient,
    stopper: Stop,
) -> Thread:
    """
    Create a thread to run the curses GUI.

    Parameters
    ----------
    estop : Estop
        The Estop object to trigger and release estop.
    state : RobotStateClient
        The RobotStateClient object to get the robot state.
    stopper : Stop
        The Stop object to monitor for stop request.

    Returns
    -------
    Thread
        The thread object.

    """

    def wrapper() -> None:
        print("Starting Curses GUI")
        time.sleep(3)
        return run_curses_gui(estop, state, stopper)

    process = Thread(target=wrapper)
    process.start()

    return process
