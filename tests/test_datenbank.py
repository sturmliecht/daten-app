import sqlite3
import tempfile
import unittest
from pathlib import Path

from app import datenbank


class TestDatenbank(unittest.TestCase):

    def setUp(self):
        # Vor jedem Test: eigene, leere Testdatenbank in einem temporären Ordner
        self.temp_ordner = tempfile.TemporaryDirectory()
        self.originaler_pfad = datenbank.DB_PATH
        datenbank.DB_PATH = Path(self.temp_ordner.name) / "test.db"
        datenbank.tabelle_anlegen()

    def tearDown(self):
        # Nach jedem Test: echten Pfad wiederherstellen und Testdatenbank löschen
        datenbank.DB_PATH = self.originaler_pfad
        self.temp_ordner.cleanup()

    def test_neue_datenbank_ist_leer(self):
        self.assertEqual(datenbank.eintraege_auslesen(), [])


    def test_eintrag_speichern_und_auslesen(self):
        datenbank.eintrag_speichern("Muster", "Anna", "2004-03-15", "w", "Bern")

        eintraege = datenbank.eintraege_auslesen()

        self.assertEqual(len(eintraege), 1)
        self.assertEqual(eintraege[0], (1, "Muster", "Anna", "2004-03-15", "w", "Bern"))

    def test_eintraege_sind_nach_nachname_sortiert(self):
        datenbank.eintrag_speichern("Zürcher", "Lea", "1990-01-01", "w", "Basel")
        datenbank.eintrag_speichern("Ammann", "Tim", "1985-06-20", "m", "Thun")

        eintraege = datenbank.eintraege_auslesen()

        self.assertEqual(eintraege[0][1], "Ammann")
        self.assertEqual(eintraege[1][1], "Zürcher")

    def test_ungueltiges_geschlecht_wird_abgelehnt(self):
        with self.assertRaises(sqlite3.IntegrityError):
            datenbank.eintrag_speichern("Muster", "Anna", "2004-03-15", "x", "Bern")

    def test_nachnamen_werden_nach_umlaut_regel_sortiert(self):
        datenbank.eintrag_speichern("Meier", "Lena", "1990-01-01", "w", "Zürich")
        datenbank.eintrag_speichern("Zürcher", "Lea", "1990-01-01", "w", "Basel")
        datenbank.eintrag_speichern("Ärni", "Tim", "1985-06-20", "m", "Thun")
        datenbank.eintrag_speichern("von Gunten", "Max", "1985-06-20", "m", "Thun")
        datenbank.eintrag_speichern("Azzola", "Eva", "1990-01-01", "w", "Zürich")

        eintraege = datenbank.eintraege_auslesen()
        tatsaechlich = tuple([eintrag[1:3] for eintrag in eintraege])  # nur Nachname und Vorname
        erwartet = (("Azzola", "Eva"), ("Ärni", "Tim"), ("Meier", "Lena"), ("von Gunten", "Max"), ("Zürcher", "Lea"))

        self.assertEqual(tatsaechlich, erwartet)

    def test_vornamen_ohne_akzent_und_grossgeschrieben_zuerst(self):
        datenbank.eintrag_speichern("Müller", "hélène", "1990-01-01", "w", "Zürich")
        datenbank.eintrag_speichern("Müller", "Noël", "1990-01-01", "w", "Zürich")
        datenbank.eintrag_speichern("Müller", "ben", "1990-01-01", "m", "Zürich")
        datenbank.eintrag_speichern("Müller", "Helene", "1990-01-01", "w", "Zürich")
        datenbank.eintrag_speichern("Müller", "BEn", "1990-01-01", "m", "Zürich")
        datenbank.eintrag_speichern("Müller", "Hélène", "1990-01-01", "w", "Zürich")
        datenbank.eintrag_speichern("Müller", "Noel", "1990-01-01", "w", "Zürich")
        datenbank.eintrag_speichern("Müller", "helene", "1990-01-01", "w", "Zürich")
        datenbank.eintrag_speichern("Müller", "Ben", "1990-01-01", "m", "Zürich")

        eintraege = datenbank.eintraege_auslesen()
        tatsaechlich = tuple([eintrag[1:3] for eintrag in eintraege])  # nur Nachname und Vorname
        erwartet = (
            ("Müller", "BEn"), 
            ("Müller", "Ben"), 
            ("Müller", "ben"), 
            ("Müller", "Helene"), 
            ("Müller", "helene"), 
            ("Müller", "Hélène"), 
            ("Müller", "hélène"), 
            ("Müller", "Noel"), 
            ("Müller", "Noël"))

        self.assertEqual(tatsaechlich, erwartet)

if __name__ == "__main__":
    unittest.main()