from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
)

from widgets.card import Card
from core.icon_manager import Icons


class DashboardToolbar(Card):

    def __init__(self):
        super().__init__()

        self.setMinimumHeight(90)

        layout = QHBoxLayout()
        layout.setSpacing(12)

        # ======================================================
        # BUTTONS
        # ======================================================

        self.startManualButton = self.create_button(
            "Start Manual",
            "play"
        )

        self.startAutoButton = self.create_button(
            "Auto Record",
            "play"
        )

        self.stopRecordButton = self.create_button(
            "Stop Record",
            "stop"
        )

        layout.addWidget(
            self.startManualButton
        )

        layout.addWidget(
            self.startAutoButton
        )

        layout.addWidget(
            self.stopRecordButton
        )

        # ======================================================
        # SPACER
        # ======================================================

        layout.addStretch()

        # ======================================================
        # RECORDING STATUS
        # ======================================================

        statusLayout = QVBoxLayout()
        statusLayout.setSpacing(2)

        self.statusLabel = QLabel(
            "● READY"
        )

        self.statusLabel.setObjectName(
            "RecordingStatus"
        )

        self.recordInfoLabel = QLabel(
            "Siap melakukan recording"
        )

        self.recordInfoLabel.setObjectName(
            "RecordingInfo"
        )

        statusLayout.addWidget(
            self.statusLabel
        )

        statusLayout.addWidget(
            self.recordInfoLabel
        )

        layout.addLayout(
            statusLayout
        )

        self.layout.addLayout(
            layout
        )

    # ==========================================================
    # BUTTON
    # ==========================================================

    def create_button(self, text, icon):

        button = QPushButton(text)

        button.setObjectName(
            "ToolbarButton"
        )

        button.setCursor(
            Qt.PointingHandCursor
        )

        button.setMinimumHeight(42)

        button.setMinimumWidth(140)

        button.setIcon(
            Icons.get(icon)
        )

        button.setIconSize(
            QSize(18, 18)
        )

        return button