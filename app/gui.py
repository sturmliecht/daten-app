import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from datetime import datetime, date
from app.logik import alter_berechnen

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

        # Vorname
        ttk.Label(formular, text="Vorname:").grid(row=0, column=0, sticky="w", pady=2)
        self.eingabe_vorname = ttk.Entry(formular, width=30)
        self.eingabe_vorname.grid(row=0, column=1, sticky="w", pady=2)

        # Nachname
        ttk.Label(formular, text="Nachname:").grid(row=1, column=0, sticky="w", pady=2)
        self.eingabe_nachname = ttk.Entry(formular, width=30)
        self.eingabe_nachname.grid(row=1, column=1, sticky="w", pady=2)

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
        spalten = ("vorname", "nachname", "geburtsdatum", "alter", "geschlecht", "wohnort")
        self.tabelle = ttk.Treeview(self.reiter_anzeige, columns=spalten, show="headings", height=10)

        # Spaltenüberschriften
        self.tabelle.heading("vorname", text="Vorname")
        self.tabelle.heading("nachname", text="Nachname")
        self.tabelle.heading("geburtsdatum", text="Geburtsdatum")
        self.tabelle.heading("alter", text="Alter")
        self.tabelle.heading("geschlecht", text="Geschlecht")
        self.tabelle.heading("wohnort", text="Wohnort")

        # Spaltenbreiten
        self.tabelle.column("vorname", width=120)
        self.tabelle.column("nachname", width=120)
        self.tabelle.column("geburtsdatum", width=100, anchor="center")
        self.tabelle.column("alter", width=50, anchor="center")
        self.tabelle.column("geschlecht", width=80, anchor="center")
        self.tabelle.column("wohnort", width=120)

        # Scrollleiste für viele Einträge
        scrollleiste = ttk.Scrollbar(self.reiter_anzeige, orient="vertical", command=self.tabelle.yview)
        self.tabelle.configure(yscrollcommand=scrollleiste.set)

        self.tabelle.grid(row=0, column=0, sticky="nsew")
        scrollleiste.grid(row=0, column=1, sticky="ns")

        # Tabelle wächst mit, wenn das Fenster grösser gezogen wird
        self.reiter_anzeige.rowconfigure(0, weight=1)
        self.reiter_anzeige.columnconfigure(0, weight=1)

        self.anzeige_aktualisieren()

    def anzeige_aktualisieren(self):
        # Alle bisherigen Zeilen entfernen
        for zeile in self.tabelle.get_children():
            self.tabelle.delete(zeile)

        # Einträge aus der Datenbank neu einfügen
        for eintrag_id, nachname, vorname, geburtsdatum, geschlecht, wohnort in datenbank.eintraege_auslesen():
            datum = date.fromisoformat(geburtsdatum)
            self.tabelle.insert("", tk.END, iid=eintrag_id, values=(
                vorname,
                nachname,
                datum.strftime("%d.%m.%Y"),
                alter_berechnen(datum),
                geschlecht,
                wohnort,
            ))


    def speichern(self):
        nachname = self.eingabe_nachname.get().strip()
        vorname = self.eingabe_vorname.get().strip()
        geburtsdatum_text = self.eingabe_geburtsdatum.get().strip()
        geschlecht = self.geschlecht.get()
        wohnort = self.eingabe_wohnort.get().strip()

        # Alle Fehler sammeln, damit man sie auf einmal sieht
        fehler = []

        if not nachname:
            fehler.append("Nachname fehlt.")
        if not vorname:
            fehler.append("Vorname fehlt.")
        if not wohnort:
            fehler.append("Wohnort fehlt.")
        if not geschlecht:
            fehler.append("Bitte ein Geschlecht auswählen.")

        geburtsdatum = None
        if not geburtsdatum_text:
            fehler.append("Geburtsdatum fehlt.")
        else:
            try:
                datum = datetime.strptime(geburtsdatum_text, "%d.%m.%Y").date()
                if datum > date.today():
                    fehler.append("Geburtsdatum darf nicht in der Zukunft liegen.")
                else:
                    geburtsdatum = datum.strftime("%Y-%m-%d")
            except ValueError:
                fehler.append("Geburtsdatum ist ungültig. Bitte im Format TT.MM.JJJJ eingeben.")

        # Bei Fehlern: Meldung anzeigen und abbrechen
        if fehler:
            messagebox.showerror("Eingabe prüfen", "\n".join(fehler))
            return

        datenbank.eintrag_speichern(nachname, vorname, geburtsdatum, geschlecht, wohnort)
        self.anzeige_aktualisieren()
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