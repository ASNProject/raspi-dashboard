from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class SettingsPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        label = QLabel("Settings Page")
        label.setStyleSheet("font-size:24px;")
        self.setObjectName("SettingsPage")

        layout.addWidget(label)