from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from api import register


class Register(QWidget):
    def __init__(self, on_done):
        super().__init__()
        self.on_done = on_done

        layout = QVBoxLayout()

        self.user = QLineEdit()
        self.user.setPlaceholderText("Username")

        self.pw = QLineEdit()
        self.pw.setPlaceholderText("Password")
        self.pw.setEchoMode(QLineEdit.Password)

        self.msg = QLabel()

        btn = QPushButton("Create account")
        btn.clicked.connect(self.handle_register)

        layout.addWidget(self.user)
        layout.addWidget(self.pw)
        layout.addWidget(btn)
        layout.addWidget(self.msg)

        self.setLayout(layout)

    def handle_register(self):
        ok = register(self.user.text(), self.pw.text())
        if ok:
            self.msg.setText("Account created. Go login.")
            self.on_done()
        else:
            self.msg.setText("Registration failed")
