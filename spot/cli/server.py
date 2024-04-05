from spot.communication import HttpServer


def test_handler():
    return "Hello from CLI!"


def run_http_server():
    HttpServer.add_handle("/cli", test_handler)
    HttpServer.run(host="0.0.0.0", port=4321)
