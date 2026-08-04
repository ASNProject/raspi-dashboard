from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
)

from widgets.card import Card
from core.icon_manager import Icons


class DashboardToolbar(Card):

    def __init__(self):
        super().__init__()

        self.setMinimumHeight(90)

        layout = QHBoxLayout()
        layout.setSpacing(12)

        self.startButton = self.create_button(
            "Start Camera",
            "play"
        )

        self.stopButton = self.create_button(
            "Stop Camera",
            "stop"
        )

        self.refreshButton = self.create_button(
            "Refresh",
            "refresh"
        )

        self.saveButton = self.create_button(
            "Save Data",
            "save"
        )

        self.settingButton = self.create_button(
            "Settings",
            "settings"
        )

        layout.addWidget(self.startButton)
        layout.addWidget(self.stopButton)
        layout.addWidget(self.refreshButton)
        layout.addStretch()
        layout.addWidget(self.saveButton)
        layout.addWidget(self.settingButton)

        self.layout.addLayout(layout)

    def create_button(self, text, icon):

        button = QPushButton(text)

        button.setObjectName("ToolbarButton")

        button.setCursor(Qt.PointingHandCursor)

        button.setMinimumHeight(42)

        button.setMinimumWidth(140)

        button.setIcon(Icons.get(icon))

        button.setIconSize(QSize(18, 18))

        return button