from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QStackedWidget,
)

from PySide6.QtCore import QThread, QTimer

from core.config_manager import Config
from core.responsive import Responsive
from core.serial_manager import SerialManager

from widgets.sidebar import Sidebar

from screens.sidebar.dashboard import Dashboard
from screens.sidebar.camera import CameraPage
from screens.sidebar.sensor import SensorPage
from screens.sidebar.control import ControlPage
from screens.sidebar.settings import SettingsPage

import logging


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.sidebar = None
        self.pages = None
        self.pageMap = {}

        # =============================
        # SERIAL
        # =============================

        self.serial = SerialManager()

        self.serial.packetReceived.connect(
            self.packet_received
        )

        self.thread = QThread()

        self.serial.moveToThread(self.thread)
        self.thread.started.connect(self.serial.start)

        # =============================
        # UI
        # =============================

        self.init_ui()

    # ==========================================================
    # UI
    # ==========================================================

    def init_ui(self):

        self.setWindowTitle(
            Config.get(
                "app",
                "windowTitle",
            )
        )

        self.resize(
            Config.get(
                "app",
                "windowWidth",
            ),
            Config.get(
                "app",
                "windowHeight",
            ),
        )

        # ==========================================
        # Central Widget
        # ==========================================

        central = QWidget()

        self.setCentralWidget(
            central
        )

        # Responsive menggunakan ukuran MainWindow
        Responsive.set_window(self)

        layout = QHBoxLayout(central)

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(0)

        # ==========================================
        # Sidebar
        # ==========================================

        self.sidebar = Sidebar(self.serial)

        layout.addWidget(
            self.sidebar,
            0,
        )

        # ==========================================
        # Stack Widget
        # ==========================================

        self.pages = QStackedWidget()

        layout.addWidget(
            self.pages,
            1,
        )

        # ==========================================
        # Register Pages
        # ==========================================

        self.add_page(
            "dashboard",
            Dashboard(
                serial=self.serial
            ),
        )

        self.add_page(
            "camera",
            CameraPage(),
        )

        self.add_page(
            "sensor",
            SensorPage(),
        )

        self.add_page(
            "control",
            ControlPage(),
        )

        self.add_page(
            "settings",
            SettingsPage(),
        )

        # ==========================================
        # Navigation
        # ==========================================

        self.bind_navigation()

        self.show_page(
            "dashboard",
        )

    # ==========================================================
    # REGISTER PAGE
    # ==========================================================

    def add_page(
            self,
            name,
            page,
    ):

        self.pageMap[name] = page

        self.pages.addWidget(page)

    # ==========================================================
    # SHOW PAGE
    # ==========================================================

    def show_page(
            self,
            name,
    ):

        page = self.pageMap.get(name)

        if page:
            self.pages.setCurrentWidget(page)

    # ==========================================================
    # NAVIGATION
    # ==========================================================

    def bind_navigation(self):

        navigation = {

            self.sidebar.dashboardButton: "dashboard",

            # self.sidebar.cameraButton: "camera",
            # self.sidebar.sensorButton: "sensor",
            # self.sidebar.controlButton: "control",
            # self.sidebar.settingButton: "settings",

        }

        for button, page in navigation.items():
            button.clicked.connect(

                lambda checked=False,
                       p=page: self.show_page(p)

            )

    # ==========================================================
    # RESPONSIVE
    # ==========================================================

    def resizeEvent(self, event):

        super().resizeEvent(event)

        Responsive.set_window(self)

        # Update Sidebar
        if hasattr(
                self.sidebar,
                "update_responsive",
        ):
            self.sidebar.update_responsive()

        # Update Semua Halaman
        for page in self.pageMap.values():

            if hasattr(
                    page,
                    "update_responsive",
            ):
                page.update_responsive()

    def packet_received(self, data):

        logging.info(data)
        print(data)

        dashboard = self.pageMap["dashboard"]

        dashboard.process_packet(data)

    def stop_serial(self):

        self.serial.disconnect()

        if self.thread.isRunning():
            self.thread.quit()

            self.thread.wait()

    def start_serial(self, port, baudrate):

        logging.info("START SERIAL")
        print("START SERIAL")

        self.serial.open(port, baudrate)

        logging.info("RUNNING:", self.serial.running)
        print("RUNNING:", self.serial.running)

        if self.serial.running and not self.thread.isRunning():
            self.thread.start()

    def showEvent(self, event):

        super().showEvent(event)
        logging.info("SHOW EVENT")
        print("SHOW EVENT")

        serialConfig = Config.get("config")
        logging.info("Serial Config:", serialConfig)
        print("Serial Config:", serialConfig)

        if serialConfig.get("autoConnect", True):
            QTimer.singleShot(
                3000,
                lambda: self.start_serial(
                    serialConfig["port"],
                    serialConfig["baudrate"],
                )
            )
