import unittest
from datetime import date

from app.logik import alter_berechnen


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


if __name__ == "__main__":
    unittest.main()