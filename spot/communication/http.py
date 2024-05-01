import os

from flask import Flask, redirect, send_from_directory
from flask.typing import RouteCallable
from werkzeug.wrappers import Response

app = Flask("spot-server")


def run(host: str = "0.0.0.0", port: int = 4321) -> None:
    """
    Run the flosk server.

    Parameters
    ----------
    host : str, optional
        The host to run the server on.
    port : int, optional
        The port to run the server on.

    """
    app.run(host=host, port=port)


def add_handle(path: str, callback: RouteCallable | None) -> None:
    """
    Add a handle to the server.

    Parameters
    ----------
    path : str
        The path to the handle.
    callback : RouteCallable, optional
        The function to call when the path is accessed.

    """
    app.add_url_rule(path, view_func=callback)


@app.route("/hello")
def hello() -> str:
    """Return a hello message."""
    return "Hello from Spot!"


@app.route("/")
def home() -> Response:
    """Redirect to the home page."""
    return redirect("/index.html")


@app.route("/<path:path>")
def serve_file(path: os.PathLike[str] | str) -> Response:
    """
    Serve a file from the website directory.

    Parameters
    ----------
    path : str
        The path to the file to serve.

    """
    print(path)
    return send_from_directory("website", path)
