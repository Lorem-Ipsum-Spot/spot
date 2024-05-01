class Stop:
    """A class to monitor for stop request."""

    flag: bool

    def __init__(self) -> None:
        """Initialize the Stop object."""
        self.flag = False
