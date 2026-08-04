from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QHBoxLayout, QSizePolicy,
)

from widgets.card import Card


class ControlCard(Card):

    toggled = Signal(str, bool)
    clicked = Signal(str)

    def __init__(
            self,
            key,
            title,
            control_type="switch",
            state=False,
            button_text="Execute",
    ):
        super().__init__()

        self.key = key
        self.type = control_type
        self.state = state

        self.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Maximum,
        )
        # ==========================================
        # TITLE
        # ==========================================

        self.titleLabel = QLabel(title)
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setObjectName("SensorCardTitle")

        # ==========================================
        # STATUS
        # ==========================================

        self.statusLabel = QLabel()
        self.statusLabel.setAlignment(Qt.AlignCenter)

        statusLayout = QHBoxLayout()
        statusLayout.addStretch()
        statusLayout.addWidget(self.statusLabel)
        statusLayout.addStretch()

        # ==========================================
        # BUTTON
        # ==========================================

        self.button = QPushButton()
        self.button.setObjectName("ToolbarButton")

        self.button.setMinimumHeight(40)

        if self.type == "switch":
            self.button.clicked.connect(self.toggle)
        else:
            self.button.clicked.connect(self.press)

        # ==========================================
        # LAYOUT
        # ==========================================

        self.layout.addWidget(self.titleLabel)

        if self.type == "switch":
            self.layout.addLayout(statusLayout)

        self.layout.addWidget(self.button)

        self.buttonText = button_text

        self.update_ui()

    # ==========================================
    # Switch
    # ==========================================

    def toggle(self):

        self.state = not self.state

        self.update_ui()

        self.toggled.emit(
            self.key,
            self.state,
        )

    # ==========================================
    # Button
    # ==========================================

    def press(self):

        self.clicked.emit(
            self.key
        )

    # ==========================================
    # External Update
    # ==========================================

    def set_state(self, state):

        self.state = state

        self.update_ui()

    # ==========================================
    # UI
    # ==========================================

    def update_ui(self):

        if self.type == "button":

            self.statusLabel.hide()

            self.button.setText(
                self.buttonText
            )

            return

        self.statusLabel.show()

        if self.state:

            self.statusLabel.setText("🟢 ON")
            self.button.setText("Turn OFF")

        else:

            self.statusLabel.setText("⚪ OFF")
            self.button.setText("Turn ON")