from movement.move import Move
from bosdyn.client.robot_command import RobotCommandClient
import bosdyn.client

class Main:
    def __init__(self) -> None:
        pass

    def createRobotVar(self):
        sdk = bosdyn.client.create_standard_sdk('MyClientName')
        dog = sdk.create_robot('192.168.80.3')
        #id_client = dog.ensure_client('robot-id')
        #id_client.get_id()
        command_client = dog.ensure_client(RobotCommandClient.default_service_name)

        mover = Move(command_client)
