from datetime import date, datetime

SORTIERWERTE = {"ä": 97.5, 
                "ö": 111.5, 
                "ü": 117.5, 
                "â": 97, 
                "à": 97, 
                "ç": 99, 
                "é": 101, 
                "è": 101, 
                "ê": 101, 
                "ë": 101, 
                "ì": 105, 
                "ô": 111, 
                "ò": 111, 
                "ù": 117}

def alter_berechnen(geburtsdatum, heute=None):
    if heute is None:
        heute = date.today()
    alter = heute.year - geburtsdatum.year
    # Falls der Geburtstag dieses Jahr noch nicht war, ein Jahr abziehen
    if (heute.month, heute.day) < (geburtsdatum.month, geburtsdatum.day):
        alter -= 1
    return alter


def eingaben_pruefen(nachname, vorname, geburtsdatum_text, geschlecht, wohnort, heute=None):
    # Gibt zwei Werte zurück:
    # fehler: Liste mit Fehlermeldungen (leer, wenn alles stimmt)
    # geburtsdatum: Datum im Format JJJJ-MM-TT, oder None bei einem Fehler
    if heute is None:
        heute = date.today()

    fehler = []
    geburtsdatum = None

    if not vorname:
        fehler.append("Vorname fehlt.")
    if not nachname:
        fehler.append("Nachname fehlt.")

    if not geburtsdatum_text:
        fehler.append("Geburtsdatum fehlt.")
    else:
        try:
            datum = datetime.strptime(geburtsdatum_text, "%d.%m.%Y").date()
            if datum > heute:
                fehler.append("Geburtsdatum darf nicht in der Zukunft liegen.")
            else:
                geburtsdatum = datum.strftime("%Y-%m-%d")
        except ValueError:
            fehler.append("Geburtsdatum ist ungültig. Bitte im Format TT.MM.JJJJ eingeben.")

    if geschlecht not in ("m", "w", "d"):
        fehler.append("Bitte ein Geschlecht auswählen.")
    if not wohnort:
        fehler.append("Wohnort fehlt.")

    return fehler, geburtsdatum

def name_in_zahlen(name):
    # Wandelt einen Namen in eine Liste von Zahlen um, die für die Sortierung verwendet werden kann
    zahlen = list(SORTIERWERTE[zeichen] if zeichen in SORTIERWERTE else ord(zeichen) for zeichen in name.lower())
    return zahlen

def namen_vergleichen(name1, name2):
    # Vergleicht zwei Namen nach der Umlaute-Regel
    zahlen1 = name_in_zahlen(name1)
    zahlen2 = name_in_zahlen(name2)

    # Vergleiche die Zahlenlisten lexikographisch
    if zahlen1 < zahlen2:
        return -1
    elif zahlen1 > zahlen2:
        return 1
    else:
        name1_lower = name1.lower()
        name2_lower = name2.lower()
        if name1_lower < name2_lower:
            return -1
        elif name1_lower > name2_lower:
            return 1
        else:
            if name1 < name2:
                return -1
            elif name1 > name2:
                return 1
            else:
                return 0


