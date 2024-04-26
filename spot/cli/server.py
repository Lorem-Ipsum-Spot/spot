from spot.communication import HttpServer
from flask import request, jsonify
from spot.communication.http import app
from spot.movement.move import Move


def test_handler():
    return "Hello from CLI!"

ser_mover:Move
def run_http_server(mover):
    global ser_mover
    HttpServer.add_handle("/cli", test_handler)
    HttpServer.run(host="0.0.0.0", port=4321)
    ser_mover = mover


# ------- Handling HTTP requests from client -------


@app.route("/api/movement", methods=["POST"])
def handle_post_request_movement():
    if request.method != "POST":
        data = {"message": "Invalid request method from server (Movement)"}
        return jsonify(data), 200

    data = request.get_json()
    vect = data.get("dir")

    if vect[0] != 0:
        print(f"x = {vect[0]}")
        ser_mover.forward()
    if vect[1] != 0:
        print(f"y = {vect[1]}")
        ser_mover.right()
    if vect[2] != 0:
        print(f"z = {vect[2]}")

    return jsonify({"message": f"Movement vector: {vect}"}), 200


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

    data = request.get_json()
    stop = data.get("stop")

    print(f"Spots operator wants it to STOP immediately!")

    return jsonify({"message": f"Spots operator wants it to STOP immediately!"}), 200
