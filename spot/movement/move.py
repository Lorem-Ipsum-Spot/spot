import sys
import time
import math
from bosdyn.geometry import EulerZXY
from bosdyn.client import math_helpers
from bosdyn.client.robot_command import RobotCommandBuilder
from bosdyn.api.basic_command_pb2 import RobotCommandFeedbackStatus
from bosdyn.client.frame_helpers import (BODY_FRAME_NAME, ODOM_FRAME_NAME, VISION_FRAME_NAME,
                                        get_se2_a_tform_b)

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

    def turnLeft(self, angle = math.pi/2):
        self.stand(yaw = angle)

    def turnRight(self, angle = -math.pi/2):
        self.stand(yaw = angle)

    def lay(self):
        pass
    
    '''
    def stand(self, body_height=0.1, yaw=0.0, roll=0.0, pitch=0.0):
        footprint_R_body = EulerZXY(yaw, roll, pitch)
        cmd = RobotCommandBuilder.synchro_stand_command(footprint_R_body=footprint_R_body, body_height = body_height)
        self.command_client.robot_command(cmd)
    def standUp(self, body_height=0.1,):
        self.stand(body_height)
    '''
        


    def __execute_command(self, command, end_time=None):
        self.__VELOCITY_BASE_SPEED = 0.5
        self.__VELOCITY_BASE_ANGULAR = 0.8
        self.__VELOCITY_CMD_DURATION = 0.6

        self.command_client.robot_command(command, end_time)


    def __execute_velocity(self, v_x=0.0, v_y=0.0, v_rot=0.0):
        self.__execute_command(
            RobotCommandBuilder.synchro_velocity_command(
                v_x=v_x,
                v_y=v_y,
                v_rot=v_rot
            ),
            time.time() + self.__VELOCITY_CMD_DURATION)




def relative_move(dx, dy, dyaw, frame_name, robot_command_client, robot_state_client, stairs=False):
    transforms = robot_state_client.get_robot_state().kinematic_state.transforms_snapshot

    # Build the transform for where we want the robot to be relative to where the body currently is.
    body_tform_goal = math_helpers.SE2Pose(x=dx, y=dy, angle=dyaw)
    # We do not want to command this goal in body frame because the body will move, thus shifting
    # our goal. Instead, we transform this offset to get the goal position in the output frame
    # (which will be either odom or vision).
    out_tform_body = get_se2_a_tform_b(transforms, frame_name, BODY_FRAME_NAME)
    out_tform_goal = out_tform_body * body_tform_goal

    # Command the robot to go to the goal point in the specified frame. The command will stop at the
    # new position.
    robot_cmd = RobotCommandBuilder.synchro_se2_trajectory_point_command(
        goal_x=out_tform_goal.x, goal_y=out_tform_goal.y, goal_heading=out_tform_goal.angle,
        frame_name=frame_name, params=RobotCommandBuilder.mobility_params(stair_hint=stairs))
    end_time = 10.0
    cmd_id = robot_command_client.robot_command(lease=None, command=robot_cmd,
                                                end_time_secs=time.time() + end_time)
    # Wait until the robot has reached the goal.
    while True:
        feedback = robot_command_client.robot_command_feedback(cmd_id)
        mobility_feedback = feedback.feedback.synchronized_feedback.mobility_command_feedback
        if mobility_feedback.status != RobotCommandFeedbackStatus.STATUS_PROCESSING:
            print('Failed to reach the goal')
            return False
        traj_feedback = mobility_feedback.se2_trajectory_feedback
        if (traj_feedback.status == traj_feedback.STATUS_AT_GOAL and
                traj_feedback.body_movement_status == traj_feedback.BODY_STATUS_SETTLED):
            print('Arrived at the goal.')
            return True
        time.sleep(1)

    return True
