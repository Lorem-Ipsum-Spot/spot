import sys
import time
import math
from bosdyn.geometry import EulerZXY
from bosdyn.client import math_helpers
from bosdyn.client.robot_command import RobotCommandBuilder
from bosdyn.api.basic_command_pb2 import RobotCommandFeedbackStatus
from bosdyn.client.math_helpers import SE2Pose, Vec2
from bosdyn.client.frame_helpers import (
    BODY_FRAME_NAME,
    ODOM_FRAME_NAME,
    VISION_FRAME_NAME,
    get_se2_a_tform_b,
)


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

    #def turnLeft(self, angle=math.pi / 2):
    #    self.stand(yaw=angle) #TODO

    #def turnRight(self, angle=-math.pi / 2):
    #    self.stand(yaw=angle) #TODO

    def lay(self):
        self.__execute_command(RobotCommandBuilder.synchro_sit_command())

    """
    def stand(self, body_height=0.1, yaw=0.0, roll=0.0, pitch=0.0):
        footprint_R_body = EulerZXY(yaw, roll, pitch)
        cmd = RobotCommandBuilder.synchro_stand_command(footprint_R_body=footprint_R_body, body_height = body_height)
        self.command_client.robot_command(cmd)
    def standUp(self, body_height=0.1,):
        self.stand(body_height)
    """

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
