from datetime import date


def alter_berechnen(geburtsdatum, heute=None):
    if heute is None:
        heute = date.today()
    alter = heute.year - geburtsdatum.year
    # Falls der Geburtstag dieses Jahr noch nicht war, ein Jahr abziehen
    if (heute.month, heute.day) < (geburtsdatum.month, geburtsdatum.day):
        alter -= 1
    return alter