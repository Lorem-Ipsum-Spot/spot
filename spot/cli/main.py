import time
from argparse import ArgumentParser
from multiprocessing import Process

import bosdyn.client.estop
from bosdyn.client import util as bosdyn_util
from bosdyn.client.lease import LeaseClient, LeaseKeepAlive
from bosdyn.client.robot_command import RobotCommandClient
from bosdyn.client.robot_state import RobotStateClient

from spot.communication.estop import Estop
from spot.cli.curses import run_curses_gui
from spot.cli.server import run_http_server
from spot.movement.move import Move


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
        name, password = load_credential_from_file(options.credentials)
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

    state_client, command_client, lease_client = [
        ensure_client(robot, client)
        for client in (RobotStateClient, RobotCommandClient, LeaseClient)
    ]

    def f():
        import time

        print("Starting Curses GUI")
        time.sleep(1)
        return run_curses_gui(estop_client, state_client)

    p = Process(target=f)
    p.start()

    run_http_server()

    # with LeaseKeepAlive(lease_client, must_acquire=True, return_at_exit=True):
    #     print("Powering on robot... This may take several seconds.")
    #     robot.power_on(timeout_sec=20)
    #     assert robot.is_powered_on(), "Robot power on failed."
    #     print("Robot powered on.")
    #
    #     print("Creating movement controller")
    #     mover = Move(command_client)
    #     print("Movement controller ready")
    #
    #     example_movement_sequence(mover)
    #
    #     print("Powering off...")
    #     robot.power_off(cut_immediately=False, timeout_sec=20)
    #     assert not robot.is_powered_on(), "Robot power off failed."
    #     print("Robot safely powered off.")

    p.join()


def example_movement_sequence(mover: Move):
    print("Commanding robot to stand...")
    mover.stand()
    print("Robot standing.")
    time.sleep(3)

    mover.forward()
    time.sleep(3)

    mover.backward()
    time.sleep(3)


def ensure_client(robot, client):
    print(f"Initializing {client.__name__}")
    result = robot.ensure_client(client.default_service_name)
    print(f"{client.__name__} initialized")

    return result


def load_credential_from_file(credentials):
    with open(credentials, "r") as file:
        print(f"Using credentials file: {credentials}")
        name, password = file.read().splitlines()
        print(f"User: {name}")
        print(f"Password: {'*' * len(password)}")
        return name, password
