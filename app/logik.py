from datetime import date, datetime


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

def namen_vergleichen(name1, name2):
    return 0
