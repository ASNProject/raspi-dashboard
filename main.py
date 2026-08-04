import sys
from PySide6.QtWidgets import QApplication

from screens.main_window import MainWindow
from screens.styles import load_stylesheet
from core.config_manager import Config


def main():
    app = QApplication(sys.argv)

    app.setStyleSheet(load_stylesheet())

    Config.load()

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
