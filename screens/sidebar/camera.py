from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class CameraPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        label = QLabel("Camera Page")
        label.setStyleSheet("font-size:24px;")
        self.setObjectName("CameraPage")

        layout.addWidget(label)