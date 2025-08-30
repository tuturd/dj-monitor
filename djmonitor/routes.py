"""
This module defines the `ConfigRoutes` class,
which manages HTTP routes for the dj-monitor Flask application.
"""

from datetime import datetime
from flask import redirect, url_for, render_template, request, Flask
from werkzeug.wrappers.response import Response as WerkzeugResponse
from flask_socketio import SocketIO
from config.config import Config


class ConfigRoutes:
    """
    Handles the registration and implementation of HTTP routes for the dj-monitor application.

    This class encapsulates all route logic related to configuration, monitoring, publication,
    and blinking functionality.
    It interacts with a Flask application, a configuration object, and a SocketIO instance to
    provide real-time updates.

    Args:
        app (Flask): The Flask application instance.
        config (Config): The configuration object managing publication settings.
        socketio (SocketIO): The SocketIO instance for emitting real-time events.

    Methods:
        register_routes():
            Registers all relevant routes to the Flask application.

        home_route() -> WerkzeugResponse:
            Redirects the root URL to the configuration page.

        monitor_route() -> str:
            Renders the monitor page.

        config_route() -> tuple[str, int]:
            Renders the configuration page with current settings.

        config_end_time_route() -> tuple[dict, int]:
            Handles POST requests to update the end time and warning minutes for the publication.

        publication_route() -> tuple[dict, int]:
            Handles POST and DELETE requests to update or clear the publication text, color,
            and blink mode.

        blink_route() -> tuple[dict, int]:
            Handles POST requests to trigger a blink event with the specified color.
    """

    def __init__(self, app: Flask, config: Config, socketio: SocketIO):
        self.app = app
        self.config = config
        self.socketio = socketio
        self.register_routes()

    def register_routes(self) -> None:
        """Registers all relevant routes to the Flask application."""

        self.app.add_url_rule("/", view_func=self.home_route)
        self.app.add_url_rule("/monitor", view_func=self.monitor_route)
        self.app.add_url_rule("/config", view_func=self.config_route)
        self.app.add_url_rule(
            "/config/end-time", view_func=self.config_end_time_route, methods=["POST"]
        )
        self.app.add_url_rule(
            "/publication", view_func=self.publication_route, methods=["POST", "DELETE"]
        )
        self.app.add_url_rule("/blink", view_func=self.blink_route, methods=["POST"])

    def home_route(self) -> WerkzeugResponse:
        """Redirects the root URL to the configuration page."""

        return redirect(url_for("config_route"))

    def monitor_route(self) -> str:
        """Renders the monitor page."""

        return render_template("monitor.html")

    def config_route(self) -> tuple[str, int]:
        """Renders the configuration page with current settings."""

        current_end_date = ""
        current_end_time = ""
        if self.config.end_timestamp:
            current_end_date = datetime.fromtimestamp(
                self.config.end_timestamp
            ).strftime("%Y-%m-%d")
            current_end_time = datetime.fromtimestamp(
                self.config.end_timestamp
            ).strftime("%H:%M")
        return (
            render_template(
                "config.html",
                current_text=self.config.text,
                current_color=self.config.color,
                current_blink_mode=self.config.blink_mode,
                current_end_date=current_end_date,
                current_end_time=current_end_time,
                current_warning_minutes=self.config.warning_minutes,
            ),
            200,
        )

    def config_end_time_route(self) -> tuple[dict, int]:
        """Handles POST requests to update the end time and warning minutes for the publication."""

        data: dict | None = request.json
        if not data:
            return {"error": "Aucune donnée reçue."}, 400

        date = data.get("date", "")
        time = data.get("time", "")
        warning_minutes = data.get("warning_minutes", "")
        if not all([date, time, warning_minutes]):
            return {"error": "Tous les champs doivent être définis."}, 400
        try:
            dt_str = f"{date} {time}"
            dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
            timestamp = int(dt.timestamp())
            self.config.end_timestamp = timestamp
            self.config.warning_minutes = int(warning_minutes)
            self.socketio.emit(
                "update_publication",
                {
                    "text": self.config.text,
                    "color": self.config.color,
                    "blink_mode": self.config.blink_mode,
                    "end_timestamp": self.config.end_timestamp,
                    "warning_minutes": self.config.warning_minutes,
                },
                namespace="/",
            )
        except (ValueError, TypeError) as e:
            return {"error": str(e)}, 400
        return {"status": "OK"}, 200

    def publication_route(self) -> tuple[dict, int]:
        """Handles POST and DELETE requests to update the publication text, color, blink mode."""

        data: dict | None = request.json
        if not data:
            return {"error": "Aucune donnée reçue."}, 400

        if request.method == "POST":
            self.config.text = data.get("text", self.config.text)
            self.config.color = data.get("color", self.config.color)
            self.config.blink_mode = data.get("blink_mode", self.config.blink_mode)
            self.socketio.emit(
                "update_publication",
                {
                    "text": self.config.text,
                    "color": self.config.color,
                    "blink_mode": self.config.blink_mode,
                    "end_timestamp": self.config.end_timestamp,
                    "warning_minutes": self.config.warning_minutes,
                },
                namespace="/",
            )
            return {
                "text": self.config.text,
                "color": self.config.color,
                "blink_mode": self.config.blink_mode,
            }, 200

        # method DELETE
        self.config.clear_text()
        self.config.color = data.get("color", self.config.color)
        self.config.blink_mode = data.get("blink_mode", self.config.blink_mode)
        self.socketio.emit(
            "update_publication",
            {
                "text": "",
                "color": self.config.color,
                "blink_mode": False,
                "end_timestamp": self.config.end_timestamp,
                "warning_minutes": self.config.warning_minutes,
            },
            namespace="/",
        )
        return {
            "text": self.config.text,
            "color": self.config.color,
            "blink_mode": self.config.blink_mode,
        }, 200

    def blink_route(self) -> tuple[dict, int]:
        """Handles POST requests to trigger a blink event with the specified color."""

        data: dict | None = request.json
        if not data:
            return {"error": "Aucune donnée reçue."}, 400

        self.config.color = data.get("color", self.config.color)
        self.socketio.emit(
            "blink",
            {
                "color": self.config.color,
            },
            namespace="/",
        )
        return {}, 200
