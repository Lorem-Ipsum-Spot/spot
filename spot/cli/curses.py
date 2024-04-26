import curses
import time

import bosdyn.client.estop
from bosdyn.client.robot import RobotStateClient

from spot.cli.stopper import Stop
from spot.communication.estop import Estop


def run_curses_gui(estop_client: Estop, state_client: RobotStateClient, stopper: Stop):
    # Initialize curses screen display
    stdscr = curses.initscr()

    def cleanup(msg: str):
        """Shut down curses and exit the program."""
        print("Exiting")
        estop_client.estop_keep_alive.shutdown()

        stdscr.keypad(False)
        curses.echo()
        stdscr.nodelay(False)
        curses.endwin()
        print(msg)

    def clean_exit(msg=""):
        cleanup(msg)
        exit(0)

    def run_example():
        """Run the actual example with the curses screen display"""
        # Set up curses screen display to monitor for stop request
        curses.noecho()
        stdscr.keypad(True)
        stdscr.nodelay(True)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        # If terminal cannot handle colors, do not proceed
        if not curses.has_colors():
            return

        # Clear screen
        stdscr.clear()

        # Display usage instructions in terminal
        stdscr.addstr("Estop w/o GUI running.\n")
        stdscr.addstr("\n")
        stdscr.addstr("[q] or [Ctrl-C]: Quit\n", curses.color_pair(2))
        stdscr.addstr("[SPACE]: Trigger estop\n", curses.color_pair(2))
        stdscr.addstr("[r]: Release estop\n", curses.color_pair(2))
        stdscr.addstr("[s]: Settle then cut estop\n", curses.color_pair(2))

        while not stopper.flag:
            # Retrieve user input (non-blocking)
            c = stdscr.getch()

            try:
                if c == ord(" "):
                    # estop_client.stop()
                    pass
                if c == ord("r"):
                    estop_client.allow()
                if c in [ord("q"), 3]:
                    clean_exit("Exit on user input")
                if c == ord("s"):
                    estop_client.settle_then_cut()
            except bosdyn.client.estop.EndpointUnknownError:
                clean_exit("This estop endpoint no longer valid. Exiting...")

            # Check if robot is estopped by any estops
            estop_status = "NOT_STOPPED\n"
            estop_status_color = curses.color_pair(1)
            state = state_client.get_robot_state()
            estop_states = state.estop_states
            for estop_state in estop_states:
                state_str = estop_state.State.Name(estop_state.state)
                if state_str == "STATE_ESTOPPED":
                    estop_status = "STOPPED\n"
                    estop_status_color = curses.color_pair(3)
                    break
                elif state_str == "STATE_UNKNOWN":
                    estop_status = "ERROR\n"
                    estop_status_color = curses.color_pair(3)
                elif state_str == "STATE_NOT_ESTOPPED":
                    pass
                else:
                    # Unknown estop status
                    clean_exit()

            # Display current estop status
            status_queue = estop_client.estop_keep_alive.status_queue
            if not status_queue.empty():
                latest_status = status_queue.get()[1].strip()
                if latest_status != "":
                    # If you lose this estop endpoint, report it to user
                    stdscr.addstr(7, 0, latest_status, curses.color_pair(3))

            stdscr.addstr(6, 0, estop_status, estop_status_color)

            time.sleep(0.5)

        clean_exit("Stopped by user request")

    try:
        run_example()
    except Exception as e:
        cleanup(str(e))
        raise e
