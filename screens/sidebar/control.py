from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class ControlPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        label = QLabel("Control Page")
        label.setStyleSheet("font-size:24px;")
        self.setObjectName("ControlPage")

        layout.addWidget(label)