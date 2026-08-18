import csv
from pathlib import Path
from datetime import datetime

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QScrollArea,
    QSizePolicy,
)
from PySide6.QtCore import Qt, QTimer

from core.config_manager import Config

from widgets.card import Card
from widgets.title_label import TitleLabel
from widgets.camera_preview import CameraPreview
from widgets.sensor_card import SensorCard
from widgets.dashboard_toolbar import DashboardToolbar


def get_daily_csv_path(mode):
    basePath = Config.get(
        "config",
        "recordingPath",
        default="/records"
    )

    basePath = Path(basePath)

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    dailyPath = (
            basePath /
            today /
            mode
    )

    dailyPath.mkdir(
        parents=True,
        exist_ok=True
    )

    return (
            dailyPath /
            "image_sensor.csv"
    )


def get_next_image_number(recordPath):

    existingImages = list(
        recordPath.glob("IMG_*.jpg")
    )

    if not existingImages:
        return 1

    numbers = []

    for imagePath in existingImages:

        try:

            number = int(
                imagePath.stem.replace(
                    "IMG_",
                    ""
                )
            )

            numbers.append(number)

        except ValueError:
            continue

    if not numbers:
        return 1

    return max(numbers) + 1


class Dashboard(QWidget):
    CAPTURE_DURATION = 3 * 60  # 3 menit
    CAPTURE_INTERVAL = 1000

    def __init__(self, serial):
        super().__init__()

        self.serial = serial

        self.setObjectName("DashboardPage")

        # ======================================================
        # STATE
        # ======================================================

        self.sensorCards = {}
        self.controlCards = {}

        self.cameraPreview = None
        self.toolbar = None

        self.isCapturing = False
        self.isAutoCapture = False

        self.currentRecordId = None
        self.currentRecordPath = None

        self.captureElapsed = 0
        self.imageIndex = 0

        self.latestSensorData = {}

        self.captureTimer = QTimer(self)

        self.captureTimer.setInterval(
            self.CAPTURE_INTERVAL
        )

        self.captureTimer.timeout.connect(
            self.capture_auto_image
        )

        # ======================================================
        # UI
        # ======================================================

        self.init_ui()

    # ==========================================================
    # UI
    # ==========================================================

    def init_ui(self):

        mainLayout = QVBoxLayout(self)

        mainLayout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        mainLayout.setSpacing(20)

        # ======================================================
        # HEADER
        # ======================================================

        headerCard = Card()

        title = TitleLabel(
            Config.get(
                "app",
                "windowTitle",
                default="ALAT IMAGE AND SENSOR RECORDING"
            )
        )

        headerCard.layout.addWidget(title)

        mainLayout.addWidget(headerCard)

        # ======================================================
        # CONTENT
        # ======================================================

        scrollArea = QScrollArea()

        scrollArea.setWidgetResizable(True)

        scrollArea.setFrameShape(
            QScrollArea.NoFrame
        )

        scrollArea.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        scrollWidget = QWidget()

        scrollWidget.setObjectName(
            "DashboardContent"
        )

        scrollWidget.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Minimum
        )

        contentLayout = QVBoxLayout(
            scrollWidget
        )

        contentLayout.setContentsMargins(
            8,
            8,
            8,
            8
        )

        contentLayout.setSpacing(20)

        contentLayout.setAlignment(
            Qt.AlignTop
        )

        scrollArea.setWidget(
            scrollWidget
        )

        mainLayout.addWidget(
            scrollArea,
            1
        )

        # ======================================================
        # CAMERA + SENSOR
        # ======================================================

        topGrid = QGridLayout()

        topGrid.setHorizontalSpacing(20)
        topGrid.setVerticalSpacing(20)

        # ------------------------------------------------------
        # CAMERA
        # ------------------------------------------------------

        self.cameraPreview = CameraPreview()

        topGrid.addWidget(
            self.cameraPreview,
            0,
            0,
            2,
            1
        )

        # ------------------------------------------------------
        # SENSOR CARDS
        # ------------------------------------------------------

        self.cardGrid = QGridLayout()

        self.cardGrid.setHorizontalSpacing(8)
        self.cardGrid.setVerticalSpacing(8)

        self.cardGrid.setContentsMargins(
            0,
            0,
            0,
            0
        )

        self.cardGrid.setAlignment(
            Qt.AlignTop
        )

        cards = Config.get("sensor", "cards", default=[])

        self.create_sensor_cards(cards)

        topGrid.addLayout(self.cardGrid, 0, 1, 2, 1, Qt.AlignTop)

        # ======================================================
        # COLUMN SIZE
        # ======================================================

        topGrid.setColumnStretch(
            0,
            7
        )

        topGrid.setColumnStretch(
            1,
            3
        )

        contentLayout.addLayout(
            topGrid
        )

        # ======================================================
        # RECORDING STATUS
        # ======================================================

        self.statusLabel = TitleLabel(
            "READY"
        )

        self.recordInfoLabel = TitleLabel(
            "Belum ada rekaman"
        )

        # ======================================================
        # TOOLBAR
        # ======================================================

        self.toolbar = DashboardToolbar()

        # Manual recording
        self.toolbar.startManualButton.clicked.connect(
            self.start_manual_capture
        )

        # Auto recording 3 menit
        self.toolbar.startAutoButton.clicked.connect(
            self.start_auto_capture
        )

        # Stop recording
        self.toolbar.stopRecordButton.clicked.connect(
            self.stop_capture
        )

        mainLayout.addWidget(
            self.toolbar
        )

        # ======================================================
        # INITIAL STATE
        # ======================================================

        self.set_recording_status(
            "READY",
            "Siap melakukan recording"
        )

    # ==========================================================
    # SENSOR CARDS
    # ==========================================================

    def create_sensor_cards(self, sensors):

        self.sensorCards.clear()

        columns = 2

        for index, sensor in enumerate(sensors):
            row = index // columns
            col = index % columns

            card = SensorCard(
                title=sensor["title"],
                value="--",
                unit=sensor["unit"],
            )

            self.sensorCards[
                sensor["key"]
            ] = card

            self.cardGrid.addWidget(
                card,
                row,
                col
            )

    # ==========================================================
    # SENSOR UPDATE
    # ==========================================================

    def process_packet(self, packet):

        packet_type = packet.get(
            "type"
        )

        # ======================================================
        # SENSOR
        # ======================================================

        if packet_type == "sensor":

            data = packet.get(
                "data",
                {}
            )

            self.update_sensor(
                data
            )

        # ======================================================
        # DEVICE STATUS
        # ======================================================

        elif packet_type == "status":

            status = packet.get(
                "status",
                "UNKNOWN"
            )

            self.set_recording_status(
                status,
                packet.get(
                    "message",
                    ""
                )
            )

    # ==========================================================
    # UPDATE SENSOR
    # ==========================================================

    def update_sensor(self, data):

        self.latestSensorData.update(
            data
        )

        for key, value in data.items():

            if key not in self.sensorCards:
                continue

            self.update_card(
                key,
                value
            )

    # ==========================================================
    # UPDATE CARD
    # ==========================================================

    def update_card(
            self,
            key,
            value
    ):

        if key not in self.sensorCards:
            return

        card = self.sensorCards[key]

        card.set_value(
            value,
            card.unit
            if hasattr(card, "unit")
            else ""
        )

    # ==========================================================
    # RECORD ID
    # ==========================================================

    def save_capture_data(
            self,
            mode,
            image_name,
            image_path
    ):

        csvPath = get_daily_csv_path(mode)

        fileExists = csvPath.exists()

        sensorKeys = list(
            self.latestSensorData.keys()
        )

        fieldnames = [
                         "image_name",
                         "image_path",
                         "timestamp",
                     ] + sensorKeys

        with open(
                csvPath,
                "a",
                newline="",
                encoding="utf-8"
        ) as csvFile:

            writer = csv.DictWriter(
                csvFile,
                fieldnames=fieldnames
            )

            if not fileExists:
                writer.writeheader()

            row = {
                "image_name":
                    image_name,

                "image_path":
                    str(image_path),

                "timestamp":
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
            }

            for key in sensorKeys:
                row[key] = (
                    self.latestSensorData.get(
                        key,
                        ""
                    )
                )

            writer.writerow(row)

    # ==========================================================
    # STATUS
    # ==========================================================

    def set_recording_status(
            self,
            status,
            message=""
    ):

        self.toolbar.statusLabel.setText(
            status
        )

        self.toolbar.recordInfoLabel.setText(
            message
        )

    def start_manual_capture(self):

        if self.isCapturing:
            return

        basePath = Config.get(
            "config",
            "recordingPath",
            default="/records"
        )

        today = datetime.now().strftime(
            "%Y-%m-%d"
        )

        recordPath = (
                Path(basePath) /
                today /
                "manual"
        )

        recordPath.mkdir(
            parents=True,
            exist_ok=True
        )

        self.currentRecordPath = recordPath

        # ======================================================
        # GET NEXT IMAGE NUMBER
        # ======================================================

        imageNumber = get_next_image_number(
            recordPath
        )

        imageName = (
            f"IMG_{imageNumber:04d}.jpg"
        )

        imagePath = (
                recordPath /
                imageName
        )

        # ======================================================
        # CAPTURE
        # ======================================================

        success = self.cameraPreview.capture_image(
            imagePath
        )

        if not success:
            self.set_recording_status(
                "ERROR",
                "Gagal mengambil gambar"
            )

            self.currentRecordPath = None

            return

        # ======================================================
        # SAVE SENSOR DATA
        # ======================================================

        self.save_capture_data(
            "manual",
            imageName,
            imagePath
        )

        self.set_recording_status(
            "CAPTURE BERHASIL",
            str(imagePath)
        )

        print(
            f"Manual capture: {imagePath}"
        )

        self.currentRecordPath = None

    def start_auto_capture(self):

        if self.isCapturing:
            return

        basePath = Config.get(
            "config",
            "recordingPath",
            default="/records"
        )

        today = datetime.now().strftime(
            "%Y-%m-%d"
        )

        recordPath = (
                Path(basePath) /
                today /
                "auto"
        )

        recordPath.mkdir(
            parents=True,
            exist_ok=True
        )

        self.isCapturing = True
        self.isAutoCapture = True

        self.currentRecordPath = recordPath

        self.captureElapsed = 0
        self.imageIndex = (
                get_next_image_number(
                    recordPath
                ) - 1
        )

        self.captureTimer.start()

        self.set_recording_status(
            "● AUTO CAPTURE",
            f"3 menit | {recordPath}"
        )

    def capture_auto_image(self):

        if not self.isCapturing:
            return

        imageNumber = self.imageIndex + 1

        imageName = (
            f"IMG_{imageNumber:04d}.jpg"
        )

        imagePath = (
                self.currentRecordPath /
                imageName
        )

        success = self.cameraPreview.capture_image(
            imagePath
        )

        if success:
            self.imageIndex += 1

            self.save_capture_data(
                "auto",
                imageName,
                imagePath
            )
            print(
                f"Auto capture: {imagePath}"
            )

        self.captureElapsed += 1

        minutes = self.captureElapsed // 60
        seconds = self.captureElapsed % 60

        elapsed = (
            f"{minutes:02d}:{seconds:02d}"
        )

        self.toolbar.statusLabel.setText(
            f"● AUTO CAPTURE | {elapsed}"
        )

        if self.captureElapsed >= self.CAPTURE_DURATION:
            self.stop_auto_capture()

    def stop_auto_capture(self):

        self.captureTimer.stop()

        recordPath = self.currentRecordPath

        totalImages = self.imageIndex

        self.isCapturing = False
        self.isAutoCapture = False

        self.set_recording_status(
            "CAPTURE SELESAI",
            f"{totalImages} gambar tersimpan"
        )

        self.toolbar.recordInfoLabel.setText(
            f"Tersimpan di: {recordPath}"
        )

        self.currentRecordId = None
        self.currentRecordPath = None

        self.captureElapsed = 0
        self.imageIndex = 0

    def stop_capture(self):

        if not self.isCapturing:
            return

        self.captureTimer.stop()

        recordPath = self.currentRecordPath
        totalImages = self.imageIndex

        self.isCapturing = False
        self.isAutoCapture = False

        self.set_recording_status(
            "CAPTURE DIHENTIKAN",
            f"{totalImages} gambar tersimpan"
        )

        self.toolbar.recordInfoLabel.setText(
            f"Tersimpan di: {recordPath}"
        )

        self.currentRecordId = None
        self.currentRecordPath = None
