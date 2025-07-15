import sqlite3

DB_NAME = "briefe.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Users
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0
        )
    """)

    # Kategorien
    c.execute("""
        CREATE TABLE IF NOT EXISTS kategorien (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            color TEXT
        )
    """)

    # Briefe
    c.execute("""
        CREATE TABLE IF NOT EXISTS briefe (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datum_erhalt TEXT,
            datum_verarbeitet TEXT,
            datum_frist TEXT,
            typ TEXT,
            absender_empfaenger TEXT,
            betreff TEXT,
            notizen TEXT,
            erledigt INTEGER DEFAULT 0,
            user_id INTEGER,
            kategorie_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(kategorie_id) REFERENCES kategorien(id)
        )
    """)

    # Prüfe, ob ein Admin existiert
    c.execute("SELECT * FROM users WHERE is_admin=1")
    if not c.fetchone():
        c.execute("""
            INSERT INTO users (username, password, is_admin) VALUES (?, ?, 1)
        """, ("admin", "admin"))

    # Prüfe, ob es Standardkategorien gibt
    c.execute("SELECT * FROM kategorien")
    if not c.fetchone():
        c.execute("INSERT INTO kategorien (name, color) VALUES (?, ?)", ("Allgemein", "#FFFFFF"))

    conn.commit()
    conn.close()
