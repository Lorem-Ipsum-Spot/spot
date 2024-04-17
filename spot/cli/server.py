from spot.communication import HttpServer
from flask import request, jsonify
from spot.communication.http import app


def test_handler():
    return "Hello from CLI!"


def run_http_server():
    HttpServer.add_handle("/cli", test_handler)
    HttpServer.run(host="0.0.0.0", port=4321)


@app.route("/cli/server.py", methods=['POST'])
def handle_post_request():
    if request.method == 'POST':
        data = request.get_json()

        vect = data.get("dir")

        if vect[0] != 0:
            print(f"x = {vect[0]}")
        if vect[1] != 0:
            print(f"y = {vect[1]}")
        if vect[2] != 0:
            print(f"z = {vect[2]}")

        return jsonify({"message" : f"Movement OK {vect}"}), 200

    else:
        data = {"message": "Invalid request method from server (Movement)"}
        return jsonify(data), 200
    

@app.route("/cli/voky.py", methods=['POST'])
def handle_post_request2():
    if request.method == 'POST':
        data = request.get_json()

        flw = data.get("follow")
        print(f"following: {flw}")

        return jsonify({"message" : f"Following OK: {flw}"}), 200
    
    else:
        data = {"message": "Invalid request method from server (Follow)"}
        return jsonify(data), 200
    