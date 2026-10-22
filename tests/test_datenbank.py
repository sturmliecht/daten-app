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

    def test_eintreage_sind_nach_nachname_und_vorname_sortiert(self):
        datenbank.eintrag_speichern("Ärni", "Anna", "1995-05-10", "w", "Zürich")
        datenbank.eintrag_speichern("von Gunten", "ben", "1985-08-15", "w", "Basel")
        datenbank.eintrag_speichern("von Gunten", "Ben", "1990-02-20", "m", "Bern")
        datenbank.eintrag_speichern("von Gunten", "BEn", "1985-08-15", "w", "Basel")
        datenbank.eintrag_speichern("Meier", "Clara", "1985-08-15", "w", "Basel")

        eintraege = datenbank.eintraege_auslesen()

        self.assertEqual(eintraege[0][1], "Meier")
        self.assertEqual(eintraege[1][2], "BEn")
        self.assertEqual(eintraege[2][2], "Ben")
        self.assertEqual(eintraege[3][2], "ben")
        self.assertEqual(eintraege[4][1], "Ärni")

    def test_eintraege_sind_nach_nachname_und_vorname_sortiert_fail(self):
        datenbank.eintrag_speichern("aerni", "Anna", "1995-05-10", "w", "Zürich")
        datenbank.eintrag_speichern("von Gunten", "ben", "1985-08-15", "w", "Basel")
        datenbank.eintrag_speichern("von Gunten", "Ben", "1990-02-20", "m", "Bern")
        datenbank.eintrag_speichern("von Gunten", "BEn", "1985-08-15", "w", "Basel")
        datenbank.eintrag_speichern("Meier", "Clara", "1985-08-15", "w", "Basel")

        eintraege = datenbank.eintraege_auslesen()
        tatsaechlich = tuple([eintrag[1:3] for eintrag in eintraege])
        erwartet = (("aerni", "Anna"), ("Meier", "Clara"), ("von Gunten", "BEn"), ("von Gunten", "ben"), ("von Gunten", "Ben"))   # Nur Nachnname und Vorname für die Überprüfung

        self.assertNotEqual(tatsaechlich, erwartet)  # Test schlägt fehl, da die Sortierung nicht korrekt ist
  

if __name__ == "__main__":
    unittest.main()