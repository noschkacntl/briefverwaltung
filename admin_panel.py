from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QInputDialog, QColorDialog, QMessageBox
)
from PyQt5.QtGui import QColor
import sqlite3

from database import DB_NAME
from utils import hex_to_qcolor, qcolor_to_hex

class AdminPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Settings")
        self.resize(900, 700)

        layout = QVBoxLayout(self)

        # Benutzerverwaltung
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(3)
        self.user_table.setHorizontalHeaderLabels(["ID", "Username", "Admin?"])
        self.load_users()

        self.add_user_btn = QPushButton("Benutzer hinzufügen")
        self.del_user_btn = QPushButton("Benutzer löschen")

        self.add_user_btn.clicked.connect(self.add_user)
        self.del_user_btn.clicked.connect(self.del_user)

        # Briefe
        self.brief_table = QTableWidget()
        self.brief_table.setColumnCount(6)
        self.brief_table.setHorizontalHeaderLabels([
            "ID", "Betreff", "Absender/Empfänger", "Erledigt", "User-ID", "Kategorie-ID"
        ])
        self.load_briefs()

        self.del_brief_btn = QPushButton("Brief löschen")
        self.del_brief_btn.clicked.connect(self.del_brief)

        # Kategorien
        self.kategorie_table = QTableWidget()
        self.kategorie_table.setColumnCount(3)
        self.kategorie_table.setHorizontalHeaderLabels(["ID", "Name", "Farbe"])
        self.load_kategorien()

        self.add_kategorie_btn = QPushButton("Kategorie hinzufügen")
        self.del_kategorie_btn = QPushButton("Kategorie löschen")

        self.add_kategorie_btn.clicked.connect(self.add_kategorie)
        self.del_kategorie_btn.clicked.connect(self.del_kategorie)

        layout.addWidget(QLabel("Benutzerverwaltung"))
        layout.addWidget(self.user_table)
        layout.addWidget(self.add_user_btn)
        layout.addWidget(self.del_user_btn)

        layout.addWidget(QLabel("Briefverwaltung"))
        layout.addWidget(self.brief_table)
        layout.addWidget(self.del_brief_btn)

        layout.addWidget(QLabel("Kategorienverwaltung"))
        layout.addWidget(self.kategorie_table)
        layout.addWidget(self.add_kategorie_btn)
        layout.addWidget(self.del_kategorie_btn)

        self.setLayout(layout)

    def load_users(self):
        self.user_table.setRowCount(0)
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT id, username, is_admin FROM users")
        for row_idx, row_data in enumerate(c.fetchall()):
            self.user_table.insertRow(row_idx)
            for col_idx, item in enumerate(row_data):
                self.user_table.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))
        conn.close()

    def add_user(self):
        username, ok1 = QInputDialog.getText(self, "Benutzername", "Benutzername:")
        password, ok2 = QInputDialog.getText(self, "Passwort", "Passwort:")
        if ok1 and ok2:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            try:
                c.execute(
                    "INSERT INTO users (username, password, is_admin) VALUES (?, ?, 0)",
                    (username, password)
                )
                conn.commit()
                self.load_users()
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, "Fehler", "Benutzername existiert bereits.")
            conn.close()

    def del_user(self):
        row = self.user_table.currentRow()
        if row >= 0:
            user_id = self.user_table.item(row, 0).text()
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("DELETE FROM users WHERE id=?", (user_id,))
            conn.commit()
            conn.close()
            self.load_users()

    def load_briefs(self):
        self.brief_table.setRowCount(0)
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("""
            SELECT id, betreff, absender_empfaenger, erledigt, user_id, kategorie_id
            FROM briefe
        """)
        for row_idx, row_data in enumerate(c.fetchall()):
            self.brief_table.insertRow(row_idx)
            for col_idx, item in enumerate(row_data):
                if col_idx == 3:
                    display = "✅" if item else "❌"
                else:
                    display = str(item)
                self.brief_table.setItem(row_idx, col_idx, QTableWidgetItem(display))
        conn.close()

    def del_brief(self):
        row = self.brief_table.currentRow()
        if row >= 0:
            brief_id = self.brief_table.item(row, 0).text()
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("DELETE FROM briefe WHERE id=?", (brief_id,))
            conn.commit()
            conn.close()
            self.load_briefs()

    def load_kategorien(self):
        self.kategorie_table.setRowCount(0)
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT id, name, color FROM kategorien")
        for row_idx, row_data in enumerate(c.fetchall()):
            self.kategorie_table.insertRow(row_idx)
            for col_idx, item in enumerate(row_data):
                if col_idx == 2:  # Farbe
                    color_item = QTableWidgetItem()
                    color_item.setBackground(hex_to_qcolor(item))
                    color_item.setText(item)
                    self.kategorie_table.setItem(row_idx, col_idx, color_item)
                else:
                    self.kategorie_table.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))
        conn.close()

    def add_kategorie(self):
        name, ok1 = QInputDialog.getText(self, "Kategorie", "Name der Kategorie:")
        if ok1 and name:
            color = QColorDialog.getColor(QColor("#FFFFFF"), self, "Wähle eine Farbe")
            if color.isValid():
                hex_color = qcolor_to_hex(color)
                conn = sqlite3.connect(DB_NAME)
                c = conn.cursor()
                try:
                    c.execute(
                        "INSERT INTO kategorien (name, color) VALUES (?, ?)",
                        (name, hex_color)
                    )
                    conn.commit()
                    self.load_kategorien()
                except sqlite3.IntegrityError:
                    QMessageBox.warning(self, "Fehler", "Kategorie existiert bereits.")
                conn.close()

    def del_kategorie(self):
        row = self.kategorie_table.currentRow()
        if row >= 0:
            kat_id = self.kategorie_table.item(row, 0).text()
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("DELETE FROM kategorien WHERE id=?", (kat_id,))
            conn.commit()
            conn.close()
            self.load_kategorien()
