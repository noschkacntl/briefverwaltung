from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QMessageBox
import sqlite3
from database import DB_NAME

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.resize(300, 150)

        layout = QFormLayout(self)
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_btn = QPushButton("Login")

        layout.addRow("Benutzername:", self.username_input)
        layout.addRow("Passwort:", self.password_input)
        layout.addRow(self.login_btn)

        self.setLayout(layout)

        self.login_btn.clicked.connect(self.try_login)

        self.user_id = None
        self.is_admin = False

    def try_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT id, is_admin FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            self.user_id = user[0]
            self.is_admin = bool(user[1])
            self.accept()
        else:
            QMessageBox.warning(self, "Fehler", "Login fehlgeschlagen.")
