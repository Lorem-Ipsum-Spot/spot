import argparse

import bosdyn.client.util
import bosdyn.client.estop
from bosdyn.client.robot_state import RobotStateClient

from spot.communication.estop import Estop
from spot.cli.curses import run_curses_gui


from multiprocessing import Process


def main():
    parser = argparse.ArgumentParser()
    bosdyn.client.util.add_base_arguments(parser)
    parser.add_argument(
        "-t", "--timeout", type=float, default=5, help="Timeout in seconds"
    )
    parser.add_argument(
        "-c", "--credentials", type=str, default=None, help="Credentials file"
    )
    # parser.add_argument("command", type=str, help="The command to execute")
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
        bosdyn.client.util.authenticate(robot)

    print("Authenticated")
    print("Initializing Estop")
    # Create nogui estop
    estop_client = Estop(robot, options.timeout, "Estop NoGUI")
    print("Estop initialized")

    print("Initializing Robot State Client")
    # Create robot state client for the robot
    state_client = robot.ensure_client(RobotStateClient.default_service_name)
    print("Robot State Client initialized")

    def f():
        import time

        print("Starting Curses GUI")
        time.sleep(1)
        return run_curses_gui(estop_client, state_client)

    p = Process(target=f, args=("bob",))
    p.start()
    p.join()

    print("program")
