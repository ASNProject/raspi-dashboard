from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QVBoxLayout, QSizePolicy,
)

from widgets.card import Card


class SensorCard(Card):

    def __init__(
        self,
        title="Sensor",
        value="--",
        unit="",
        status="Waiting",
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
        self.titleLabel.setObjectName("SensorCardTitle")

        # ==========================
        # Value
        # ==========================

        self.valueLabel = QLabel(f"{value} {unit}".strip())
        self.valueLabel.setObjectName("SensorCardValue")

        # ==========================
        # Status
        # ==========================

        statusLayout = QHBoxLayout()

        self.statusDot = QLabel("●")
        self.statusDot.setObjectName("SensorStatusDot")

        self.statusLabel = QLabel(status)
        self.statusLabel.setObjectName("SensorStatus")

        statusLayout.addWidget(self.statusDot)
        statusLayout.addWidget(self.statusLabel)
        statusLayout.addStretch()

        # ==========================
        self.layout.addWidget(
            self.titleLabel,
            alignment=Qt.AlignTop,
        )

        self.layout.addWidget(
            self.valueLabel,
            alignment=Qt.AlignTop,
        )

        self.layout.addLayout(statusLayout)

    def set_value(self, value, unit=""):

        self.valueLabel.setText(
            f"{value} {unit}".strip()
        )

    def set_status(self, status):

        self.statusLabel.setText(status)

        color = "#AAAAAA"

        if status.lower() in ["normal", "connected", "safe"]:
            color = "#2ecc71"

        elif status.lower() in ["warning", "high"]:
            color = "#f39c12"

        elif status.lower() in ["danger", "error", "critical"]:
            color = "#e74c3c"

        self.statusDot.setStyleSheet(
            f"""
            color:{color};
            font-size:18px;
            """
        )