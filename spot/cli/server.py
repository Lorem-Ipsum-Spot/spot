import sys
import time

from flask import Response, jsonify, request

from spot.cli.stopper import Stop
from spot.communication import HttpServer
from spot.communication.http import app
from spot.communication import HttpServer
from spot.cli.command import Command

HANDLER: Callable[[Command], None]


def run_http_server(stopper: Stop, handler: Callable[[Command], None]) -> None:
    """
    Run the HTTP server.

    Parameters
    ----------
    stopper : Stop
        The Stop object to monitor for stop request.
    handler : Callable[[Command], None]
        The function to call when a command is received.

    """
    global HANDLER
    HANDLER = handler

    HttpServer.run(host="0.0.0.0", port=4321)

    exit(0)


# ------- Handling HTTP requests from client -------

# ----- Small buttons


@app.route("/api/movement", methods=["POST"])
def handle_post_request_movement() -> tuple[Response, int]:
    """
    Handle the POST request for movement.

    Returns
    -------
    tuple[Response, int]
        The response and status code.

    """
    if request.method != "POST":
        data = {"message": "Invalid request method from server (Movement)"}
        return jsonify(data), 200

    data = request.get_json()
    vect = data.get("dir")

    # x je dopredu dozadu
    x, y = vect

    if x != 0 or y != 0:
        if y > 0:
            HANDLER(Command.LEFT)
        if y < 0:
            HANDLER(Command.RIGHT)
        if x > 0:
            HANDLER(Command.FORWARD)
        if x < 0:
            HANDLER(Command.BACKWARD)
    else:
        HANDLER(Command.STOP)

    return jsonify({"message": f"Movement vector: {vect}"}), 200


@app.route("/api/rotation", methods=["POST"])
def handle_post_request_rotate():
    if request.method != "POST":
        data = {"message": "Invalid request method from server (Movement)"}
        return jsonify(data), 200

    data = request.get_json()
    direction = data.get("direction")

    if direction > 0:
        HANDLER(Command.ROTATE_LEFT)
    elif direction < 0:
        HANDLER(Command.ROTATE_RIGHT)
    else:
        HANDLER(Command.STOP)

    return jsonify({"message": f"Rotation: {direction}"}), 200


@app.route("/api/updown", methods=["POST"])
def handle_post_request_updown():
    if request.method != "POST":
        data = {"message": "Invalid request method from server (Movement)"}
        return jsonify(data), 200

    data = request.get_json()
    stand = data.get("stand")

    if not stand:
        HANDLER(Command.SIT)
    else:
        HANDLER(Command.STAND)

    return jsonify({"message": f"Spot shoud now be standing is: {stand}"}), 200


# ----- Big buttons -----


@app.route("/api/followingStatus", methods=["POST"])
def handle_post_request_following() -> tuple[Response, int]:
    """
    Handle the POST request for following.

    Returns
    -------
    tuple[Response, int]
        The response and status code.

    """
    if request.method != "POST":
        data = {"message": "Invalid request method from server (Follow)"}
        return jsonify(data), 200

    data = request.get_json()
    flw = data.get("follow")

    print(f"following: {flw}")

    return jsonify({"message": f"Following Status: {flw}"}), 200


@app.route("/api/listeningStatus", methods=["POST"])
def handle_post_request_listening() -> tuple[Response, int]:
    """
    Handle the POST request for listening.

    Returns
    -------
    tuple[Response, int]
        The response and status code.

    """
    if request.method != "POST":
        data = {"message": "Invalid request method from server (Listen)"}
        return jsonify(data), 200

    data = request.get_json()
    lst = data.get("listen")

    print(f"listening: {lst}")

    return jsonify({"message": f"Listening Status: {lst}"}), 200


@app.route("/api/stop", methods=["POST"])
def handle_post_request_stop() -> tuple[Response, int]:
    """
    Handle the POST request for stopping.

    Returns
    -------
    tuple[Response, int]
        The response and status code.

    """
    if request.method != "POST":
        data = {"message": "Invalid request method from server (Stop)"}
        return jsonify(data), 200

    HANDLER(Command.STAND)

    return jsonify({"message": "Spots operator wants it to STOP immediately!"}), 200
