#Python-Programmier Vokabel-Quiz-Spiel

import tkinter
import sqlite3
import tkinter.messagebox as mb

class quiz_game:
    def __init__(self,root):
        #verbindung datenbank
        self.conn = sqlite3.connect("quiz.db",)
        self.c = self.conn.cursor()

        # Tabelle erstellen, falls noch nicht vorhanden
        self.c.execute(
        """
        CREATE TABLE IF NOT EXISTS quiz (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player TEXT NOT NULL,
            score INTEGER NOT NULL
        )
        """)

        self.conn.commit()
        self.root = root
        self.root.title("Vokabel Quiz")
        self.root.geometry("600x550")

        #variablen listen zwischenspiechern
        self.selected_player = None
        self.score_v= 0                         #v=variable da score nicht 2x exestieren kan

        #frame container für knöpfe erstellen
        self.frame_buttons = tkinter.Frame(root)
        self.frame_buttons.pack(expand=True)

        #menü knöpfe erstellen
        self.button_create_player = tkinter.Button(self.frame_buttons, text="Spieler erstellen",command=self.create_player)
        self.button_create_player.pack(pady=10)

        self.button_select_player = tkinter.Button(self.frame_buttons, text="Spieler wählen",command=self.select_player)
        self.button_select_player.pack(pady=10)

        self.button_play = tkinter.Button(self.frame_buttons, text="Spielen", command=self.play)
        self.button_play.pack(pady=10)

        self.button_score = tkinter.Button(self.frame_buttons, text="Score anzeigen", command=self.show_score)
        self.button_score.pack(pady=10)

        self.button_exit = tkinter.Button(self.frame_buttons, text="Beenden", command=self.exit_game)
        self.button_exit.pack(pady=10)

        #fragen
        self.question = [
            #Grundfunktionen
            ("Was macht int()?", "Ganzzahl"),           #Wert wird in eine Ganzzahl umgewandelt
            ("Was macht str()?", "Text"),               #Wandelt alles in text um 5 wird zu"5"
            ("Was ist bool?", "True/False"),            #Datentyp für Wahr oder Falsch
            ("Was macht float()?", "Kommazahl"),        #wandelt in Kommazahl um (5 zu 5.0)
            ("Was macht import?", "lädt Modul"),             #lädt externe Module/Bibliotheken
            ("Was ist print()?", "Ausgabe"),            #gibt Text aus
            ("Was ist input()?", "Eingabe"),            #Benutzer schreibt etwas
            #funktionen
            ("Was macht def?", "Funktion"),             #erstellt eine eigene Funktion
            ("Was macht return?", "Rückgabe"),          #gibt ein Ergebnis aus einer Funktion zurück
            ("Was ist Parameter?", "Wert"),             #wert, der einer Funktion übergeben wird
            #Listen & Text
            ("Was macht len()?", "Länge"),              #zählt Zeichen oder Elemente
            ("Was macht split()?", "Trennen"),          #trennt Text in einzelne Teile (Liste)
            ("Was macht .strip()?", "entfernt Leerzeichen"),  #entfernt Leerzeichen am Anfang/Ende (\n wäre Zeilenumbruch)
            ("Was macht .lower()?", "klein"),           #macht alles klein
            ("Was macht .upper()?", "gross"),           #macht alles groß
            #Listen Funktionen
            ("Was macht append()?", "Hinzufügen"),      #fügt ein Element ans Ende der Liste
            ("Was macht remove()?", "Löschen"),         #entfernt ein bestimmtes Element
            ("Was macht pop()?", "Letztes"),            #entfernt das !letzte! Element
            ("Was macht sort()?", "Sortieren"),         #sortiert eine Liste
            ("Was macht []?", "Liste"),                 #speichert mehrere Werte in einer Sammlung
            ("Was macht index?", "Position"),           #gibt die Position eines Elements in einer Liste zurück
            ("Was macht in?", "Enthalten"),             #prüft ob etwas in einer Liste ist
            #Schleifen / range
            ("Was macht for?", "Schleife"),             #wiederholt Code eine bestimmte Anzahl
            ("Was macht while?", "Wiederholung"),       #wiederholt solange eine Bedingung stimmt
            ("Was macht break?", "Stop"),               #beendet eine Schleife sofort
            ("Was macht continue?", "Weiter"),          #überspringt einen Schritt
            ("Was macht range(5)?", "Zählen"),          #erzeugt eine Zahlenreihe (Start bei 0)
            ("Was gibt range(5) zurück?", "0-4"),       #Liste von Zahlen 0 bis 4
            ("Wofür nutzt man range()?", "Wiederholung"), #für Wiederholungen in for-Schleifen
            #Dateien
            ("Was macht open()?", "Datei"),             ## öffnet oder erstellt eine Datei
            ("Was macht open('r')?", "Lesen"),          #öffnet Datei zum Lesen
            ("Was macht open('w')?", "Schreiben"),      #öffnet Datei zum Schreiben
            #Bedingungen
            ("Was macht if?", "Bedingung"),             #prüft ob die bedingung wahr ist
            ("Was macht else?", "Sonst"),               #alternative bedingungen wenn if falsch ist
            ("Was macht elif?", "Sonst-wenn"),          #weitere Bedingung wenn if falsch ist
            ("Was macht ==?", "Gleich"),                #prüft ob zwei Werte gleich sind
            ("Was macht !=?", "Ungleich"),              #prüft ob Werte ungleich sind
            ("Was macht isalpha()?", "Buchstaben"),     #prüft ob nur Buchstaben vorhanden sind
            ("Was macht isdigit()?", "Zahlen"),         #prüft ob nur Zahlen vorhanden sind
            ("Was prüft ==?","Vergleich"),              #vergleicht zwei Werte
            ("Was macht < ?", "kleiner"),               #kleiner als
            ("Was macht > ?", "größer"),                #größer als
            #Rechnen/Operatoren
            ("Was macht +?", "Plus"),                   #addiert zwei Werte
            ("Was macht -?", "Minus"),                  #subtrahiert Werte
            ("Was macht *?", "Mal"),                    #multipliziert Werte
            ("Was macht /?", "Geteilt"),                #teilt Werte
            ("Was macht %?", "Rest"),                   #gibt den Rest einer Division
            #GUI (tkinter)
            ("Was ist tkinter?", "GUI"),                #bibliothek für benutzeroberflächen (Grafische Darstellung)
            ("Was macht pack()?", "Stapel"),            #ordnet Elemente untereinander an
            ("Was macht grid()?", "Raster"),            #ordnet Elemente in Tabellenform
            ("Was macht place()?", "Position"),         #setzt Elemente an feste Position
            #Entry / GUI Text
            ("Was macht entry.get()?", "Lesen"),        #holt Text aus Eingabefeld
            ("Was macht insert()?", "Schreiben"),       #fügt Text ein
            ("Was macht delete()?", "Löschen"),         #löscht Text
            ("Was ist entry?", "Feld"),                 #Eingabefeld in GUI
        ]
    def create_player(self):
        self.frame_buttons.pack_forget()
        self.show_create_player_screen()

    def show_create_player_screen(self):
        self.frame_create_player = tkinter.Frame(self.root)
        self.frame_create_player.pack()

        label = tkinter.Label(self.frame_create_player, text="Spielername:")
        label.pack(pady=10)

        self.entry_name = tkinter.Entry(self.frame_create_player)
        self.entry_name.pack(pady=10)

        button_save = tkinter.Button(self.frame_create_player,text="Speichern",command=self.save_player)
        button_save.pack(pady=10)
        button_back = tkinter.Button(self.frame_create_player,text="Zurück",command=self.back_to_menu_0)
        button_back.pack(pady=10)

    def save_player(self):
        name = self.entry_name.get()

        if name == "":
            mb.showwarning("Fehler","Bitte Namen eingeben")
            return

        score = 0

        self.c.execute("INSERT INTO quiz (player, score) VALUES (?, ?)", (name, score))
        self.conn.commit()

        self.frame_create_player.destroy()
        self.frame_buttons.pack(expand=True)

    def back_to_menu_0(self):
        self.frame_create_player.destroy()
        self.frame_buttons.pack(expand=True)

    def select_player(self):
        self.frame_buttons.pack_forget()
        self.show_select_player_screen()

    def show_select_player_screen(self):
        self.frame_select_player = tkinter.Frame(self.root)
        self.frame_select_player.pack()

        label = tkinter.Label(self.frame_select_player, text="Spielername auswählen:")
        label.pack(pady=10)

        self.listbox = tkinter.Listbox(self.frame_select_player)
        self.listbox.pack(pady=10)

        #aus datenbank spieler holen
        self.c.execute("SELECT player FROM quiz")
        players = self.c.fetchall()

        #in liste eintragen
        for p in players:
            self.listbox.insert(tkinter.END, p[0])

        button_choose = tkinter.Button(self.frame_select_player, text="Spieler auswählen", command=self.set_player)
        button_choose.pack(pady=10)
        button_delete = tkinter.Button(self.frame_select_player,text="Spieler löschen",command=self.delete_player)
        button_delete.pack(pady=10)
        button_back = tkinter.Button(self.frame_select_player, text="Zurück", command=self.set_player)
        button_back.pack(pady=10)

    def set_player(self):
        selected = self.listbox.get(tkinter.ACTIVE)

        if selected == "":
            mb.showwarning("Fehler","Bitte Namen auswählen")
            return

        self.selected_player = selected

        self.frame_select_player.destroy()
        self.frame_buttons.pack(expand=True)

    def play(self):


    def show_score(self):
        self.frame_buttons.pack_forget()
        self.score()

    def score(self):
        self.frame_score = tkinter.Frame(self.root)
        self.frame_score.pack()

        label = tkinter.Label(self.frame_score, text="Score:")
        label.pack(pady=10)

        self.listbox = tkinter.Listbox(self.frame_score)
        self.listbox.pack(pady=10)

        # aus datenbank spieler holen
        self.c.execute("SELECT player, score FROM quiz")
        scores = self.c.fetchall()

        # in liste eintragen
        for s in scores:
            self.listbox.insert(tkinter.END,f"{s[0]}, {s[1]} Punkte")

        button_back = tkinter.Button(self.frame_score, text="Zurück", command=self.back_to_menu)
        button_back.pack(pady=10)
        button_delete = tkinter.Button(self.frame_score,text="Score löschen",command=self.delete_score)
        button_delete.pack(pady=10)

    def back_to_menu(self):
        self.frame_score.destroy()
        self.frame_buttons.pack(expand=True)

    def exit_game(self):
        self.root.destroy()

    #löschen funktion für spieler auswahl
    def delete_player(self):
        selected = self.listbox.get(tkinter.ACTIVE)

        if not selected:
            mb.showwarning("Fehler", "Bitte Spieler auswählen")
            return

        name = selected.split(",")[0]

        self.c.execute("DELETE FROM quiz WHERE player = ?", (name,))
        self.conn.commit()

        mb.showinfo("OK", "Spieler gelöscht")

        self.frame_select_player.destroy()
        self.show_select_player_screen()

    #löschfunktion für score
    def delete_score(self):
        selected = self.listbox.get(tkinter.ACTIVE)

        if not selected:
            mb.showwarning("Fehler", "Bitte Eintrag auswählen")
            return

        name = selected.split(",")[0]

        self.c.execute("DELETE FROM quiz WHERE player = ?", (name,))
        self.conn.commit()

        mb.showinfo("OK", "Score gelöscht")

        self.frame_score.destroy()
        self.score()

root=tkinter.Tk()
game = quiz_game(root)
root.mainloop()