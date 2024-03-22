from flask import Flask

app = Flask("spot-server")


def run(host="0.0.0.0", port=4321):
    app.run(host=host, port=port)


def add_handle(path, callback):
    app.add_url_rule(path, view_func=callback)


@app.route("/")
def hello():
    return "Hello from Spot!"
