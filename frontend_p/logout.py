from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from api import clear_token, clear_history


class Logout(QWidget):
    def __init__(self, on_done):
        super().__init__()
        self.on_done = on_done

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Logged out"))

        btn = QPushButton("Back to login")
        btn.clicked.connect(self.logout)

        layout.addWidget(btn)
        self.setLayout(layout)

    def logout(self):
        clear_token()
        clear_history()
        self.on_done()
