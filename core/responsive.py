from PySide6.QtCore import QObject


class Responsive(QObject):

    _window = None

    @classmethod
    def set_window(cls, window):
        cls._window = window

    # ==========================================
    # Window
    # ==========================================

    @classmethod
    def width(cls):

        if cls._window:
            return cls._window.width()

        return 1400

    @classmethod
    def height(cls):

        if cls._window:
            return cls._window.height()

        return 800

    # ==========================================
    # Sidebar
    # ==========================================

    @classmethod
    def sidebar_width(cls):

        width = int(cls.width() * 0.20)

        return max(180, min(width, 320))

    # ==========================================
    # Logo
    # ==========================================

    @classmethod
    def logo_size(cls):

        size = int(cls.sidebar_width() * 0.18)

        return max(40, min(size, 64))

    # ==========================================
    # Menu Button
    # ==========================================

    @classmethod
    def menu_height(cls):

        h = int(cls.height() * 0.06)

        return max(42, min(h, 60))

    # ==========================================
    # Font
    # ==========================================

    @classmethod
    def title_font(cls):

        return max(
            11,
            min(int(cls.width() / 120), 16),
        )

    @classmethod
    def subtitle_font(cls):

        return max(
            8,
            min(int(cls.width() / 180), 11),
        )

    # ==========================================
    # Dashboard
    # ==========================================

    @classmethod
    def card_columns(cls):

        w = cls.width()

        if w <= 800:
            return 2

        elif w <= 1280:
            return 3

        return 4

    @classmethod
    def card_height(cls):

        h = int(cls.height() * 0.16)

        return max(120, min(h, 170))

    @classmethod
    def camera_height(cls):

        h = int(cls.height() * 0.38)

        return max(180, min(h, 360))

    @classmethod
    def chart_height(cls):

        return cls.camera_height()

    @classmethod
    def toolbar_height(cls):

        h = int(cls.height() * 0.07)

        return max(48, min(h, 70))