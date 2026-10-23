import unittest
from datetime import date

from app.logik import alter_berechnen, eingaben_pruefen, namen_vergleichen

HEUTE = date(2026, 10, 13)

class TestAlterBerechnen(unittest.TestCase):

    def test_geburtstag_schon_gewesen(self):
        alter = alter_berechnen(date(2004, 3, 15), heute=date(2026, 10, 13))
        self.assertEqual(alter, 22)

    def test_geburtstag_noch_nicht_gewesen(self):
        alter = alter_berechnen(date(2004, 12, 1), heute=date(2026, 10, 13))
        self.assertEqual(alter, 21)

    def test_genau_am_geburtstag(self):
        alter = alter_berechnen(date(2004, 10, 13), heute=date(2026, 10, 13))
        self.assertEqual(alter, 22)

    def test_einen_tag_vor_dem_geburtstag(self):
        alter = alter_berechnen(date(2004, 10, 14), heute=date(2026, 10, 13))
        self.assertEqual(alter, 21)


class TestEingabenPruefen(unittest.TestCase):

    def test_gueltige_eingaben(self):
        fehler, geburtsdatum = eingaben_pruefen("Muster", "Anna", "15.03.2004", "w", "Bern", heute=HEUTE)
        self.assertEqual(fehler, [])
        self.assertEqual(geburtsdatum, "2004-03-15")

    def test_alles_leer(self):
        fehler, geburtsdatum = eingaben_pruefen("", "", "", "", "", heute=HEUTE)
        self.assertEqual(len(fehler), 5)
        self.assertIsNone(geburtsdatum)

    def test_datum_existiert_nicht(self):
        fehler, _ = eingaben_pruefen("Muster", "Anna", "31.02.2004", "w", "Bern", heute=HEUTE)
        self.assertEqual(len(fehler), 1)
        self.assertIn("ungültig", fehler[0])

    def test_falsches_datumsformat(self):
        fehler, _ = eingaben_pruefen("Muster", "Anna", "2004-03-15", "w", "Bern", heute=HEUTE)
        self.assertEqual(len(fehler), 1)
        self.assertIn("ungültig", fehler[0])

    def test_datum_in_der_zukunft(self):
        fehler, _ = eingaben_pruefen("Muster", "Anna", "14.10.2026", "w", "Bern", heute=HEUTE)
        self.assertEqual(len(fehler), 1)
        self.assertIn("Zukunft", fehler[0])

    def test_heute_geboren_ist_gueltig(self):
        fehler, _ = eingaben_pruefen("Muster", "Anna", "13.10.2026", "w", "Bern", heute=HEUTE)
        self.assertEqual(fehler, [])


class TestNamenVergleichen(unittest.TestCase):

    def test_ae_kommt_nach_allen_a(self):
        self.assertEqual(namen_vergleichen("Azzola", "Ärni"), -1)

    def test_umgekehrte_reihenfolge_ergibt_1(self):
        self.assertEqual(namen_vergleichen("Ärni", "Azzola"), 1)

    def test_umlaut_wird_auch_im_namen_beachtet(self):
        self.assertEqual(namen_vergleichen("Bauer", "Bär"), -1)

    def test_kleinbuchstabe_am_anfang_wird_normal_einsortiert(self):
        self.assertEqual(namen_vergleichen("von Gunten", "Zürcher"), -1)

    def test_ohne_akzent_kommt_vor_mit_akzent(self):
        self.assertEqual(namen_vergleichen("Helene", "Hélène"), -1)

    def test_ohne_trema_kommt_vor_mit_trema(self):
        self.assertEqual(namen_vergleichen("Noel", "Noël"), -1)

    def test_grossbuchstabe_kommt_vor_kleinbuchstabe(self):
        self.assertEqual(namen_vergleichen("Helene", "helene"), -1)

    def test_akzent_entscheidet_vor_gross_klein(self):
        self.assertEqual(namen_vergleichen("Hélène", "helene"), 1)

    def test_grossbuchstabe_auch_im_namen_zuerst(self):
        self.assertEqual(namen_vergleichen("BEn", "Ben"), -1)

    def test_gleiche_namen_ergeben_0(self):
        self.assertEqual(namen_vergleichen("Müller", "Müller"), 0)

    def test_akzent_wird_wie_grundbuchtstabe_sortiert(self):
        self.assertEqual(namen_vergleichen("Hélène", "Helga"), -1)

    def test_cedille_wird_wie_c_sortiert(self):
        self.assertEqual(namen_vergleichen("François", "Franz"), -1)

if __name__ == "__main__":
    unittest.main()
