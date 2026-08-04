from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QMessageBox,
)

from widgets.card import Card
from core.system_manager import SystemManager
from core.responsive import Responsive


class SystemPanel(Card):

    def __init__(self):
        super().__init__()

        self.titleLabel = None
        self.autoStartButton = None
        self.restartButton = None
        self.rebootButton = None
        self.shutdownButton = None

        self.init_ui()

    # ==========================================================
    # UI
    # ==========================================================

    def init_ui(self):

        self.titleLabel = QLabel("System")
        self.titleLabel.setObjectName("CardTitle")

        self.layout.addWidget(self.titleLabel)

        self.autoStartButton = QPushButton()
        self.restartButton = QPushButton("Restart Dashboard")
        self.rebootButton = QPushButton("Restart Device")
        self.shutdownButton = QPushButton("Shutdown Device")

        self.layout.addWidget(self.autoStartButton)
        self.layout.addWidget(self.restartButton)
        self.layout.addWidget(self.rebootButton)
        self.layout.addWidget(self.shutdownButton)

        self.autoStartButton.clicked.connect(
            self.toggle_autostart
        )

        self.restartButton.clicked.connect(
            self.restart_dashboard
        )

        self.rebootButton.clicked.connect(
            self.reboot
        )

        self.shutdownButton.clicked.connect(
            self.shutdown
        )

        self.refresh_status()

        self.update_responsive()

    # ==========================================================
    # RESPONSIVE
    # ==========================================================

    def update_responsive(self):

        buttonHeight = Responsive.menu_height()

        titleFont = self.titleLabel.font()
        titleFont.setPixelSize(
            max(
                12,
                Responsive.title_font() - 2,
            )
        )

        self.titleLabel.setFont(titleFont)

        buttons = [
            self.autoStartButton,
            self.restartButton,
            self.rebootButton,
            self.shutdownButton,
        ]

        for button in buttons:
            button.setObjectName("ToolbarButton")
            button.setMinimumHeight(buttonHeight)

    # ==========================================================
    # STATUS
    # ==========================================================

    def refresh_status(self):

        if SystemManager.is_autostart_enabled():

            self.autoStartButton.setText(
                "Disable Auto Start"
            )

        else:

            self.autoStartButton.setText(
                "Enable Auto Start"
            )

    # ==========================================================
    # AUTO START
    # ==========================================================

    def toggle_autostart(self):

        enabled = SystemManager.is_autostart_enabled()

        if enabled:

            title = "Disable Auto Start"

            message = (
                "Disable Auto Start?\n\n"
                "Dashboard tidak akan berjalan otomatis saat boot."
            )

        else:

            title = "Enable Auto Start"

            message = (
                "Enable Auto Start?\n\n"
                "Dashboard akan otomatis berjalan saat Raspberry Pi boot."
            )

        reply = QMessageBox.question(
            self,
            title,
            message,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply != QMessageBox.Yes:
            return

        try:

            if enabled:

                SystemManager.disable_autostart()

            else:

                SystemManager.enable_autostart(
                    "assets/systemd/panzer-dashboard.service"
                )

            self.refresh_status()

            QMessageBox.information(
                self,
                "Success",
                "Configuration updated successfully.",
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                str(e),
            )

    # ==========================================================
    # RESTART DASHBOARD
    # ==========================================================

    def restart_dashboard(self):

        reply = QMessageBox.question(
            self,
            "Restart Dashboard",
            "Restart Panzer Dashboard?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply != QMessageBox.Yes:
            return

        SystemManager.restart_dashboard()

    # ==========================================================
    # REBOOT
    # ==========================================================

    def reboot(self):

        reply = QMessageBox.question(
            self,
            "Restart Device",
            "Restart Raspberry Pi?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply != QMessageBox.Yes:
            return

        SystemManager.reboot()

    # ==========================================================
    # SHUTDOWN
    # ==========================================================

    def shutdown(self):

        reply = QMessageBox.question(
            self,
            "Shutdown Device",
            "Shutdown Raspberry Pi?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply != QMessageBox.Yes:
            return

        SystemManager.shutdown()