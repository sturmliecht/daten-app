import sqlite3
from pathlib import Path
from app.logik import namen_vergleichen

DB_PATH = Path(__file__).resolve().parent.parent / "daten.db"

def tabelle_anlegen():
    verbindung = sqlite3.connect(DB_PATH)
    try:
        verbindung.execute("""
            CREATE TABLE IF NOT EXISTS personen(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nachname TEXT NOT NULL,
                vorname TEXT NOT NULL,
                geburtsdatum TEXT NOT NULL,
                geschlecht TEXT NOT NULL CHECK(geschlecht IN ('m', 'w', 'd')),
                wohnort TEXT NOT NULL
            )
        """)
        verbindung.commit()
    finally:
        verbindung.close()



def eintrag_speichern(nachname, vorname, geburtsdatum, geschlecht, wohnort):
    verbindung = sqlite3.connect(DB_PATH)
    try:
        verbindung.execute(
            "INSERT INTO personen (nachname, vorname, geburtsdatum, geschlecht, wohnort) "
            "VALUES (?, ?, ?, ?, ?)",
            (nachname, vorname, geburtsdatum, geschlecht, wohnort)
        )
        verbindung.commit()
    finally:
        verbindung.close()


def eintraege_auslesen():
    verbindung = sqlite3.connect(DB_PATH)
    verbindung.create_collation("alphabetisch", namen_vergleichen )
    try:
        cursor = verbindung.execute(
            "SELECT id, nachname, vorname, geburtsdatum, geschlecht, wohnort "
            "FROM personen ORDER BY nachname COLLATE alphabetisch, vorname COLLATE alphabetisch"
        )
        return cursor.fetchall()
    finally:
        verbindung.close()