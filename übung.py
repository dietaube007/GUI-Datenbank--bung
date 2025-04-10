import tkinter as tk
from tkinter import ttk, messagebox
import mariadb

class BestellungApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bestellung - Lagerbestandsprüfung")
        
        # Datenbankverbindung
        self.conn = mariadb.connect(
            user="root",
            password="",
            host="localhost",
            port=3306,
            database="schlumpfshop3"
        )
        self.cur = self.conn.cursor()
        
        self.setup_ui()
    
    def setup_ui(self):
        # Eingabefeld für Mindeststückzahl
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10, fill=tk.X)
        
        tk.Label(input_frame, text="Mindeststückzahl:").pack(side=tk.LEFT, padx=5)
        self.mindestbestand_entry = tk.Entry(input_frame, width=10)
        self.mindestbestand_entry.pack(side=tk.LEFT, padx=5)
        
        suchen_button = tk.Button(input_frame, text="Suchen", command=self.zeige_bestellliste)
        suchen_button.pack(side=tk.LEFT, padx=5)
        
        # Tabelle für Ergebnisse
        self.tabelle = ttk.Treeview(self.root, columns=("Artikelname", "Lagerbestand", "Lieferant"), show="headings")
        self.tabelle.heading("Artikelname", text="Artikelname")
        self.tabelle.heading("Lagerbestand", text="Lagerbestand")
        self.tabelle.heading("Lieferant", text="Lieferant")
        self.tabelle.column("Artikelname", width=200)
        self.tabelle.column("Lagerbestand", width=100)
        self.tabelle.column("Lieferant", width=150)
        self.tabelle.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Statusleiste
        self.status = tk.Label(self.root, text="Bitte Mindeststückzahl eingeben und auf 'Suchen' klicken", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(fill=tk.X)
    
    def zeige_bestellliste(self):
        try:
            mindestbestand = int(self.mindestbestand_entry.get())
        except ValueError:
            messagebox.showerror("Fehler", "Bitte eine gültige Zahl eingeben")
            return
            
        self.cur.execute("""
            SELECT artikel.Artikelname, artikel.Lagerbestand, lieferant.Lieferantenname
            FROM artikel
            JOIN lieferant ON artikel.Lieferant = lieferant.ID_Lieferant
            WHERE artikel.Lagerbestand < ?
            ORDER BY artikel.Lagerbestand ASC
        """, (mindestbestand,))
        
        # Tabelle leeren
        for row in self.tabelle.get_children():
            self.tabelle.delete(row)
        
        # Ergebnisse einfügen
        artikel_gefunden = False
        for artikel in self.cur.fetchall():
            self.tabelle.insert("", tk.END, values=artikel)
            artikel_gefunden = True
        
        if artikel_gefunden:
            self.status.config(text=f"Artikel mit Lagerbestand unter {mindestbestand} Stück")
        else:
            self.status.config(text=f"Keine Artikel mit Lagerbestand unter {mindestbestand} Stück gefunden")
    
    def __del__(self):
        self.cur.close()
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = BestellungApp(root)
    root.mainloop()