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
        self.current_question = 0
        self.questions = [
            #Grundfunktionen
            ("Was macht int()?",["Ganzzahl","Text","Kommas","True/false"],"Ganzzahl"),           #Wert wird in eine Ganzzahl umgewandelt
            ("Was macht str()?",["Zahl","Text","Komma","Liste"],"Text"),                         #Wandelt alles in text um 5 wird zu"5"
            ("Was ist bool?",["Text","True/False","Zahl","Liste"],"True/False"),                 #Datentyp für Wahr oder Falsch
            ("Was macht float()?",["Ganzzahl","Text","Kommazahl","Liste"],"Kommazahl"),          #wandelt in Kommazahl um (5 zu 5.0)
            ("Was macht import?",["Funktion","lädt Modul","Variable","erstellt schleife"],"lädt Modul"), #lädt externe Module/Bibliotheken
            ("Was ist print()?",["Ausgabe","Eingabe","Datei","Liste"],"Ausgabe"),                 #gibt Text aus
            ("Was ist input()?",["Berechnung","Eingabe","Ausgabe","Datai"],"Eingabe"),            #Benutzer schreibt etwas
            #funktionen
            ("Was macht def?",["Funktion", "Variable", "Schleife", "Import"],"Funktion"),         #erstellt eine eigene Funktion
            ("Was macht return?",["Ausgabe", "Rückgabe", "Abbruch", "Vergleich"],"Rückgabe"),     #gibt ein Ergebnis aus einer Funktion zurück
            ("Was ist Parameter?",["Variable", "Liste", "Funktion", "Wert"],"Wert"),              #wert, der einer Funktion übergeben wird
            #Listen & Text
            ("Was macht len()?",["Index", "Zählen", "Länge", "Sortieren"],"Länge"),              #zählt Zeichen oder Elemente
            ("Was macht split()?",["Trennen", "Verbinden", "Löschen","Sortieren"],"Trennen"),   #trennt Text in einzelne Teile (Liste)
            ("Was macht .strip()?",["Teilen", "Text kürzen", "Zählen","Leerzeichen entfernen"],"Leerzeichen entfernen"),  #entfernt Leerzeichen am Anfang/Ende (\n wäre Zeilenumbruch)
            ("Was macht .lower()?",["klein", "groß", "löschen", "trennen"],"klein"),           #macht alles klein
            ("Was macht .upper()?",["anhängen", "klein", "groß", "löschen"],"groß"),           #macht alles groß
            #Listen Funktionen
            ("Was macht append()?",["Hinzufügen", "Löschen", "Sortieren", "Teilen"],"Hinzufügen"),  #fügt ein Element ans Ende der Liste
            ("Was macht remove()?",["Sortieren", "Hinzufügen", "Löschen", "Kopieren"],"Löschen"),    #entfernt ein bestimmtes Element
            ("Was macht pop()?",["Letztes", "Erstes", "Alles", "Sortieren"],"Letztes"),              #entfernt das !letzte! Element
            ("Was macht sort()?",["Mischen", "Sortieren", "Löschen", "Kopieren"],"Sortieren"),       #sortiert eine Liste
            ("Was macht []?",["Liste", "Text", "Zahl", "Funktion"],"Liste"),                         #speichert mehrere Werte in einer Sammlung
            ("Was macht index?",["Position", "Wert", "Sortieren", "Zählen"],"Position"),             #gibt die Position eines Elements in einer Liste zurück
            ("Was macht in?",["Addieren", "Vergleich", "Sortieren", "Enthalten"],"Enthalten"),       #prüft ob etwas in einer Liste ist
            #Schleifen / range
            ("Was macht for?",["Funktion", "Bedingung", "Schleife", "Variable"],"Schleife"),         #wiederholt Code eine bestimmte Anzahl
            ("Was macht while?",["Vergleich", "Wiederholung", "Funktion", "Import"],"Wiederholung"), #wiederholt solange eine Bedingung stimmt
            ("Was macht break?",["Stop", "Weiter", "Start", "Vergleich"],"Stop"),                    #beendet eine Schleife sofort
            ("Was macht continue?",["Reset", "Stop", "Weiter", "Ende"],"Weiter"),                    #überspringt einen Schritt
            ("Was macht range(5)?",["Text", "Liste löschen", "Sortieren", "Zahlenreihe"],"Zahlenreihe"), #erzeugt eine Zahlenreihe (Start bei 0)
            ("Was gibt range(5) zurück?",["0-5", "1-5", "0-4", "1-4"], "0-4"),                       #Liste von Zahlen 0 bis 4
            ("Wofür nutzt man range()?",["Speichern", "Vergleich", "Sortieren", "Wiederholung"],"Wiederholung"), #für Wiederholungen in for-Schleifen
            #Dateien
            ("Was macht open()?",["Datei öffnen", "Liste erstellen", "Text löschen", "Sortieren"],"Datei"),             ## öffnet oder erstellt eine Datei
            ("Was macht open('r')?",["Löschen", "Schreiben", "Lesen", "Erstellen"],"Lesen"),        #öffnet Datei zum Lesen
            ("Was macht open('w')?",["Lesen", "Schreiben", "Anhängen", "Vergleichen"],"Schreiben"),                                                  #öffnet Datei zum Schreiben
            #Bedingungen
            ("Was macht if?",["Bedingung", "Schleife", "Funktion", "Variable"],"Bedingung"),    #prüft ob die bedingung wahr ist
            ("Was macht else?",["Start", "Wenn", "Stop", "Sonst"],"Sonst"),                     #alternative bedingungen wenn if falsch ist
            ("Was macht elif?",["Sonst-wenn", "Immer", "Stop", "Start"],"Sonst-wenn"),          #weitere Bedingung wenn if falsch ist
            ("Was macht ==?",["Kleiner", "Ungleich", "Vergleich", "Größer"],"Vergleich"),          #prüft ob zwei Werte gleich sind
            ("Was macht !=?",["Zuweisung", "Gleich", "Vergleich", "Ungleich"],"Ungleich"),      #prüft ob Werte ungleich sind
            ("Was macht isalpha()?",["Leerzeichen", "Zahlen", "Buchstaben", "Symbole"],"Buchstaben"),   #prüft ob nur Buchstaben vorhanden sind
            ("Was macht isdigit()?",["Zahlen", "Buchstaben", "Text", "Liste"],"Zahlen"),        #prüft ob nur Zahlen vorhanden sind
            ("Was macht < ?",["gleich", "größer", "kleiner", "ungleich"],"kleiner"),            #kleiner als
            ("Was macht > ?",["größer", "kleiner", "gleich", "ungleich"],"größer"),             #größer als
            #Rechnen/Operatoren
            ("Was macht +?",["Minus", "Mal", "Plus", "Rest"],"Plus"),                   #addiert zwei Werte
            ("Was macht -?",["Plus", "Minus", "Mal", "Geteilt"],"Minus"),               #subtrahiert Werte
            ("Was macht *?",["Geteilt", "Mal", "Plus", "Rest"],"Mal"),                  #multipliziert Werte
            ("Was macht /?",["Rest", "Mal", "Plus", "Geteilt"],"Geteilt"),              #teilt Werte
            ("Was macht %?",["Rest", "Division", "Multiplikation", "Addition"], "Rest"), #gibt den Rest einer Division
            #GUI (tkinter)
            ("Was ist tkinter?",["Spiel", "Datenbank", "GUI", "Text"],"GUI"),            #bibliothek für benutzeroberflächen (Grafische Darstellung)
            ("Was macht pack()?",["Sortieren", "Raster", "Position", "Stapel"],"Stapel"),    #ordnet Elemente untereinander an
            ("Was macht grid()?",["Stapel", "Raster", "Liste", "Position"],"Raster"),        #ordnet Elemente in Tabellenform
            ("Was macht place()?",["Position", "Raster", "Stapel", "Liste"],"Position"),     #setzt Elemente an feste Position
            #Entry / GUI Text
            ("Was macht entry.get()?",["Schreiben", "Lesen", "Löschen", "Sortieren"],"Lesen"),     #holt Text aus Eingabefeld
            ("Was macht insert()?",["Teilen","Löschen","Vergleichen","Schrieben"],"Schreiben"),    #fügt Text ein
            ("Was macht delete()?",["Ende","Trennen","Löschen","Lesen"],"Löschen"),                #löscht Text
            ("Was ist entry?",["Feld","Sortieren","Lesen","Stapeln"],"Feld"),                 #Eingabefeld in GUI
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
        self.frame_buttons.pack_forget()
        self.game()

    def game(self):
        self.current_question = 0
        self.score_v = 0

        self.frame_game = tkinter.Frame(self.root)
        self.frame_game.pack()

        self.question_label = tkinter.Label(self.frame_game, text="")
        self.question_label.pack()
        self.buttons = []

        self.load_question()

    def load_question(self):

        if hasattr(self, "buttons"):        #prüfen ob schon Buttons existieren
            # alle alten Buttons löschen
            for button in self.buttons:
                button.destroy()

        question = self.questions[self.current_question]   #aktuelle Frage holen
        self.question_label.config(text=question[0])        #frage im Label anzeigen

        for answer in question[1]:            #alle Antwortmöglichkeiten durchgehen (Am Ende der Schleife ist antwort immer der letzte Wert)
            # Button erstellen
            button = tkinter.Button(self.frame_game, text=answer)
            button.config(command=lambda a=answer, b=button: self.check_answer(a, b)) #a=platzhalter
            button.pack(pady=5)                                                      #a=ist nur eine Kopie vom aktuellen Wert damit jeder Button seine eigene Antwort behält
            self.buttons.append(button)

            button.pack(pady=5)              #nutton im Fenster anzeigen

            self.buttons.append(button)          #button speichern (damit wir ihn später ändern können)

    def check_answer(self, selected_answer, button):

        correct_answer = self.questions[self.current_question][2]

        if selected_answer == correct_answer:
            button.config(bg="green")
            self.score_v += 1
        else:
            button.config(bg="red")

        self.root.after(100,self.next_question)

    def next_question(self):
        self.current_question += 1

        if self.current_question < len(self.questions):                 #<len() = bin ich noch im Bereich
            self.load_question()
        else:
            mb.showinfo("Fertig",f"Dein Score: {self.score_v}")

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