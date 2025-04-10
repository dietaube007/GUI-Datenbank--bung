import tkinter as tk
from tkinter import messagebox
import mariadb

class AnredeHinzufuegenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Neue Anrede hinzufügen")
        
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
        # Hauptframe
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True)
        
        # Eingabefeld für Anrede
        tk.Label(main_frame, text="Neue Anrede:").grid(row=0, column=0, sticky="w", pady=5)
        self.anrede_entry = tk.Entry(main_frame, width=30)
        self.anrede_entry.grid(row=0, column=1, pady=5, padx=10)
        
        # Button zum Hinzufügen
        hinzufuegen_button = tk.Button(main_frame, text="Anrede hinzufügen", 
                                     command=self.anrede_hinzufuegen)
        hinzufuegen_button.grid(row=1, column=0, columnspan=2, pady=15)
        
        # Statusleiste
        self.status = tk.Label(self.root, text="Bitte neue Anrede eingeben", 
                             bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(fill=tk.X)
    
    def anrede_hinzufuegen(self):
        neue_anrede = self.anrede_entry.get().strip()
        
        if not neue_anrede:
            messagebox.showerror("Fehler", "Bitte eine Anrede eingeben")
            return
        
        try:
            # Überprüfen ob Anrede bereits existiert
            self.cur.execute("SELECT COUNT(*) FROM anrede WHERE Anrede = ?", (neue_anrede,))
            if self.cur.fetchone()[0] > 0:
                messagebox.showerror("Fehler", "Diese Anrede existiert bereits")
                return
            
            # Anrede in Datenbank einfügen
            self.cur.execute("INSERT INTO anrede (Anrede) VALUES (?)", (neue_anrede,))
            self.conn.commit()
            
            messagebox.showinfo("Erfolg", f"Anrede '{neue_anrede}' wurde erfolgreich hinzugefügt")
            self.anrede_entry.delete(0, tk.END)
            self.status.config(text=f"Anrede '{neue_anrede}' wurde hinzugefügt")
            
        except mariadb.Error as e:
            messagebox.showerror("Datenbankfehler", f"Fehler beim Hinzufügen der Anrede: {e}")
            self.conn.rollback()
    
    def __del__(self):
        self.cur.close()
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = AnredeHinzufuegenApp(root)
    root.mainloop()