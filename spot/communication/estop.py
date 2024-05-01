from bosdyn.client import Robot
from bosdyn.client.estop import EstopClient, EstopEndpoint, EstopKeepAlive


class Estop:
    """
    Provides a software estop without a GUI.

    To use this estop, create an instance of the EstopNoGui class and use the stop()
    and allow() functions programmatically.
    """

    keepalive: EstopKeepAlive

    def __init__(
        self,
        robot: Robot,
        timeout_sec: float,
        name: str | None = None,
    ) -> None:
        """
        Create an instance of the Estop class.

        Parameters
        ----------
        robot : Robot
            The robot to estop.
        timeout_sec : float
            The time in seconds to wait before estop.
        name : str, optional
            The name of the estop endpoint.

        """
        client = robot.ensure_client(EstopClient.default_service_name)

        # Force server to set up a single endpoint system
        ep = EstopEndpoint(client, name, timeout_sec)
        ep.force_simple_setup()

        # Begin periodic check-in between keep-alive and robot
        self.estop_keep_alive = EstopKeepAlive(ep)

        # Release the estop
        self.estop_keep_alive.allow()

    def stop(self) -> None:
        """Cut the estop."""
        self.estop_keep_alive.stop()

    def allow(self) -> None:
        """Allow the robot to move."""
        self.estop_keep_alive.allow()

    def settle_then_cut(self) -> None:
        """Settle the estop, then cut it."""
        self.estop_keep_alive.settle_then_cut()
