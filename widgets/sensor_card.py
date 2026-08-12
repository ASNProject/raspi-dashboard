from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QSizePolicy,
)

from widgets.card import Card


class SensorCard(Card):

    def __init__(
        self,
        title="Sensor",
        value="--",
        unit="",
    ):
        super().__init__()

        self.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Maximum,
        )

        # ==========================
        # Title
        # ==========================

        self.titleLabel = QLabel(title)

        self.titleLabel.setObjectName(
            "SensorCardTitle"
        )

        # ==========================
        # Value
        # ==========================

        self.valueLabel = QLabel(
            f"{value} {unit}".strip()
        )

        self.valueLabel.setObjectName(
            "SensorCardValue"
        )

        # ==========================
        # Layout
        # ==========================

        self.layout.addWidget(
            self.titleLabel,
            alignment=Qt.AlignTop,
        )

        self.layout.addWidget(
            self.valueLabel,
            alignment=Qt.AlignTop,
        )

    # ==========================================================
    # SET VALUE
    # ==========================================================

    def set_value(
        self,
        value,
        unit=""
    ):

        self.valueLabel.setText(
            f"{value} {unit}".strip()
        )