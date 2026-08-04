from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class SensorPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        label = QLabel("Sensor Page")
        label.setStyleSheet("font-size:24px;")
        self.setObjectName("SensorPage")

        layout.addWidget(label)