from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QVBoxLayout


class Card(QFrame):

    def __init__(self):

        super().__init__()

        self.setObjectName("Card")

        self.layout = QVBoxLayout()

        self.layout.setContentsMargins(15, 15, 15, 15)

        self.layout.setSpacing(8)

        self.setLayout(self.layout)