from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QMessageBox, QHBoxLayout, QLabel, QGroupBox
)
import sqlite3

from database import DB_NAME
from utils import iso_to_de, hex_to_qcolor
from brief_detail import BriefDetail


class BriefApp(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Meine Briefe")
        self.resize(1000, 600)

        main_layout = QVBoxLayout(self)

        ### 📊 Tabelle
        table_group = QGroupBox("Meine Briefe")
        table_layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            "ID", "Erhalt", "Verarbeitet", "Frist", "Typ", "Absender/Empfänger",
            "Betreff", "Notizen", "Kategorie", "Erledigt"
        ])
        self.table.setColumnHidden(0, True)
        self.table.cellDoubleClicked.connect(self.open_edit_brief)
        table_layout.addWidget(self.table)
        table_group.setLayout(table_layout)

        ### 🧩 Buttons
        btn_layout = QHBoxLayout()
        self.new_btn = QPushButton("Neuen Brief erfassen")
        self.new_btn.clicked.connect(self.open_new_brief)
        self.logout_btn = QPushButton("Logout")
        self.logout_btn.clicked.connect(self.logout)
        btn_layout.addWidget(self.new_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.logout_btn)

        main_layout.addWidget(table_group)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

        ### Initial
        self.check_erinnerungen()
        self.load_data()

    def load_data(self):
        self.table.setRowCount(0)
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("""
            SELECT b.id, b.datum_erhalt, b.datum_verarbeitet, b.datum_frist,
                   b.typ, b.absender_empfaenger, b.betreff, b.notizen,
                   k.name, b.erledigt, k.color
            FROM briefe b
            LEFT JOIN kategorien k ON b.kategorie_id = k.id
            WHERE b.user_id=?
            ORDER BY b.datum_frist ASC
        """, (self.user_id,))
        for row_idx, row in enumerate(c.fetchall()):
            self.table.insertRow(row_idx)
            for col_idx, value in enumerate(row[:-1]):  # letzte Spalte: Farbe
                if col_idx in [1, 2, 3]:
                    display = iso_to_de(value)
                elif col_idx == 9:
                    display = "✅" if value else "❌"
                else:
                    display = str(value)
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(display))
            color = row[-1]
            if color:
                for col_idx in range(self.table.columnCount()):
                    self.table.item(row_idx, col_idx).setBackground(hex_to_qcolor(color))
        conn.close()

    def open_new_brief(self):
        self.open_detail_window()

    def open_edit_brief(self, row, column):
        brief_id_item = self.table.item(row, 0)
        if brief_id_item:
            self.open_detail_window(int(brief_id_item.text()))

    def open_detail_window(self, brief_id=None):
        self.detail_window = BriefDetail(self.user_id, brief_id, on_save=self.load_data)
        self.detail_window.show()

    def check_erinnerungen(self):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("""
            SELECT betreff, datum_frist
            FROM briefe
            WHERE user_id=? AND erledigt=0 AND datum_frist<=date('now')
        """, (self.user_id,))
        offene = c.fetchall()
        conn.close()
        if offene:
            msg = "\n".join(f"{betreff} (Frist: {iso_to_de(datum_frist)})" for betreff, datum_frist in offene)
            QMessageBox.warning(self, "Offene Briefe", f"Diese Briefe sind noch nicht erledigt:\n\n{msg}")

    def logout(self):
        self.close()
        from login import LoginDialog
        dlg = LoginDialog()
        if dlg.exec_():
            if dlg.is_admin:
                from admin_panel import AdminPanel
                admin = AdminPanel()
                admin.show()
            else:
                new_window = BriefApp(dlg.user_id)
                new_window.show()
