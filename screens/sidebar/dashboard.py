from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QScrollArea,
)
from PySide6.QtCore import Qt

from core.config_manager import Config
from core.dummy_data import DummyData
from PySide6.QtWidgets import QSizePolicy

from widgets.card import Card
from widgets.title_label import TitleLabel
from widgets.camera_preview import CameraPreview
from widgets.sensor_chart import SensorChart
from widgets.sensor_card import SensorCard
from widgets.dashboard_toolbar import DashboardToolbar
from widgets.control_card import ControlCard
from PySide6.QtWidgets import QScrollArea


class Dashboard(QWidget):

    def __init__(self, serial):
        super().__init__()

        self.serial = serial

        self.controlCards = None
        self.controlGrid = None
        self.cardGrid = None
        self.setObjectName("DashboardPage")

        self.sensorCards = {}

        self.sensorChart = None
        self.cameraPreview = None
        self.toolbar = None
        self.dummy = None

        self.init_ui()

    def init_ui(self):

        mainLayout = QVBoxLayout(self)

        mainLayout.setContentsMargins(20, 20, 20, 20)
        mainLayout.setSpacing(20)

        # ======================================================
        # HEADER
        # ======================================================

        headerCard = Card()

        title = TitleLabel(
            Config.get(
                "app",
                "windowTitle",
                default="Panzer Dashboard",
            )
        )

        headerCard.layout.addWidget(title)

        mainLayout.addWidget(headerCard, 0)

        # ======================================================
        # CONTENT SCROLL
        # ======================================================

        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setFrameShape(QScrollArea.NoFrame)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        scrollWidget = QWidget()
        scrollWidget.setObjectName("DashboardContent")

        scrollWidget.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Minimum
        )

        contentLayout = QVBoxLayout(scrollWidget)
        contentLayout.setContentsMargins(8, 8, 8, 8)
        contentLayout.setSpacing(20)
        contentLayout.setAlignment(Qt.AlignTop)

        contentLayout.setSpacing(20)

        scrollArea.setWidget(scrollWidget)

        mainLayout.addWidget(scrollArea, 1)

        # ======================================================
        # CAMERA + CHART
        # ======================================================

        topGrid = QGridLayout()

        topGrid.setHorizontalSpacing(20)
        topGrid.setVerticalSpacing(20)

        self.cameraPreview = CameraPreview()
        self.sensorChart = SensorChart()

        topGrid.addWidget(self.cameraPreview, 0, 0)
        topGrid.addWidget(self.sensorChart, 0, 1)

        topGrid.setColumnStretch(0, 4)
        topGrid.setColumnStretch(1, 6)

        contentLayout.addLayout(topGrid)

        # ======================================================
        # SENSOR CARDS
        # ======================================================

        self.cardGrid = QGridLayout()

        self.cardGrid.setHorizontalSpacing(15)
        self.cardGrid.setVerticalSpacing(15)

        cards = Config.get(
            "sensor",
            "cards",
            default=[]
        )

        self.create_sensor_cards(cards)

        contentLayout.addLayout(self.cardGrid)

        # ======================================================
        # CONTROL CARD
        # ======================================================

        self.controlGrid = QGridLayout()
        self.controlGrid.setSpacing(15)

        controls = Config.get(
            "control",
            "cards",
            default=[],
        )

        self.create_control_cards(
            controls
        )

        print("Controls", controls)

        contentLayout.addLayout(self.controlGrid)

        # ======================================================
        # TOOLBAR
        # ======================================================

        self.toolbar = DashboardToolbar()

        self.toolbar.startButton.clicked.connect(
            self.cameraPreview.start_camera
        )

        self.toolbar.stopButton.clicked.connect(
            self.cameraPreview.stop_camera
        )

        mainLayout.addWidget(self.toolbar, 0)

        # ======================================================
        # DUMMY
        # ======================================================

        self.dummy = DummyData()

        self.dummy.sensorChanged.connect(
            self.update_sensor
        )

        self.dummy.fpsChanged.connect(
            self.update_fps
        )

        self.dummy.start()

    # ==========================================================
    # CREATE CARD
    # ==========================================================

    def create_sensor_cards(self, sensors):

        self.sensorCards.clear()

        columns = 4

        row = 0
        col = 0

        for sensor in sensors:

            card = SensorCard(
                title=sensor["title"],
                value="--",
                unit=sensor["unit"],
            )

            self.sensorCards[sensor["key"]] = card

            self.cardGrid.addWidget(card, row, col)

            col += 1

            if col >= columns:
                col = 0
                row += 1

    # ==========================================================
    # UPDATE SENSOR
    # ==========================================================

    def update_sensor(
            self,
            temp,
            hum,
            gas,
    ):

        values = {
            "temperature": temp,
            "humidity": hum,
            "gas": gas,
        }

        self.sensorChart.update_data(values)

        self.update_card(
            "temperature",
            f"{temp:.1f}",
            "Normal" if temp < 30 else "Warning",
        )

        self.update_card(
            "humidity",
            f"{hum:.1f}",
            "Optimal" if hum < 70 else "High",
        )

        self.update_card(
            "gas",
            f"{gas:.0f}",
            "Safe" if gas < 250 else "Danger",
        )

    # ==========================================================
    # UPDATE FPS
    # ==========================================================

    def update_fps(self, fps):

        self.update_card(
            "fps",
            fps,
            "Connected",
        )

    # ==========================================================
    # ADD CARD RUNTIME
    # ==========================================================

    def add_sensor_card(self, key, title, unit):

        total = len(self.sensorCards)

        row = total // 4
        col = total % 4

        card = SensorCard(
            title=title,
            value="--",
            unit=unit,
        )

        self.sensorCards[key] = card

        self.cardGrid.addWidget(
            card,
            row,
            col,
        )

    def update_card(
            self,
            key,
            value,
            status=None,
    ):

        if key not in self.sensorCards:
            return

        card = self.sensorCards[key]

        unit = ""

        cards = Config.get(
            "sensor",
            "cards",
            default=[]
        )

        for sensor in cards:

            if sensor["key"] == key:
                unit = sensor["unit"]
                break

        if key == "fps":
            unit = "FPS"

        card.set_value(value, unit)

        if status:
            card.set_status(status)

    def create_control_cards(self, controls):

        self.controlCards = {}

        columns = 4

        for index, control in enumerate(controls):
            row = index // columns
            col = index % columns

            card = ControlCard(
                key=control["key"],
                title=control["title"],
                control_type=control.get("type", "switch"),
                state=control.get("default", False),
                button_text=control.get("text", "Execute"),
                value=control.get("value", None)
            )

            card.toggled.connect(self.control_changed)
            card.clicked.connect(self.control_pressed)

            self.controlCards[control.get("key", "")] = card

            self.controlGrid.addWidget(card, row, col)

    def control_changed(
            self,
            key,
            state,
    ):

        self.serial.send(
            {
                "type": "control",
                "key": key,
                "value": state,
            }
        )

    def control_pressed(self, key, value):

        self.serial.send({
            "type": "button",
            "key": key,
            "value": value,
        })

    def process_packet(self, packet):

        if packet.get("type") != "sensor":
            return

        data = packet.get("data", {})

        self.sensorChart.update_data(data)

        for key, value in data.items():

            self.update_card(
                key=key,
                value=value,
                status="Connected",
        )