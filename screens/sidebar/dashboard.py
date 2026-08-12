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


class Dashboard(QWidget):

    RECORD_DURATION = 3 * 60  # 3 menit

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

        self.isRecording = False
        self.isAutoRecording = False

        self.currentRecordId = None
        self.currentRecordPath = None

        self.recordElapsed = 0

        # ======================================================
        # TIMER
        # ======================================================

        self.recordTimer = QTimer(self)
        self.recordTimer.setInterval(1000)
        self.recordTimer.timeout.connect(
            self.update_record_timer
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
            self.start_manual_record
        )

        # Auto recording 3 menit
        self.toolbar.startAutoButton.clicked.connect(
            self.start_auto_record
        )

        # Stop recording
        self.toolbar.stopRecordButton.clicked.connect(
            self.stop_record
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
    # START MANUAL
    # ==========================================================

    def start_manual_record(self):

        if self.isRecording:
            return

        self.start_recording(
            auto=False
        )

    # ==========================================================
    # START AUTO
    # ==========================================================

    def start_auto_record(self):

        if self.isRecording:
            return

        self.start_recording(
            auto=True
        )

    # ==========================================================
    # START RECORDING
    # ==========================================================

    def start_recording(
        self,
        auto=False
    ):

        if self.isRecording:
            return

        # ------------------------------------------------------
        # CREATE RECORD ID
        # ------------------------------------------------------

        record_id = self.generate_record_id()

        # ------------------------------------------------------
        # SSD PATH
        # ------------------------------------------------------

        basePath = Config.get(
            "config",
            "recordingPath",
            default="/records"
        )

        basePath = Path(
            basePath
        )

        recordPath = (
            basePath /
            record_id
        )

        recordPath.mkdir(
            parents=True,
            exist_ok=True
        )

        # ------------------------------------------------------
        # STATE
        # ------------------------------------------------------

        self.isRecording = True
        self.isAutoRecording = auto

        self.currentRecordId = record_id
        self.currentRecordPath = recordPath

        self.recordElapsed = 0

        # ------------------------------------------------------
        # CAMERA
        # ------------------------------------------------------

        self.cameraPreview.start_recording(
            str(recordPath)
        )

        # ------------------------------------------------------
        # SERIAL
        # ------------------------------------------------------

        self.serial.send(
            {
                "type": "record",
                "command": "start",
                "mode": "auto"
                if auto
                else "manual",
                "record_id": record_id,
            }
        )

        # ------------------------------------------------------
        # TIMER
        # ------------------------------------------------------

        self.recordTimer.start()

        # ------------------------------------------------------
        # STATUS
        # ------------------------------------------------------

        mode = (
            "AUTO - 3 MENIT"
            if auto
            else "MANUAL"
        )

        self.set_recording_status(
            "● RECORDING",
            f"{mode} | {record_id}"
        )

        self.toolbar.recordInfoLabel.setText(
            f"Folder: {recordPath}"
        )

    # ==========================================================
    # STOP RECORDING
    # ==========================================================

    def stop_record(self):

        if not self.isRecording:
            return

        # ------------------------------------------------------
        # STOP TIMER
        # ------------------------------------------------------

        self.recordTimer.stop()

        # ------------------------------------------------------
        # STOP CAMERA
        # ------------------------------------------------------

        self.cameraPreview.stop_recording()

        # ------------------------------------------------------
        # SERIAL
        # ------------------------------------------------------

        self.serial.send(
            {
                "type": "record",
                "command": "stop",
                "record_id": self.currentRecordId,
            }
        )

        # ------------------------------------------------------
        # STATUS
        # ------------------------------------------------------

        recordPath = self.currentRecordPath

        self.isRecording = False
        self.isAutoRecording = False

        self.set_recording_status(
            "RECORDING SELESAI",
            self.currentRecordId
        )

        self.toolbar.recordInfoLabel.setText(
            f"Tersimpan di: {recordPath}"
        )

        self.currentRecordId = None
        self.currentRecordPath = None

    # ==========================================================
    # RECORD TIMER
    # ==========================================================

    def update_record_timer(self):

        if not self.isRecording:
            return

        self.recordElapsed += 1

        minutes = self.recordElapsed // 60
        seconds = self.recordElapsed % 60

        elapsed = (
            f"{minutes:02d}:{seconds:02d}"
        )

        # ------------------------------------------------------
        # AUTO STOP 3 MENIT
        # ------------------------------------------------------

        if (
            self.isAutoRecording
            and self.recordElapsed >= self.RECORD_DURATION
        ):

            self.stop_record()

            return

        mode = (
            "AUTO"
            if self.isAutoRecording
            else "MANUAL"
        )

        self.toolbar.statusLabel.setText(
            f"● RECORDING | {mode} | {elapsed}"
        )

    # ==========================================================
    # RECORD ID
    # ==========================================================

    def generate_record_id(self):

        basePath = Config.get(
            "config",
            "recordingPath",
            default="/records"
        )
        basePath = Path(
            basePath
        )

        basePath.mkdir(
            parents=True,
            exist_ok=True
        )

        # ======================================================
        # DATE + TIME
        # ======================================================

        timestamp = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )

        # ======================================================
        # INDEX
        # ======================================================

        index = 1

        while True:

            record_id = (
                f"REC-{index:04d}_"
                f"{timestamp}"
            )

            recordPath = (
                basePath /
                record_id
            )

            if not recordPath.exists():
                return record_id

            index += 1

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
