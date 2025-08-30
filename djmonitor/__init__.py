"""
Initializes a Flask application with SocketIO support using eventlet for asynchronous networking.

- Applies eventlet monkey patching for cooperative concurrency.
- Sets up Flask app with custom template and static directories.
- Configures a secret key for session management.
- Initializes SocketIO for real-time communication.

Attributes:
    BASE_DIR (str): Base directory of the project.
    TEMPLATES_DIR (str): Path to the templates directory.
    STATIC_DIR (str): Path to the static files directory.
    app (Flask): The Flask application instance.
    socketio (SocketIO): The SocketIO instance for real-time features.
"""

import eventlet  # type: ignore

eventlet.monkey_patch()

import os  # pylint: disable=wrong-import-position,wrong-import-order
from flask import Flask  # pylint: disable=wrong-import-position
from flask_socketio import SocketIO  # pylint: disable=wrong-import-position


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)
