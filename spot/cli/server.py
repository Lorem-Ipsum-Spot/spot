import sys
import time

from flask import Response, jsonify, request

from spot.cli.stopper import Stop
from spot.communication import HttpServer
from spot.communication.http import app
from spot.movement.move import Move


def test_handler() -> str:
    """Test handler for HTTP server."""
    return "Hello from CLI!"


MOVER: Move


def run_http_server(stopper: Stop, mover: Move) -> None:
    """
    Run the HTTP server.

    Parameters
    ----------
    stopper : Stop
        The Stop object to monitor for stop request.
    mover : Move
        The Move object to control the robot movement.

    """
    global MOVER
    MOVER = mover

    HttpServer.add_handle("/cli", test_handler)
    HttpServer.run(host="0.0.0.0", port=4321)

    while not stopper.flag:
        time.sleep(1)

    sys.exit(0)


# ------- Handling HTTP requests from client -------


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

    x, y, z = vect

    if x > 0:
        MOVER.right()
    if x < 0:
        MOVER.left()

    if y > 0:
        MOVER.forward()
    if y < 0:
        MOVER.backward()

    if z > 0:
        MOVER.stand()
    if z < 0:
        MOVER.sit()

    return jsonify({"message": f"Movement vector: {vect}"}), 200


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

    data = request.get_json()
    stop = data.get("stop")

    print("Spots operator wants it to STOP immediately!")

    return jsonify({"message": "Spots operator wants it to STOP immediately!"}), 200
