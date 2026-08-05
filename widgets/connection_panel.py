from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)

from core.config_manager import Config


class ConnectionPanel(QWidget):

    def __init__(self, serial):
        super().__init__()

        self.serial = serial

        self.connected = False

        self.setObjectName("ConnectionPanel")

        self.status = None
        self.portLabel = None
        self.baudLabel = None

        self.init_ui()

        self.bind_events()

    # =====================================================
    # UI
    # =====================================================

    def init_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(8)

        title = QLabel(
            Config.get("app", "connectionNameLabel")
        )

        title.setObjectName("ConnectionTitle")

        self.status = QLabel("Disconnected")
        self.status.setObjectName("ConnectionStatus")

        port = Config.get(
            "config",
            "port",
            default="COM3",
        )

        baudrate = Config.get(
            "config",
            "baudrate",
            default=115200,
        )

        self.portLabel = QLabel(
            f"Port : {port}"
        )

        self.baudLabel = QLabel(
            f"Baudrate : {baudrate}"
        )
        layout.addWidget(title)
        layout.addWidget(self.status)

        layout.addSpacing(10)

        layout.addWidget(self.portLabel)
        layout.addWidget(self.baudLabel)

        layout.addStretch()

    # =====================================================
    # SIGNAL
    # =====================================================

    def bind_events(self):

        self.serial.connected.connect(
            self.on_connected
        )

        self.serial.disconnected.connect(
            self.on_disconnected
        )

        self.serial.error.connect(
            self.on_error
        )

    # =====================================================
    # CONNECTED
    # =====================================================

    def on_connected(self):
        print("CONNECTED SIGNAL MASUK")

        self.connected = True

        self.status.setText("🟢 Connected")

        self.status.setStyleSheet("""
            color:#00C853;
            font-weight:bold;
        """)

    # =====================================================
    # DISCONNECTED
    # =====================================================

    def on_disconnected(self):

        self.connected = False

        self.status.setText("🔴 Disconnected")

        self.status.setStyleSheet("""
            color:#F44336;
            font-weight:bold;
        """)

    # =====================================================
    # ERROR
    # =====================================================

    def on_error(self, message):

        self.connected = False

        self.status.setText("🔴 Error")

        self.status.setStyleSheet("""
            color:#F44336;
            font-weight:bold;
        """)

        print(message)
