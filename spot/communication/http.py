from flask import Flask, send_from_directory, redirect

app = Flask("spot-server")


def run(host="0.0.0.0", port=4321):
    app.run(host=host, port=port)


def add_handle(path, callback):
    app.add_url_rule(path, view_func=callback)


@app.route("/hello")
def hello():
    return "Hello from Spot!"


@app.route("/")
def home():
    return redirect("/index.html")


@app.route("/<path:path>")
def serve_file(path):
    print(path)
    return send_from_directory("website", path)
