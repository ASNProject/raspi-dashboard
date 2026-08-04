import random

from PySide6.QtCore import QObject, QTimer, Signal


class DummyData(QObject):

    sensorChanged = Signal(float, float, float)
    fpsChanged = Signal(int)

    def __init__(self):
        super().__init__()

        self.timer = QTimer()
        self.timer.timeout.connect(self.generate)

    def start(self):
        self.timer.start(1000)

    def stop(self):
        self.timer.stop()

    def generate(self):

        temperature = random.uniform(26, 33)

        humidity = random.uniform(50, 85)

        gas = random.uniform(120, 350)

        fps = random.randint(28, 31)

        self.sensorChanged.emit(
            temperature,
            humidity,
            gas,
        )

        self.fpsChanged.emit(fps)