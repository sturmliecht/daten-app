# Personenverwaltung

Kleine Desktop-App in Python zum Erfassen und Anzeigen von Personendaten.

Entstanden als Wochenprojekt im Rahmen von Modul 03 in der KW 42.

## Funktionen

- Das Erfassen von Personen mit Vorname, Nachname, Geburtsdatum, Geschlecht (m/w/d) und Wohnort
- Die Prüfung der Eingaben mit verständlichen Fehlermeldungen
- Das Speichern der Daten in einer SQLite-Datenbank
- Das Anzeigen aller Einträge in einer Tabelle, inklusive automatischer Berechnung des Alters mit dem Geburtsdatum als Grundlage
- Getrennte Bereiche für Eingabe und Anzeige über zwei Reiter im selben Fenster

## Installation und Start

**Voraussetzung:** Python 3.11 (entwickelt mit 3.11.3)

Die App verwendet nur die Standardbibliothek von Python (tkinter, sqlite3, unittest).
Es müssen keine zusätzlichen Pakete installiert werden.

```
git clone https://github.com/sturmliecht/daten-app.git
cd daten-app
python main.py
```

Unter Windows funktioniert je nach Installation `py main.py` statt `python main.py`.

Beim ersten Start wird die Datenbankdatei `daten.db` automatisch im Projektordner angelegt.

## Bedienung

**Reiter „Eingabe“**

Alle Felder ausfüllen, das Geburtsdatum im Format `TT.MM.JJJJ`, und auf „Speichern“ klicken. Bei fehlenden oder ungültigen Angaben erscheint eine Meldung mit allen Fehlern.

**Reiter „Anzeige“**

Zeigt alle gespeicherten Personen, sortiert nach Nachname.

## Aufbau des Projekts

```
daten-app/
├── main.py              Startpunkt der App
├── app/
│   ├── datenbank.py     Zugriff auf die SQLite-Datenbank
│   ├── logik.py         Altersberechnung und Eingabeprüfung
│   └── gui.py           Oberfläche mit tkinter
└── tests/
    ├── test_datenbank.py
    └── test_logik.py
```

Der Code ist in drei Schichten aufgeteilt: Oberfläche (`gui.py`), Logik (`logik.py`)
und Datenbank (`datenbank.py`). Dadurch lassen sich Logik und Datenbank testen,
ohne dass dafür ein Fenster geöffnet werden muss.

### Datenbanktabelle `personen`

| Feld         | Datentyp | Hinweis                                    |
|--------------|----------|--------------------------------------------|
| id           | INTEGER  | Laufende Nummer, wird automatisch vergeben |
| nachname     | TEXT     | Pflichtfeld                                |
| vorname      | TEXT     | Pflichtfeld                                |
| geburtsdatum | TEXT     | Gespeichert als JJJJ-MM-TT                 |
| geschlecht   | TEXT     | Nur m, w oder d erlaubt                    |
| wohnort      | TEXT     | Pflichtfeld                                |

Das Alter wird nicht gespeichert, sondern bei der Anzeige aus dem Geburtsdatum berechnet,
da es sich jedes Jahr ändert.

## Tests ausführen

Im Projektordner:

```
python -m unittest -v
```

Es laufen 14 Tests für die Datenbankfunktionen, die Altersberechnung und die Eingabeprüfung.
Die Tests verwenden eine eigene, temporäre Datenbank. Die echte `daten.db` bleibt dabei unverändert.

## Autor

Alwin Huber