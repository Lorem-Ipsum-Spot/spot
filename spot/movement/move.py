import time
from bosdyn.client.robot_command import RobotCommandBuilder
from bosdyn.client.math_helpers import SE2Pose
from bosdyn.client.frame_helpers import BODY_FRAME_NAME


class Move:
    def __init__(self, command_client):
        self.command_client = command_client

    def sit(self):
        self.__execute_command(RobotCommandBuilder.synchro_sit_command())

    def stand(self):
        self.__execute_command(RobotCommandBuilder.synchro_stand_command())

    def forward(self):
        self.__execute_velocity(v_x=self.__VELOCITY_BASE_SPEED)

    def backward(self):
        self.__execute_velocity(v_x=-self.__VELOCITY_BASE_SPEED)

    def left(self):
        self.__execute_velocity(v_y=self.__VELOCITY_BASE_SPEED)

    def right(self):
        self.__execute_velocity(v_y=-self.__VELOCITY_BASE_SPEED)

    def rotate_left(self):
        self.__execute_velocity(v_rot=self.__VELOCITY_BASE_ANGULAR)

    def rotate_right(self):
        self.__execute_velocity(v_rot=-self.__VELOCITY_BASE_ANGULAR)

    def lay(self):
        self.__execute_command(RobotCommandBuilder.synchro_sit_command())

    def move_to_destination(self, destination: SE2Pose):
        command = RobotCommandBuilder.synchro_se2_trajectory_point_command(
            destination.x, destination.y, destination.angle, BODY_FRAME_NAME
        )
        self.__execute_command(command)

    def __execute_command(self, command, end_time=None):
        self.__VELOCITY_BASE_SPEED = 0.5
        self.__VELOCITY_BASE_ANGULAR = 0.8
        self.__VELOCITY_CMD_DURATION = 0.6

        self.command_client.robot_command(command, end_time)

    def __execute_velocity(self, v_x=0.0, v_y=0.0, v_rot=0.0):
        self.__execute_command(
            RobotCommandBuilder.synchro_velocity_command(v_x=v_x, v_y=v_y, v_rot=v_rot),
            time.time() + self.__VELOCITY_CMD_DURATION,
        )
