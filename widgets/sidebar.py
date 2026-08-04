from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QButtonGroup, QSizePolicy
)

from core.config_manager import Config
from core.icon_manager import Icons
from widgets.connection_panel import ConnectionPanel
from core.responsive import Responsive
from widgets.system_panel import SystemPanel


class Sidebar(QWidget):

    def __init__(self):
        super().__init__()

        self.systemPanel = None
        self.logo = None
        self.subtitleLabel = None
        self.titleLabel = None
        self.menuButtons = None
        self.setObjectName("Sidebar")

        self.menuGroup = None

        self.dashboardButton = None
        self.cameraButton = None
        self.sensorButton = None
        self.controlButton = None
        self.settingButton = None

        self.connectionPanel = None

        self.init_ui()

    def init_ui(self):

        mainLayout = QVBoxLayout(self)

        mainLayout.setContentsMargins(20, 20, 20, 20)
        mainLayout.setSpacing(15)

        # =====================================================
        # HEADER
        # =====================================================

        header = QHBoxLayout()
        header.setSpacing(12)

        self.logo = QLabel()

        pixmap = QPixmap(
            Config.get("app", "sidebarLogo", default="")
        )

        self.titleLabel = QLabel(
            Config.get(
                "app",
                "sidebarName",
                default="PANZER"
            )
        )

        self.titleLabel.setWordWrap(True)

        self.titleLabel.setObjectName("Logo")

        self.subtitleLabel = QLabel(
            Config.get(
                "app",
                "sidebarSubtitle",
                default="Robotics Dashboard"
            )
        )

        self.subtitleLabel.setWordWrap(True)

        self.subtitleLabel.setObjectName("Subtitle")

        textLayout = QVBoxLayout()
        textLayout.setSpacing(2)

        textLayout.addWidget(self.titleLabel)
        textLayout.addWidget(self.subtitleLabel)

        header.addWidget(self.logo)
        header.addLayout(textLayout)

        mainLayout.addLayout(header)

        mainLayout.addSpacing(25)

        # =====================================================
        # MENU
        # =====================================================

        menuLayout = QVBoxLayout()
        menuLayout.setSpacing(18)

        self.dashboardButton = QPushButton("Dashboard")
        self.dashboardButton.setIcon(Icons.get("dashboard"))

        # self.cameraButton = QPushButton("Camera")
        # self.cameraButton.setIcon(Icons.get("camera"))

        # self.sensorButton = QPushButton("Sensor")
        # self.sensorButton.setIcon(Icons.get("sensor"))

        # self.controlButton = QPushButton("Control")
        # self.controlButton.setIcon(Icons.get("control"))

        # self.settingButton = QPushButton("Settings")
        # self.settingButton.setIcon(Icons.get("settings"))

        self.menuGroup = QButtonGroup(self)
        self.menuGroup.setExclusive(True)

        self.menuButtons = [
            self.dashboardButton,
            # self.cameraButton,
            # self.sensorButton,
            # self.controlButton,
            # self.settingButton,
        ]

        for button in self.menuButtons:
            button.setCheckable(True)

            button.setCursor(Qt.PointingHandCursor)

            button.setMinimumHeight(48)

            button.setIconSize(QSize(18, 18))

            button.setObjectName("SidebarButton")

            self.menuGroup.addButton(button)

            menuLayout.addWidget(button)

        self.dashboardButton.setChecked(True)

        mainLayout.addLayout(menuLayout)

        mainLayout.addStretch()

        # =====================================================
        # CONNECTION PANEL
        # =====================================================

        self.connectionPanel = ConnectionPanel()
        mainLayout.addWidget(self.connectionPanel)

        mainLayout.addSpacing(10)

        # =====================================================
        # SYSTEM PANEL
        # =====================================================

        self.systemPanel = SystemPanel()
        mainLayout.addWidget(self.systemPanel)

        self.setSizePolicy(
            QSizePolicy.Fixed,
            QSizePolicy.Expanding,
        )

        self.update_responsive()

    def update_responsive(self):

        sidebarWidth = Responsive.sidebar_width()

        logoSize = Responsive.logo_size()

        buttonHeight = Responsive.menu_height()

        self.setFixedWidth(
            sidebarWidth
        )

        # ============================================
        # Logo
        # ============================================

        pixmap = QPixmap(
            Config.get(
                "app",
                "sidebarLogo",
                default="",
            )
        )

        if not pixmap.isNull():
            self.logo.setPixmap(
                pixmap.scaled(
                    logoSize,
                    logoSize,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation,
                )
            )

        self.logo.setFixedSize(
            logoSize,
            logoSize,
        )

        # ============================================
        # Font Title
        # ============================================

        titleFont = self.titleLabel.font()
        titleFont.setPixelSize(
            max(
                16,
                int(sidebarWidth * 0.085),
            )
        )
        self.titleLabel.setFont(titleFont)

        # ============================================
        # Font Subtitle
        # ============================================

        subtitleFont = self.subtitleLabel.font()
        subtitleFont.setPixelSize(
            max(
                10,
                int(sidebarWidth * 0.045),
            )
        )
        self.subtitleLabel.setFont(subtitleFont)

        # ============================================
        # Menu
        # ============================================

        iconSize = max(
            18,
            int(buttonHeight * 0.45),
        )

        for button in self.menuButtons:
            button.setMinimumHeight(
                buttonHeight
            )

            button.setIconSize(
                QSize(
                    iconSize,
                    iconSize,
                )
            )

        if hasattr(self.connectionPanel, "update_responsive"):
            self.connectionPanel.update_responsive()

        if hasattr(self.systemPanel, "update_responsive"):
            self.systemPanel.update_responsive()
