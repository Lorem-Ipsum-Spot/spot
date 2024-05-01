import time
from flask import request, jsonify

from spot.cli.stopper import Stop
from spot.communication.http import app
from spot.communication import HttpServer
from spot.cli.command import Command

HANDLER: callable


def run_http_server(stopper: Stop, handler: callable):
    global HANDLER
    HANDLER = handler

    HttpServer.run(host="0.0.0.0", port=4321)

    exit(0)


# ------- Handling HTTP requests from client -------

# ----- Small buttons

@app.route("/api/movement", methods=["POST"])
def handle_post_request_movement():
    if request.method != "POST":
        data = {"message": "Invalid request method from server (Movement)"}
        return jsonify(data), 200

    data = request.get_json()
    vect = data.get("dir")

    x, y = vect

    if x > 0:
        HANDLER(Command.RIGHT)
    if x < 0:
        HANDLER(Command.LEFT)
    else:
        HANDLER(Command.STOP)

    if y > 0:
        HANDLER(Command.FORWARD)
    if y < 0:
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
        return jsonify({"message": "Got 0 for rotation > impossible."}), 200

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
def handle_post_request_following():
    if request.method != "POST":
        data = {"message": "Invalid request method from server (Follow)"}
        return jsonify(data), 200

    data = request.get_json()
    flw = data.get("follow")

    print(f"following: {flw}")

    return jsonify({"message": f"Following Status: {flw}"}), 200


@app.route("/api/listeningStatus", methods=["POST"])
def handle_post_request_listening():
    if request.method != "POST":
        data = {"message": "Invalid request method from server (Listen)"}
        return jsonify(data), 200

    data = request.get_json()
    lst = data.get("listen")

    print(f"listening: {lst}")

    return jsonify({"message": f"Listening Status: {lst}"}), 200


@app.route("/api/stop", methods=["POST"])
def handle_post_request_stop():
    if request.method != "POST":
        data = {"message": "Invalid request method from server (Stop)"}
        return jsonify(data), 200

    HANDLER(Command.STOP)

    return jsonify({"message": f"Spots operator wants it to STOP immediately!"}), 200
