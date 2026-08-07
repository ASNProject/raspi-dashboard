import json
from pathlib import Path


class Config:
    app = {}
    ui = {}
    sensor = {}
    serial = {}
    theme = {}
    control = {}

    _loaded = False
    _config_dir = Path(__file__).parent.parent / "config"

    @classmethod
    def load(cls):

        if cls._loaded:
            return

        cls.app = cls._read("app.json")
        cls.ui = cls._read("ui.json")
        cls.sensor = cls._read("sensor.json")
        cls.serial = cls._read("serial.json")
        cls.theme = cls._read("theme.json")
        cls.control = cls._read("control.json")
        cls.config = cls._read("config.json")

        cls._loaded = True

    @classmethod
    def _read(cls, filename):

        path = cls._config_dir / filename

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    @classmethod
    def get(cls, category, *keys, default=None):

        data = getattr(cls, category, None)

        if data is None:
            return default

        try:
            for key in keys:
                data = data[key]

            return data

        except (KeyError, TypeError):
            return default
