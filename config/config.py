"""
Configuration management module for DJ Monitor.

This module defines the Config class, which loads, saves, and manages
application parameters (text, color, blink mode, end date, etc.).
Configuration is persisted in a JSON file.
"""

import json
import os

from djmonitor import BASE_DIR


class Config:
    """
    Configuration management class for the DJ Monitor application.
    Allows reading, writing, and persisting parameters in a JSON file.
    """

    CONFIG_FILE = "config.json"

    def __init__(self):
        """
        Initializes the configuration and loads data from the JSON file.
        """
        self._data = {}
        self.__config_path = os.path.join(BASE_DIR, "config", self.CONFIG_FILE)
        self.load()

    def load(self) -> None:
        """
        Loads configuration from the JSON file.
        If the file does not exist, initializes an empty config.
        """
        if os.path.exists(self.__config_path):
            with open(self.__config_path, "r", encoding="utf-8") as f:
                self._data = json.load(f)
        else:
            self._data = {}

    def save(self) -> None:
        """
        Saves the current configuration to the JSON file.
        """
        with open(self.__config_path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)

    @property
    def text(self) -> str:
        """
        Returns the configured publication text.
        """
        return self._data.get("text", "")

    @text.setter
    def text(self, value) -> None:
        """
        Sets the publication text and saves the config.
        """
        self._data["text"] = value
        self.save()

    @property
    def color(self) -> str:
        """
        Returns the configured display color.
        """
        return self._data.get("color", "")

    @color.setter
    def color(self, value) -> None:
        """
        Sets the display color and saves the config.
        """
        self._data["color"] = value
        self.save()

    @property
    def blink_mode(self) -> bool:
        """
        Returns the blink mode (True/False).
        """
        return self._data.get("blink_mode", False)

    @blink_mode.setter
    def blink_mode(self, value) -> None:
        """
        Sets the blink mode and saves the config.
        """
        self._data["blink_mode"] = value
        self.save()

    @property
    def end_timestamp(self) -> int:
        """
        Returns the end timestamp for the publication.
        """
        return self._data.get("end_timestamp", "")

    @end_timestamp.setter
    def end_timestamp(self, value) -> None:
        """
        Sets the end timestamp and saves the config.
        """
        self._data["end_timestamp"] = value
        self.save()

    @property
    def warning_minutes(self) -> int:
        """
        Returns the number of warning minutes before the end.
        """
        return self._data.get("warning_minutes", "")

    @warning_minutes.setter
    def warning_minutes(self, value) -> None:
        """
        Sets the number of warning minutes and saves the config.
        """
        self._data["warning_minutes"] = value
        self.save()

    def clear_text(self) -> None:
        """
        Clears the publication text and saves the config.
        """
        self._data["text"] = ""
        self.save()
