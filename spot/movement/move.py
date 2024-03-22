from bosdyn.client.robot_state import RobotStateClient
from bosdyn.geometry import EulerZXY
from bosdyn.client.robot_command import RobotCommandBuilder, RobotCommandClient


class Move:
    state_client: RobotStateClient
    command_client: RobotCommandClient

    def __init__(self, state_client, command_client) -> None:
        self.state_client = state_client
        self.command_client = command_client

    def stand(self, yaw=0.0, roll=0.0, pitch=0.0, height=0.1):
        footprint_R_body = EulerZXY(yaw, roll, pitch)
        cmd = RobotCommandBuilder.synchro_stand_command(
            footprint_R_body=footprint_R_body, body_height=height
        )
        self.command_client.robot_command(cmd)
