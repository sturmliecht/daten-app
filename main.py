
from app import datenbank

datenbank.tabelle_anlegen()
datenbank.eintrag_speichern("Muster", "Anna", "2004-03-15", "w", "Bern")

for eintrag in datenbank.eintraege_auslesen():
    print(eintrag)