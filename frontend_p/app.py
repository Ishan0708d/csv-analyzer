import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from api import load_token
from login import Login
from register import Register
from upload import Upload
from logout import Logout


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CSV Analyzer Desktop")
        self.resize(400, 500)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        token = load_token()
        if token:
            self.show_upload(token)
        else:
            self.show_login()

    def clear(self):
        while self.layout.count():
            self.layout.takeAt(0).widget().deleteLater()

    def show_login(self):
        self.clear()
        self.layout.addWidget(
            Login(self.show_upload, self.show_register)
        )

    def show_register(self):
        self.clear()
        self.layout.addWidget(
            Register(self.show_login)
        )

    def show_upload(self, token):
        self.clear()
        self.layout.addWidget(
            Upload(token, self.show_logout)
        )

    def show_logout(self):
        self.clear()
        self.layout.addWidget(
            Logout(self.show_login)
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Main()
    win.show()
    sys.exit(app.exec_())
