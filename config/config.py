import json
import os


class Config:
    CONFIG_FILE = "config.json"

    def __init__(self):
        self._data = {}
        self.load()

    def load(self):
        if os.path.exists(self.CONFIG_FILE):
            with open(self.CONFIG_FILE, "r", encoding="utf-8") as f:
                self._data = json.load(f)
        else:
            self._data = {}

    def save(self):
        with open(self.CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)

    @property
    def text(self) -> str:
        return self._data.get("text", "")

    @text.setter
    def text(self, value) -> None:
        self._data["text"] = value
        self.save()

    @property
    def color(self) -> str:
        return self._data.get("color", "")

    @color.setter
    def color(self, value) -> None:
        self._data["color"] = value
        self.save()

    @property
    def blink_mode(self) -> bool:
        return self._data.get("blink_mode", False)

    @blink_mode.setter
    def blink_mode(self, value) -> None:
        self._data["blink_mode"] = value
        self.save()

    @property
    def end_timestamp(self) -> int:
        return self._data.get("end_timestamp", "")

    @end_timestamp.setter
    def end_timestamp(self, value) -> None:
        self._data["end_timestamp"] = value
        self.save()

    @property
    def warning_minutes(self) -> int:
        return self._data.get("warning_minutes", "")

    @warning_minutes.setter
    def warning_minutes(self, value) -> None:
        self._data["warning_minutes"] = value
        self.save()

    def clear_text(self):
        self._data["text"] = ""
        self.save()
