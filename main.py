from PyQt5.QtWidgets import QApplication, QDialog
from database import init_db
from login import LoginDialog
from user_panel import BriefApp
from admin_panel import AdminPanel
import sys

if __name__ == "__main__":
    # Initialisiere Datenbank
    init_db()

    # Starte Qt App
    app = QApplication(sys.argv)
    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())


    while True:
        login = LoginDialog()
        if login.exec_() == QDialog.Accepted:
            if login.is_admin:
                window = AdminPanel()
            else:
                window = BriefApp(user_id=login.user_id)

            window.show()
            app.exec_()  # Starte Eventloop bis Fenster geschlossen wird
        else:
            break  # Login wurde abgebrochen — Programmende

    sys.exit()
