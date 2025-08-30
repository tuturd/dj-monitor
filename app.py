"""
Main application entry point for dj-monitor.

- Imports configuration, app instance, routes, and socket registration functions.
- Initializes configuration and sets up HTTP routes and WebSocket sockets.
- Registers socket handlers twice (potential redundancy).
- Runs the app using SocketIO on host 0.0.0.0 and port 8080 in debug mode when executed
as the main module.
"""

from config.config import Config
from djmonitor import app, socketio
from djmonitor.routes import ConfigRoutes
from djmonitor.sockets import register_sockets

config = Config()
ConfigRoutes(app, config, socketio)
register_sockets(socketio, config)
register_sockets(socketio, config)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8080, debug=True)
