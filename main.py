#Python-Programmier Vokabel-Quiz-Spiel

import tkinter
import sqlite3

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
        self.select_player=tkinter.StringVar()
        self.score= 0

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

    def button_typ_click(self):
        typ_wert = self.entry_typ.get()
        print("Typ:", typ_wert)

    def create_player(self):
        print("Spieler erstellen geklickt")

    def select_player(self):
        print("Spieler wählen geklickt")

    def play(self):
        print("Spielen geklickt")

    def show_score(self):
        print("Score anzeigen geklickt")

    def exit_game(self):
        self.root.destroy()


root=tkinter.Tk()
game = quiz_game(root)
root.mainloop()