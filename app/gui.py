import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from app import datenbank

class DatenApp:
    def __init__(self, fenster):
        self.fenster = fenster
        self.fenster.title("Personenverwaltung")

        # Reiter-Leiste mit zwei Reitern
        self.reiter = ttk.Notebook(fenster)
        self.reiter.pack(fill="both", expand=True)

        self.reiter_eingabe = ttk.Frame(self.reiter, padding=10)
        self.reiter_anzeige = ttk.Frame(self.reiter, padding=10)
        self.reiter.add(self.reiter_eingabe, text="Eingabe")
        self.reiter.add(self.reiter_anzeige, text="Anzeige")

        self.eingabe_bauen()
        self.anzeige_bauen()

    def eingabe_bauen(self):
        formular = self.reiter_eingabe

        # Nachname
        ttk.Label(formular, text="Nachname:").grid(row=0, column=0, sticky="w", pady=2)
        self.eingabe_nachname = ttk.Entry(formular, width=30)
        self.eingabe_nachname.grid(row=0, column=1, sticky="w", pady=2)

        # Vorname
        ttk.Label(formular, text="Vorname:").grid(row=1, column=0, sticky="w", pady=2)
        self.eingabe_vorname = ttk.Entry(formular, width=30)
        self.eingabe_vorname.grid(row=1, column=1, sticky="w", pady=2)

        # Geburtsdatum
        ttk.Label(formular, text="Geburtsdatum (TT.MM.JJJJ):").grid(row=2, column=0, sticky="w", pady=2)
        self.eingabe_geburtsdatum = ttk.Entry(formular, width=12)
        self.eingabe_geburtsdatum.grid(row=2, column=1, sticky="w", pady=2)

        # Geschlecht als Auswahlknöpfe
        ttk.Label(formular, text="Geschlecht:").grid(row=3, column=0, sticky="w", pady=2)
        self.geschlecht = tk.StringVar()
        auswahl = ttk.Frame(formular)
        auswahl.grid(row=3, column=1, sticky="w", pady=2)
        for wert in ("m", "w", "d"):
            ttk.Radiobutton(auswahl, text=wert, value=wert, variable=self.geschlecht).pack(side="left", padx=(0, 10))

        # Wohnort
        ttk.Label(formular, text="Wohnort:").grid(row=4, column=0, sticky="w", pady=2)
        self.eingabe_wohnort = ttk.Entry(formular, width=30)
        self.eingabe_wohnort.grid(row=4, column=1, sticky="w", pady=2)

        # Speichern-Button (Funktion folgt in der nächsten Unteraufgabe)
        self.knopf_speichern = ttk.Button(formular, text="Speichern", command=self.speichern)
        self.knopf_speichern.grid(row=5, column=1, sticky="w", pady=(10, 0))

    def anzeige_bauen(self):
        # Platzhalter, wird in Aufgabe 5 durch die Tabelle ersetzt
        ttk.Label(self.reiter_anzeige, text="Hier erscheinen später die Einträge.").pack()


    def speichern(self):
        nachname = self.eingabe_nachname.get().strip()
        vorname = self.eingabe_vorname.get().strip()
        geburtsdatum_text = self.eingabe_geburtsdatum.get().strip()
        geschlecht = self.geschlecht.get()
        wohnort = self.eingabe_wohnort.get().strip()

        # Datum von TT.MM.JJJJ in JJJJ-MM-TT umwandeln
        geburtsdatum = datetime.strptime(geburtsdatum_text, "%d.%m.%Y").strftime("%Y-%m-%d")

        datenbank.eintrag_speichern(nachname, vorname, geburtsdatum, geschlecht, wohnort)
        messagebox.showinfo("Gespeichert", f"{vorname} {nachname} wurde gespeichert.")
        self.felder_leeren()



    def felder_leeren(self):
        self.eingabe_nachname.delete(0, tk.END)
        self.eingabe_vorname.delete(0, tk.END)
        self.eingabe_geburtsdatum.delete(0, tk.END)
        self.eingabe_wohnort.delete(0, tk.END)
        self.geschlecht.set("")

def starten():
    fenster = tk.Tk()
    DatenApp(fenster)
    fenster.mainloop()