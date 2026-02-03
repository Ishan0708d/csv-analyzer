from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from api import login, save_token


class Login(QWidget):
    def __init__(self, on_success, on_switch_register):
        super().__init__()
        self.on_success = on_success
        self.on_switch_register = on_switch_register

        layout = QVBoxLayout()

        self.user = QLineEdit()
        self.user.setPlaceholderText("Username")

        self.pw = QLineEdit()
        self.pw.setPlaceholderText("Password")
        self.pw.setEchoMode(QLineEdit.Password)

        self.msg = QLabel()

        btn = QPushButton("Login")
        btn.clicked.connect(self.handle_login)

        switch = QPushButton("Sign up")
        switch.clicked.connect(self.on_switch_register)

        layout.addWidget(self.user)
        layout.addWidget(self.pw)
        layout.addWidget(btn)
        layout.addWidget(switch)
        layout.addWidget(self.msg)

        self.setLayout(layout)

    def handle_login(self):
        token = login(self.user.text(), self.pw.text())
        if not token:
            self.msg.setText("Login failed")
            return
        save_token(token)
        self.on_success(token)
