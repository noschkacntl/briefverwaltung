from PyQt5.QtWidgets import (
    QWidget, QFormLayout, QVBoxLayout, QDateEdit, QComboBox, QLineEdit, QTextEdit,
    QCheckBox, QPushButton, QMessageBox
)
from PyQt5.QtCore import QDate
import sqlite3

from database import DB_NAME
from utils import iso_to_de

class BriefDetail(QWidget):
    def __init__(self, user_id, brief_id=None, on_save=None):
        """
        :param user_id: ID des aktuellen Users
        :param brief_id: Optional: ID des Briefs (für Bearbeiten)
        :param on_save: Callback nach Speichern, um Liste zu aktualisieren
        """
        super().__init__()
        self.user_id = user_id
        self.brief_id = brief_id
        self.on_save = on_save

        self.setWindowTitle("Brief erfassen" if not self.brief_id else "Brief bearbeiten")
        self.resize(500, 600)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        today = QDate.currentDate()

        self.datum_erhalt = QDateEdit(today)
        self.datum_erhalt.setDisplayFormat("dd.MM.yyyy")

        self.datum_verarbeitet = QDateEdit(today)
        self.datum_verarbeitet.setDisplayFormat("dd.MM.yyyy")

        self.datum_frist = QDateEdit(today)
        self.datum_frist.setDisplayFormat("dd.MM.yyyy")

        self.typ_input = QComboBox()
        self.typ_input.addItems(["Eingang", "Ausgang"])

        self.ae_input = QLineEdit()
        self.betreff_input = QLineEdit()
        self.notizen_input = QTextEdit()
        self.kategorie_input = QComboBox()
        self.erledigt_checkbox = QCheckBox("Erledigt")

        form.addRow("Datum Erhalt:", self.datum_erhalt)
        form.addRow("Datum verarbeitet:", self.datum_verarbeitet)
        form.addRow("Frist-Datum:", self.datum_frist)
        form.addRow("Typ:", self.typ_input)
        form.addRow("Absender/Empfänger:", self.ae_input)
        form.addRow("Betreff:", self.betreff_input)
        form.addRow("Notizen:", self.notizen_input)
        form.addRow("Kategorie:", self.kategorie_input)
        form.addRow(self.erledigt_checkbox)

        layout.addLayout(form)

        btn = QPushButton("Speichern")
        btn.clicked.connect(self.save_brief)
        layout.addWidget(btn)

        self.load_kategorien()

        if self.brief_id:
            self.load_brief()

    def load_kategorien(self):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT id, name FROM kategorien")
        self.kategorien = {name: kid for kid, name in c.fetchall()}
        self.kategorie_input.addItems(self.kategorien.keys())
        conn.close()

    def load_brief(self):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("""
            SELECT datum_erhalt, datum_verarbeitet, datum_frist,
                   typ, absender_empfaenger, betreff, notizen,
                   erledigt, kategorie_id
            FROM briefe WHERE id=?
        """, (self.brief_id,))
        row = c.fetchone()
        conn.close()

        if row:
            erh, ver, frist, typ, ae, betreff, notizen, erledigt, kategorie_id = row
            self.datum_erhalt.setDate(QDate.fromString(erh, "yyyy-MM-dd"))
            self.datum_verarbeitet.setDate(QDate.fromString(ver, "yyyy-MM-dd"))
            self.datum_frist.setDate(QDate.fromString(frist, "yyyy-MM-dd"))
            self.typ_input.setCurrentText(typ)
            self.ae_input.setText(ae)
            self.betreff_input.setText(betreff)
            self.notizen_input.setPlainText(notizen)
            self.erledigt_checkbox.setChecked(bool(erledigt))
            for idx, (name, kid) in enumerate(self.kategorien.items()):
                if kid == kategorie_id:
                    self.kategorie_input.setCurrentIndex(idx)
                    break

    def save_brief(self):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        data = (
            self.datum_erhalt.date().toString("yyyy-MM-dd"),
            self.datum_verarbeitet.date().toString("yyyy-MM-dd"),
            self.datum_frist.date().toString("yyyy-MM-dd"),
            self.typ_input.currentText(),
            self.ae_input.text(),
            self.betreff_input.text(),
            self.notizen_input.toPlainText(),
            int(self.erledigt_checkbox.isChecked()),
            self.user_id,
            self.kategorien[self.kategorie_input.currentText()]
        )

        if self.brief_id:
            c.execute("""
                UPDATE briefe SET
                    datum_erhalt=?, datum_verarbeitet=?, datum_frist=?,
                    typ=?, absender_empfaenger=?, betreff=?, notizen=?,
                    erledigt=?, user_id=?, kategorie_id=?
                WHERE id=?
            """, (*data, self.brief_id))
        else:
            c.execute("""
                INSERT INTO briefe (
                    datum_erhalt, datum_verarbeitet, datum_frist,
                    typ, absender_empfaenger, betreff, notizen,
                    erledigt, user_id, kategorie_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, data)

        conn.commit()
        conn.close()

        if self.on_save:
            self.on_save()
        self.close()
