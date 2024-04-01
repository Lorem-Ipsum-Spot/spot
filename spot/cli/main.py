import time
from argparse import ArgumentParser
from multiprocessing import Process

import bosdyn.client.estop
from bosdyn.client import util
from bosdyn.client.lease import LeaseClient, LeaseKeepAlive
from bosdyn.client.robot_command import RobotCommandClient
from bosdyn.client.robot_state import RobotStateClient

from spot.cli.curses import run_curses_gui
from spot.communication.estop import Estop
from spot.movement.move import Move


def main():
    parser = ArgumentParser()
    util.add_base_arguments(parser)
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
        with open(options.credentials, "r") as file:
            print(f"Using credentials file: {options.credentials}")
            name, password = file.read().splitlines()
            print(f"User: {name}")
            print(f"Password: {'*' * len(password)}")
            robot.authenticate(name, password)
    else:
        util.authenticate(robot)

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

    # def f():
    #     import time
    #
    #     print("Starting Curses GUI")
    #     time.sleep(1)
    #     return run_curses_gui(estop_client, state_client)
    #
    # p = Process(target=f, args=("bob",))
    # p.start()
    # p.join()
    #
    # print("program")

    with LeaseKeepAlive(lease_client, must_acquire=True, return_at_exit=True):
        example_movement_sequence(robot, state_client, command_client)


def example_movement_sequence(robot, state_client, command_client):
    print("Powering on robot... This may take several seconds.")
    robot.power_on(timeout_sec=20)
    assert robot.is_powered_on(), "Robot power on failed."
    print("Robot powered on.")

    print("Creating movement controller")
    movement_controller = Move(state_client, command_client)
    print("Movement controller ready")

    print("Commanding robot to stand...")
    movement_controller.stand(height=0.5)
    print("Robot standing.")
    time.sleep(3)

    print("Twist")
    movement_controller.stand(yaw=0.4)
    time.sleep(3)

    print("Back")
    movement_controller.stand(height=0.8)
    time.sleep(3)

    print("Powering off...")
    robot.power_off(cut_immediately=False, timeout_sec=20)
    assert not robot.is_powered_on(), "Robot power off failed."
    print("Robot safely powered off.")


def ensure_client(robot, client):
    print(f"Initializing {client.__name__}")
    result = robot.ensure_client(client.default_service_name)
    print(f"{client.__name__} initialized")

    return result
