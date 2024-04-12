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
        if data.get("x") == "1":
            data = {"message": "Positive answer from server"}
            return jsonify(data), 200
        else:
            data = {"message": "Negative answer from server"}
            return jsonify(data), 200
    else:
        data = {"message": "Invalid request method from server"}
        return jsonify(data), 200