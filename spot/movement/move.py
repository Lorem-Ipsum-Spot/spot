from bosdyn.geometry import EulerZXY
from bosdyn.client.robot_command import RobotCommandBuilder
[mypy-aws_xray_sdk]
ignore_missing_imports = True

class Move:
    def __init__(self, commandClient) -> None:
        self.command_client = commandClient

    def standUp(self, body_height=0.1, yaw=0.0, roll=0.0, pitch=0.0):
        footprint_R_body = EulerZXY(yaw, roll, pitch)
        cmd = RobotCommandBuilder.synchro_stand_command(footprint_R_body=footprint_R_body, body_height = body_height)
        self.command_client.robot_command(cmd)

        #cmd = RobotCommandBuilder.synchro_stand_command(body_height=0.1)

        #self.command_client.robot_command(cmd) #used to command dog


        #robot.power_off(cut_immediately=False)