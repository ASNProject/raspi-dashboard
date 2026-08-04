from pathlib import Path

from PySide6.QtGui import QIcon


class Icons:
    _base = Path(__file__).resolve().parent.parent / "assets" / "icons"

    @classmethod
    def get(cls, name: str) -> QIcon:
        return QIcon(str(cls._base / f"{name}.svg"))
