import tkinter as tk
from tkinter import messagebox
import mariadb

fenster = tk.Tk()
fenster.title("Neue Anrede hinzufügen")
fenster.geometry("400x200")

verbindung = mariadb.connect(
    user="root",
    password="",
    host="localhost",
    port=3306,
    database="schlumpfshop3"
)
cursor = verbindung.cursor()

def anrede_hinzufuegen():
    # Text aus dem Eingabefeld lesen
    neue_anrede = eingabe.get()
    
    if neue_anrede == "":
        messagebox.showerror("Fehler", "Bitte eine Anrede eingeben!")
        return
    
    try:
        cursor.execute("SELECT * FROM anrede WHERE Anrede = ?", (neue_anrede,))
        if cursor.fetchone() is not None:
            messagebox.showerror("Fehler", "Diese Anrede gibt es schon!")
            return
        
        cursor.execute("INSERT INTO anrede (Anrede) VALUES (?)", (neue_anrede,))
        verbindung.commit()
        
        messagebox.showinfo("Erfolg", f"Anrede '{neue_anrede}' wurde hinzugefügt!")
        eingabe.delete(0, tk.END)
        
    except:
        messagebox.showerror("Fehler", "Es gab ein Problem mit der Datenbank!")
        verbindung.rollback()

tk.Label(fenster, text="Geben Sie eine neue Anrede ein:").pack(pady=10)

eingabe = tk.Entry(fenster, width=30)
eingabe.pack(pady=5)

tk.Button(fenster, text="Hinzufügen", command=anrede_hinzufuegen).pack(pady=10)
fenster.mainloop()
cursor.close()
verbindung.close()