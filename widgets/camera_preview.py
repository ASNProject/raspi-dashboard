import cv2

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QLabel

from widgets.card import Card


class CameraPreview(Card):

    def __init__(self, camera_index=0):
        super().__init__()

        self.camera_index = camera_index

        self.cap = None

        self.title = QLabel("Live Camera")
        self.title.setObjectName("CardTitle")

        self.imageLabel = QLabel()
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.setMinimumHeight(300)

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.imageLabel)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        self.start_camera()

    def start_camera(self):

        self.cap = cv2.VideoCapture(self.camera_index)

        if not self.cap.isOpened():

            self.imageLabel.setText("Camera Not Found")
            return

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_FPS, 30)

        self.timer.start(30)

    def stop_camera(self):

        self.timer.stop()

        if self.cap is not None:

            self.cap.release()

    def update_frame(self):

        if self.cap is None:
            return

        ret, frame = self.cap.read()

        if not ret:
            return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        h, w, ch = frame.shape

        image = QImage(
            frame.data,
            w,
            h,
            ch * w,
            QImage.Format_RGB888,
        )

        pixmap = QPixmap.fromImage(image)

        pixmap = pixmap.scaled(
            self.imageLabel.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )

        self.imageLabel.setPixmap(pixmap)

    def closeEvent(self, event):

        self.stop_camera()

        super().closeEvent(event)