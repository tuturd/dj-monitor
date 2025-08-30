"""
This module defines socket event handlers for the DJ Monitor application.

Functions:
    register_sockets(socketio: SocketIO, config: Config) -> None:
        Registers SocketIO events for the application.

        SocketIO Events:
            "get_config":
                Handles requests for the current configuration.
                Emits the "update_publication" event to the requesting client with the following
                configuration parameters:
                    - text: The display text.
                    - color: The display color.
                    - blink_mode: The blinking mode setting.
                    - end_timestamp: The timestamp indicating when the publication ends.
                    - warning_minutes: The number of minutes before a warning is triggered.
"""

from flask_socketio import SocketIO
from config.config import Config


def register_sockets(socketio: SocketIO, config: Config) -> None:
    """
    Enregistre les événements SocketIO pour l'application DJ Monitor.

    Args:
        socketio (SocketIO): Instance du serveur SocketIO.
        config (Config): Instance de la configuration globale.
    """

    @socketio.on("get_config")
    def handle_get_config() -> None:
        """
        Événement SocketIO : renvoie la configuration courante au client demandeur.
        Envoie l'événement "update_publication" avec les paramètres de config au client.
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
            namespace="/",
        )
