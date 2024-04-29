from bosdyn.client.estop import EstopClient, EstopEndpoint, EstopKeepAlive


class Estop:
    """
    Provides a software estop without a GUI.

    To use this estop, create an instance of the EstopNoGui class and use the stop() and allow()
    functions programmatically.
    """

    keepalive: EstopKeepAlive

    def __init__(self, robot, timeout_sec, name=None) -> None:
        client = robot.ensure_client(EstopClient.default_service_name)

        # Force server to set up a single endpoint system
        ep = EstopEndpoint(client, name, timeout_sec)
        ep.force_simple_setup()

        # Begin periodic check-in between keep-alive and robot
        self.estop_keep_alive = EstopKeepAlive(ep)

        # Release the estop
        self.estop_keep_alive.allow()

    def __enter__(self):
        pass

    def __exit__(self, _exc_type, _exc_val, _exc_tb):
        """Cleanly shut down estop on exit."""
        self.estop_keep_alive.shutdown()

    def stop(self) -> None:
        self.estop_keep_alive.stop()

    def allow(self) -> None:
        self.estop_keep_alive.allow()

    def settle_then_cut(self) -> None:
        self.estop_keep_alive.settle_then_cut()
