"""
Main application for DJ Monitor using Flask and SocketIO.

This module sets up a Flask web application with SocketIO integration to provide
real-time updates for a DJ monitoring system. It allows configuration of a publication message,
color, end time, and warning minutes, which can be updated and broadcasted to connected clients.

Routes:
    - "/" (GET): Redirects to the configuration page.
    - "/monitor" (GET): Renders the monitor view.
    - "/config" (GET): Renders the configuration view with current settings.
    - "/config/end-time" (POST): Updates the end time and warning minutes for the publication.
    - "/publication" (POST, DELETE): Updates or clears the publication text and color.

SocketIO Events:
    - "get_config": Sends the current configuration to the requesting client.
    - "update_publication": Broadcasts updated publication settings to all clients.

Configuration is managed via the `Config` class, which stores the current text,
color, end timestamp, and warning minutes.

Usage:
    Run this module directly to start the server on host 0.0.0.0 and port 8080.
"""

import eventlet

eventlet.monkey_patch()

from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO
from config.config import Config

DEBUG = True

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)
config = Config()


@app.route("/", methods=["GET"])
def home_route():
    """
    Redirects the user to the configuration route.
    Returns:
        Response: A redirect response to the 'config_route' endpoint.
    """

    return redirect(url_for("config_route"))


@app.route("/monitor", methods=["GET"])
def monitor_route():
    """
    Renders the monitor page.
    Returns:
        Response: The rendered 'monitor.html' template.
    """

    return render_template("monitor.html")


@app.route("/config", methods=["GET"])
def config_route():
    """
    Renders the configuration page with current settings.
    Retrieves the current configuration values such as text, color, end date, end time,
    and warning minutes from the global `config` object. If an end timestamp is set,
    it formats the date and time accordingly. Returns a rendered HTML template
    with these values passed as context.
    Returns:
        flask.Response: Rendered HTML template for the configuration page.
    """

    current_end_date = ""
    current_end_time = ""
    if config.end_timestamp:
        current_end_date = datetime.fromtimestamp(config.end_timestamp).strftime(
            "%Y-%m-%d"
        )
        current_end_time = datetime.fromtimestamp(config.end_timestamp).strftime(
            "%H:%M"
        )
    return render_template(
        "config.html",
        current_text=config.text,
        current_color=config.color,
        current_blink_mode=config.blink_mode,
        current_end_date=current_end_date,
        current_end_time=current_end_time,
        current_warning_minutes=config.warning_minutes,
    )


@app.route("/config/end-time", methods=["POST"])
def config_end_time_route():
    """
    Handles the configuration of the end time for a publication.
    Expects a JSON payload with the following fields:
        - date (str): The date in "YYYY-MM-DD" format.
        - time (str): The time in "HH:MM" format.
        - warning_minutes (int or str): The number of minutes before the end
        time to trigger a warning.
    Validates the input fields and updates the global configuration with the
    new end timestamp and warning minutes.
    Emits an "update_publication" event via SocketIO to notify clients of the
    updated configuration.
    Returns:
        tuple: A JSON response with either a success status or an error message,
        and the corresponding HTTP status code.
    """

    data = request.json
    date = data.get("date", "")
    time = data.get("time", "")
    warning_minutes = data.get("warning_minutes", "")

    if not all([date, time, warning_minutes]):
        return {"error": "Tous les champs doivent être définis."}, 400

    try:
        dt_str = f"{date} {time}"
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        timestamp = int(dt.timestamp())
        config.end_timestamp = timestamp
        config.warning_minutes = int(warning_minutes)

        socketio.emit(
            "update_publication",
            {
                "text": config.text,
                "color": config.color,
                "blink_mode": config.blink_mode,
                "end_timestamp": config.end_timestamp,
                "warning_minutes": config.warning_minutes,
            },
            namespace="/",
        )

    except (ValueError, TypeError) as e:
        return {"error": str(e)}, 400

    return {"status": "OK"}, 200


@app.route("/publication", methods=["POST", "DELETE"])
def publication_route():
    """
    Handles publication updates via POST and DELETE HTTP methods.
    POST:
        - Expects JSON data with optional "text" and "color" fields.
        - Updates the publication configuration with provided values.
        - Emits a "update_publication" event via SocketIO to notify clients of the update.
        - Returns the updated "text" and "color" as a JSON response.
    DELETE:
        - Clears the publication text and color in the configuration.
        - Emits a "update_publication" event via SocketIO to notify clients of the update.
        - Returns the cleared "text" and "color" as a JSON response.
    Returns:
        dict: A dictionary containing the current "text" and "color" values.
    """

    if request.method == "POST":
        data = request.json
        config.text = data.get("text", config.text)
        config.color = data.get("color", config.color)
        config.blink_mode = data.get("blink_mode", config.blink_mode)
        socketio.emit(
            "update_publication",
            {
                "text": config.text,
                "color": config.color,
                "blink_mode": config.blink_mode,
                "end_timestamp": config.end_timestamp,
                "warning_minutes": config.warning_minutes,
            },
            namespace="/",
        )
        return {
            "text": config.text,
            "color": config.color,
            "blink_mode": config.blink_mode,
        }
    if request.method == "DELETE":
        data = request.json
        config.clear_text()
        config.color = data.get("color", config.color)
        config.blink_mode = data.get("blink_mode", config.blink_mode)
        socketio.emit(
            "update_publication",
            {
                "text": "",
                "color": config.color,
                "blink_mode": False,
                "end_timestamp": config.end_timestamp,
                "warning_minutes": config.warning_minutes,
            },
            namespace="/",
        )
        return {
            "text": config.text,
            "color": config.color,
            "blink_mode": config.blink_mode,
        }


@app.route("/blink", methods=["POST"])
def blink_route():
    data = request.json
    config.color = data.get("color", config.color)
    socketio.emit(
        "blink",
        {
            "color": config.color,
        },
        namespace="/",
    )

    return {}, 200


@socketio.on("get_config")
def handle_get_config():
    """
    Emits the current configuration to the client via Socket.IO.
    Sends an "update_publication" event to the requesting client's session with
    the following configuration details:
        - text: The publication text.
        - color: The display color.
        - end_timestamp: The timestamp when the publication ends.
        - warning_minutes: Minutes before end to trigger a warning.
    The event is sent to the requesting client's room using their session ID.
    """

    socketio.emit(
        "update_publication",
        {
            "text": config.text,
            "color": config.color,
            "blink_mode": config.blink_mode,
            "end_timestamp": config.end_timestamp,
            "warning_minutes": config.warning_minutes,
        },
        room=request.sid,
        namespace="/",
    )


if __name__ == "__main__":
    socketio.run(
        app,
        host="0.0.0.0",
        port=8080,
        debug=DEBUG,
    )
