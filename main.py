#Python-Programmier Vokabel-Quiz-Spiel

import tkinter
import sqlite3
import tkinter.messagebox as mb
import random

class quiz_game:
    def __init__(self,root):
        #verbindung datenbank
        self.conn = sqlite3.connect("quiz.db",)
        self.c = self.conn.cursor()
        self.user_answers = []                                  #liste erstellen für gespeicherte antworten

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
        self.root.geometry("400x350")

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
            ("Was macht int()?",["Ganzzahl","Text","Kommas","True/false"],"Ganzzahl","Wert wird in eine Ganzzahl umgewandelt(5 zu 5.0"),
            ("Was macht str()?",["Zahl","Text","Komma","Liste"],"Text","Wandelt alles in text um 5 wird zu '5'(gänsefüße''text'' "),
            ("Was ist bool?",["Text","True/False","Zahl","Liste"],"True/False","Datentyp für Wahr oder Falsch(True/False)"),
            ("Was macht float()?",["Ganzzahl","Text","Kommazahl","Liste"],"Kommazahl","wandelt in Kommazahl um (5 zu 5.0)"),
            ("Was macht import?",["Funktion","lädt Modul","Variable","erstellt schleife"],"lädt Modul","lädt externe Module/Bibliotheken aus Phyton"),
            ("Was ist print()?",["Ausgabe","Eingabe","Datei","Liste"],"Ausgabe","gibt Text aus"),
            ("Was ist input()?",["Berechnung","Eingabe","Ausgabe","Datai"],"Eingabe","Benutzer schreibt etwas"),
            #funktionen
            ("Was ist def?",["Funktion", "Variable", "Schleife", "Import"],"Funktion","erstellt eine eigene Funktion"),
            ("Was macht return?",["Ausgabe", "Rückgabe", "Abbruch", "Vergleich"],"Rückgabe","gibt ein Ergebnis aus einer Funktion zurück"),
            ("Was ist Parameter?",["Variable", "Liste", "Funktion", "Wert"],"Wert","wert, der einer Funktion übergeben wird"),
            #Listen & Text
            ("Was macht len()?",["Index", "Zählen", "Länge", "Sortieren"],"Länge","zählt Zeichen oder Elemente"),
            ("Was macht split()?",["Trennen", "Verbinden", "Löschen","Sortieren"],"Trennen","trennt Text in einzelne Teile (Liste)"),
            ("Was macht .strip()?",["Teilen", "Text kürzen", "Zählen","Leerzeichen entfernen"],"Leerzeichen entfernen","entfernt Leerzeichen am Anfang/Ende (\\n wäre Zeilenumbruch)"),
            ("Was macht .lower()?",["klein", "groß", "löschen", "trennen"],"klein","macht alles klein"),
            ("Was macht .upper()?",["anhängen", "klein", "groß", "löschen"],"groß","macht alles groß"),
            #Listen Funktionen
            ("Was macht append()?",["Hinzufügen", "Löschen", "Sortieren", "Teilen"],"Hinzufügen","fügt ein Element ans Ende der Liste"),
            ("Was macht remove()?",["Sortieren", "Hinzufügen", "Löschen", "Kopieren"],"Löschen","entfernt ein bestimmtes Element"),
            ("Was macht pop()?",["Letztes", "Erstes", "Alles", "Sortieren"],"Letztes","entfernt das !letzte! Element"),
            ("Was macht sort()?",["Mischen", "Sortieren", "Löschen", "Kopieren"],"Sortieren","sortiert eine Liste"),
            ("Was ist []?",["Liste", "Text", "Zahl", "Funktion"],"Liste","speichert mehrere Werte in einer Sammlung"),
            ("Was macht index?",["Position", "Wert", "Sortieren", "Zählen"],"Position","gibt die Position eines Elements in einer Liste zurück"),
            ("Was macht in?",["Addieren", "Vergleich", "Sortieren", "Enthalten"],"Enthalten","prüft ob etwas in einer Liste ist"),
            #Schleifen / range
            ("Was macht for?",["Funktion", "Bedingung", "Schleife", "Variable"],"Schleife","wiederholt Code eine bestimmte Anzahl"),
            ("Was macht while?",["Vergleich", "Wiederholung", "Funktion", "Import"],"Wiederholung","wiederholt solange eine Bedingung stimmt"),
            ("Was macht break?",["Stop", "Weiter", "Start", "Vergleich"],"Stop","beendet eine Schleife sofort"),
            ("Was macht continue?",["Reset", "Stop", "Weiter", "Ende"],"Weiter","überspringt einen Schritt"),
            ("Was macht range(5)?",["Text", "Liste löschen", "Sortieren", "Zahlenreihe"],"Zahlenreihe","erzeugt eine Zahlenreihe (Start bei 0)"),
            ("Was gibt range(5) zurück?",["0-5", "1-5", "0-4", "1-4"], "0-4","Liste von Zahlen 0 bis 4"),
            ("Wofür nutzt man range()?",["Speichern", "Vergleich", "Sortieren", "Wiederholung"],"Wiederholung","für Wiederholungen in for-Schleifen"),
            #Dateien
            ("Was macht open()?",["Datei öffnen", "Liste erstellen", "Text löschen", "Sortieren"],"Datei","öffnet oder erstellt eine Datei"),
            ("Was macht open('r')?",["Löschen", "Schreiben", "Lesen", "Erstellen"],"Lesen","öffnet Datei zum Lesen"),
            ("Was macht open('w')?",["Lesen", "Schreiben", "Anhängen", "Vergleichen"],"Schreiben","öffnet Datei zum Schreiben"),
            #Bedingungen
            ("Was macht if?",["Bedingung", "Schleife", "Funktion", "Variable"],"Bedingung","prüft ob die bedingung wahr ist"),
            ("Was macht else?",["Start", "Wenn", "Stop", "Sonst"],"Sonst","alternative bedingungen wenn if falsch ist"),
            ("Was macht elif?",["Sonst-wenn", "Immer", "Stop", "Start"],"Sonst-wenn","weitere Bedingung wenn if falsch ist"),
            ("Was macht ==?",["Kleiner", "Ungleich", "Vergleich", "Größer"],"Vergleich","prüft ob zwei Werte gleich sind"),
            ("Was macht !=?",["Zuweisung", "Gleich", "Vergleich", "Ungleich"],"Ungleich","prüft ob Werte ungleich sind"),
            ("Was macht isalpha()?",["Leerzeichen", "Zahlen", "Buchstaben", "Symbole"],"Buchstaben","prüft ob nur Buchstaben vorhanden sind"),
            ("Was macht isdigit()?",["Zahlen", "Buchstaben", "Text", "Liste"],"Zahlen","prüft ob nur Zahlen vorhanden sind"),
            ("Was macht < ?",["gleich", "größer", "kleiner", "ungleich"],"kleiner","kleiner als"),
            ("Was macht > ?",["größer", "kleiner", "gleich", "ungleich"],"größer","größer als"),
            #Rechnen/Operatoren
            ("Was macht +?",["Minus", "Mal", "Plus", "Rest"],"Plus","addiert zwei Werte"),
            ("Was macht -?",["Plus", "Minus", "Mal", "Geteilt"],"Minus","subtrahiert Werte"),
            ("Was macht *?",["Geteilt", "Mal", "Plus", "Rest"],"Mal","multipliziert Werte"),
            ("Was macht /?",["Rest", "Mal", "Plus", "Geteilt"],"Geteilt","teilt Werte"),
            ("Was macht %?",["Rest", "Division", "Multiplikation", "Addition"], "Rest","gibt den Rest einer Division"),
            #GUI (tkinter)
            ("Was ist tkinter?",["Spiel", "Datenbank", "GUI", "Text"],"GUI","bibliothek für benutzeroberflächen (Grafische Darstellung"),
            ("Was macht pack()?",["Sortieren", "Raster", "Position", "Stapel"],"Stapel","ordnet Elemente untereinander an"),
            ("Was macht grid()?",["Stapel", "Raster", "Liste", "Position"],"Raster","ordnet Elemente in Tabellenform"),
            ("Was macht place()?",["Position", "Raster", "Stapel", "Liste"],"Position","setzt Elemente an feste Position"),
            #Entry / GUI Text
            ("Was macht entry.get()?",["Schreiben", "Lesen", "Löschen", "Sortieren"],"Lesen","holt Text aus Eingabefeld"),
            ("Was macht insert()?",["Teilen","Löschen","Vergleichen","Schreiben"],"Schreiben","fügt Text ein"),
            ("Was macht delete()?",["Ende","Trennen","Löschen","Lesen"],"Löschen","löscht Text"),
            ("Was ist entry?",["Feld","Sortieren","Lesen","Stapeln"],"Feld","Eingabefeld in GUI")
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
        self.user_answers = []    #pro spiel neue liste damit alte weg sind(Start ein neues Spiel = alles zurücksetzen)

        random.shuffle(self.questions)                          #mischt Reihenfolge zufällig (fragen Reihenfolge)

        self.frame_game = tkinter.Frame(self.root)              #Container für spiel seite
        self.frame_game.pack()

        self.question_label = tkinter.Label(self.frame_game, text="")
        self.question_label.pack()

        self.button_frame = tkinter.Frame(self.frame_game)     #Container für antwort buttons 2v2
        self.button_frame.pack()

        self.back_button = tkinter.Button(self.frame_game, text="Zurück", command=self.previous_question)
        self.back_button.pack(pady=5)

        #beenden knopf
        self.exit_button = tkinter.Button(self.frame_game,text="Beenden",command=self.back_to_menu_2)
        self.exit_button.pack(pady=10)
        #weiter knopf
        self.next_button = tkinter.Button(self.frame_game,text="Weiter",command=self.next_question)         #knopf in game weil dan nur 1 mal erstellt wird
        self.next_button.pack_forget()
        self.root.bind("<Return>", self.on_enter)               #<Return> = taste enter auf der Tastatur
        #Erklärungstext
        self.explanation_label = tkinter.Label(self.frame_game, text="", fg="blue", wraplength=300)      #wraplength = ab welcher Breite der Text automatisch umbricht
        self.explanation_label.pack(pady=10)
        self.buttons = []

        self.load_question()

    def on_enter(self, event):                                  #event : objekt infos wie mausposition, welche taste gedrückt ist etc
        self.next_question()

    def back_to_menu_2(self):
        self.frame_game.destroy()
        self.frame_buttons.pack(expand=True)

    def load_question(self):
        col = 0     #spalte
        row = 0     #zeile


        if hasattr(self, "buttons"):        #prüfen ob schon Buttons existieren
            # alle alten Buttons löschen
            for button in self.buttons:
                button.destroy()

            self.buttons = []

        question = self.questions[self.current_question]   #aktuelle Frage holen
        self.question_label.config(text=question[0])        #frage im Label anzeigen
        #erklärung zurücksetzen
        self.explanation_label.config(text="")

        for answer in question[1]:            #alle Antwortmöglichkeiten durchgehen (Am Ende der Schleife ist antwort immer der letzte Wert)
            # Button erstellen
            button = tkinter.Button(self.button_frame, text=answer)
            button.config(command=lambda a=answer, b=button: self.check_answer(a, b)) #a=platzhalter

            button.grid(row=row, column=col, padx=10, pady=10)
            self.buttons.append(button)

            col += 1
            if col > 1:         #größer als 2 (buttons) neue Zeile
                col = 0
                row += 1

    def check_answer(self, selected_answer, button):

        correct_answer = self.questions[self.current_question][2]

        #Erklärung holen
        explanation = self.questions[self.current_question][3]

        if selected_answer == correct_answer:
            button.config(bg="green")
            self.score_v += 1
        else:
            button.config(bg="red")

        #richtige Antwort IMMER grün anzeigen
        for all_button in self.buttons:
            if all_button["text"] == correct_answer:
                all_button.config(bg="green")

        #alle Buttons deaktivieren das nur noch 1x mal wählen möglich ist
        for all_button in self.buttons:
            all_button.config(state="disabled")

        self.next_button.pack(pady=10)
        self.explanation_label.config(text=explanation)
        self.user_answers.append(selected_answer)

    def previous_question(self):
        if self.current_question > 0:
            self.current_question -= 1
            self.load_question()

            #alte antwort
            prev_answer = self.user_answers[self.current_question]
            correct_answer = self.questions[self.current_question][2]

            for button in self.buttons:
                if button["text"] == prev_answer:
                    if prev_answer == correct_answer:
                        button.config(bg="green")
                    else:
                        button.config(bg="red")

                if button["text"] == correct_answer:
                    button.config(bg="green")

                # Buttons deaktivieren
            for button in self.buttons:
                button.config(state="disabled")

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

        button_back = tkinter.Button(self.frame_score, text="Zurück", command=self.back_to_menu_1)
        button_back.pack(pady=10)
        button_delete = tkinter.Button(self.frame_score,text="Score löschen",command=self.delete_score)
        button_delete.pack(pady=10)

    def back_to_menu_1(self):
        self.frame_score.destroy()
        self.frame_buttons.pack(expand=True)

    def exit_game(self):
        self.save_score()
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

    def save_score(self):
        if not self.selected_player:
            mb.showwarning("Fehler", "Kein Spieler gewählt,Speichern nicht möglich")
            return

        self.c.execute(
            "UPDATE quiz SET score = ? WHERE player = ?",
            (self.score_v, self.selected_player))
        self.conn.commit()

root=tkinter.Tk()
game = quiz_game(root)
root.mainloop()