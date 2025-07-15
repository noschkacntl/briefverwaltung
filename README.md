# Briefverwaltung

Eine elegante, minimalistische Desktop-Anwendung für Windows zur Verwaltung von Briefen, mit Benutzer- und Kategorienverwaltung, Erinnerungen und Bearbeitungsfunktion.  
Entwickelt mit Python & PyQt5.

## Features

- Benutzerverwaltung (Admin & normale User)
- Kategorien mit Farbcodes (durch Admin pflegbar)
- Briefe mit:
  - Datum Erhalt
  - Datum verarbeitet
  - Fristdatum
  - Typ: Eingang / Ausgang
  - Kategorie
  - „Erledigt“-Status
- Erinnerungen bei offenen Briefen
- Minimalistisches und elegantes UI
- Getrennte Fenster für Liste und Bearbeiten
- `.exe`-Build für einfache Verteilung

## Installation (aus Quellcode)

### Voraussetzungen

- Windows 10/11
- Python 3.8 oder neuer
- Installierte Abhängigkeiten:
  ```bash
  pip install pyqt5
  ```
### Starten (Development)
- Repository/Ordner herunterladen
- Terminal in den Ordner öffnen
- Starten:
```bash 
python main.py
```

## Build .exe (optional)

### 1. PyInstaller installieren
```bash
pip install pyinstaller
```
### 2. `.exe` bauen
Wechsle in den Ordner, in dem `main.py` liegt, und führe aus:

```bash
python -m PyInstaller --noconsole --onefile --add-data "style.qss;." main.py
```

### 3. Ergebnis

Die Datei `dist/main.exe` kann umbenannt und auf anderen Rechnern gestartet werden.
Keine Python-Installation auf dem Zielrechner nötig.

## Dateien & Struktur

```
Briefverwaltung/
├── main.py                # Einstiegspunkt
├── database.py            # DB-Initialisierung & Migration
├── utils.py               # Hilfsfunktionen
├── models.py              # Datenmodelle
├── user_panel.py          # Brief-Liste (UI)
├── brief_detail.py        # Detailfenster (UI)
├── admin_panel.py         # Admin-Bereich (UI)
├── login.py               # Login-Fenster
├── style_minimal.qss      # Minimalistisches Stylesheet
├── README.md              # Dieses Dokument
```

## Benutzer

- Standard-Admin beim ersten Start

```
Benutzername: admin
Passwort: admin
```
- Admin kann neue Benutzer und Kategorien anlegen sowie Briefeinträge löschen-


## Lizenz

Dieses Projekt ist privat und für Lern- und Demonstrationszwecke gedacht. Eine kommerzielle Nutzung oder Weitergabe ohne Genehmigung ist nicht vorgesehen.

## Support

Wenn Fragen, Probleme oder Verbesserungsvorschläge bestehen, wenden Sie sich bitte an den Entwickler. Feedback ist jederzeit willkommen.

