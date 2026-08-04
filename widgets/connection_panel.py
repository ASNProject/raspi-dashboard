from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
)

from core.config_manager import Config


class ConnectionPanel(QWidget):

    def __init__(self):
        super().__init__()

        self.baudCombo = None
        self.portCombo = None
        self.status = None
        self.connectButton = None
        self.setObjectName("ConnectionPanel")

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(8)

        title = QLabel(Config.get("app", "connectionNameLabel"))
        title.setObjectName("ConnectionTitle")

        self.status = QLabel(Config.get("app", "disconnected"))
        self.status.setObjectName("ConnectionStatus")

        portLabel = QLabel(Config.get("app", "port"))

        self.portCombo = QComboBox()
        self.portCombo.addItem(Config.get("app", "selectPort"))

        baudLabel = QLabel(Config.get("app", "baudRate"))

        self.baudCombo = QComboBox()
        self.baudCombo.addItems([
            "9600",
            "57600",
            "115200"
        ])

        self.baudCombo.setCurrentText("115200")

        self.connectButton = QPushButton(Config.get("app", "connectButton"))
        self.connectButton.setObjectName("PrimaryButton")

        layout.addWidget(title)
        layout.addWidget(self.status)

        layout.addSpacing(5)

        layout.addWidget(portLabel)
        layout.addWidget(self.portCombo)

        layout.addWidget(baudLabel)
        layout.addWidget(self.baudCombo)

        layout.addStretch()

        layout.addWidget(self.connectButton)
