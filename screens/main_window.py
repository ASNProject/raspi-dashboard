from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QStackedWidget,
)

from core.config_manager import Config
from core.responsive import Responsive
from core.serial_manager import SerialManager

from widgets.sidebar import Sidebar

from screens.sidebar.dashboard import Dashboard
from screens.sidebar.camera import CameraPage
from screens.sidebar.sensor import SensorPage
from screens.sidebar.control import ControlPage
from screens.sidebar.settings import SettingsPage


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.sidebar = None
        self.pages = None

        self.pageMap = {}

        self.serial = SerialManager()

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

        self.sidebar = Sidebar()

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