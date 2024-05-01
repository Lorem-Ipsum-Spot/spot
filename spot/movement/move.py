import time
from typing import Any

from bosdyn.client.frame_helpers import BODY_FRAME_NAME
from bosdyn.client.math_helpers import SE2Pose
from bosdyn.client.robot_command import RobotCommandBuilder, RobotCommandClient


class Move:
    """Provides a way to move the robot."""

    def __init__(self, command_client: RobotCommandClient) -> None:
        """
        Create an instance of the Move class.

        Parameters
        ----------
        command_client : RobotCommandClient
            The command client to send commands to the robot.

        """
        self.command_client = command_client

    def sit(self) -> None:
        """Sit the robot down."""
        self.__execute_command(RobotCommandBuilder.synchro_sit_command())

    def stand(self) -> None:
        """Stand the robot up."""
        self.__execute_command(RobotCommandBuilder.synchro_stand_command())

    def forward(self) -> None:
        """Move the robot forward."""
        self.__execute_velocity(v_x=self.__VELOCITY_BASE_SPEED)

    def backward(self) -> None:
        """Move the robot backward."""
        self.__execute_velocity(v_x=-self.__VELOCITY_BASE_SPEED)

    def left(self) -> None:
        """Move the robot left."""
        self.__execute_velocity(v_y=self.__VELOCITY_BASE_SPEED)

    def right(self) -> None:
        """Move the robot right."""
        self.__execute_velocity(v_y=-self.__VELOCITY_BASE_SPEED)

    def rotate_left(self) -> None:
        """Rotate the robot left."""
        self.__execute_velocity(v_rot=self.__VELOCITY_BASE_ANGULAR)

    def rotate_right(self) -> None:
        """Rotate the robot right."""
        self.__execute_velocity(v_rot=-self.__VELOCITY_BASE_ANGULAR)

    def lay(self) -> None:
        """Lay the robot down."""
        self.__execute_command(RobotCommandBuilder.synchro_sit_command())

    def move_to_destination(self, destination: SE2Pose) -> None:
        """
        Move the robot to the specified destination.

        Parameters
        ----------
        destination : SE2Pose
            The destination to move the robot to.

        """
        command = RobotCommandBuilder.synchro_se2_trajectory_point_command(
            destination.x,
            destination.y,
            destination.angle,
            BODY_FRAME_NAME,
        )
        self.__execute_command(command)

    def __execute_command(self, command: Any, end_time: float | None = None) -> None:
        """
        Execute the specified command.

        Parameters
        ----------
        command
            The command to execute.
        end_time
            The time to end the command.

        """
        self.__VELOCITY_BASE_SPEED = 0.5
        self.__VELOCITY_BASE_ANGULAR = 0.8
        self.__VELOCITY_CMD_DURATION = 0.6

        self.command_client.robot_command(command, end_time)

    def __execute_velocity(
        self,
        v_x: float = 0.0,
        v_y: float = 0.0,
        v_rot: float = 0.0,
    ) -> None:
        """
        Execute the specified velocity.

        Parameters
        ----------
        v_x : float, optional
            The velocity in the x direction.
        v_y : float, optional
            The velocity in the y direction.
        v_rot : float, optional
            The rotational velocity.

        """
        self.__execute_command(
            RobotCommandBuilder.synchro_velocity_command(v_x=v_x, v_y=v_y, v_rot=v_rot),
            time.time() + self.__VELOCITY_CMD_DURATION,
        )
