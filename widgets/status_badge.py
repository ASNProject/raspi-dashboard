from PySide6.QtWidgets import QLabel


class StatusBadge(QLabel):

    def __init__(self, text="OFFLINE"):

        super().__init__(text)

        self.setObjectName("StatusOffline")

    def online(self):

        self.setText("ONLINE")

        self.setObjectName("StatusOnline")

        self.style().polish(self)

    def offline(self):

        self.setText("OFFLINE")

        self.setObjectName("StatusOffline")

        self.style().polish(self)