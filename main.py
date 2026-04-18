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
        try:
            self.c.execute("ALTER TABLE quiz ADD COLUMN games INTEGER DEFAULT 0")
        except:
            pass

        self.conn.commit()
        self.root = root
        self.root.title("Vokabel Quiz")
        self.root.geometry("300x400")

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
            ("Was ist int()?",["Ganzzahl","Text","Kommas","True/false"],"Ganzzahl","Wandelt einen Wert in eine Ganzzahl um, dabei werden Nachkommastellen entfernt (z. B. 5.7 wird zu 5)"),
            ("Was macht str()?",["Zahl","Text","Komma","Liste"],"Text","Wandelt einen Wert in einen Text (String) um, z. B. wird 5 zu '5'"),
            ("Was ist der Datentyp bool?",["Text","True/False","Zahl","Liste"],"True/False","Ein Datentyp, der nur zwei Werte kennt: True (wahr) oder False (falsch)"),
            ("Was macht float()?",["Ganzzahl","Text","Kommazahl","Liste"],"Kommazahl","Wandelt einen Wert in eine Kommazahl um, z. B. wird 5 zu 5.0"),
            ("Was macht import?",["Funktion","lädt Modul","Variable","erstellt schleife"],"lädt Modul","Lädt ein externes Modul oder eine Bibliothek, um zusätzliche Funktionen zu nutzen"),
            ("Was macht print()?",["Ausgabe","Eingabe","Datei","Liste"],"Ausgabe","Gibt Werte oder Text im Terminal bzw. auf dem Bildschirm aus"),
            ("Was macht input()?",["Berechnung","Eingabe","Ausgabe","Datai"],"Eingabe","Fordert den Benutzer zur Eingabe auf und gibt den eingegebenen Text als String zurück"),
            #funktionen
            ("Was ist def?",["Funktion", "Variable", "Schleife", "Import"],"Funktion","Definiert eine eigene Funktion, die später wiederverwendet werden kann"),
            ("Was macht return?",["Ausgabe", "Rückgabe", "Abbruch", "Vergleich"],"Rückgabe","Gibt ein Ergebnis aus einer Funktion zurück, sodass es weiterverwendet werden kann"),
            ("Was ist ein Parameter?",["Variable", "Liste", "Funktion", "Wert"],"Wert","Ein Wert, der einer Funktion beim Aufruf übergeben wird"),
            #Listen & Text
            ("Was macht len()?",["Index", "Zählen", "Länge", "Sortieren"],"Länge","Gibt die Anzahl der Elemente in einer Liste oder die Länge eines Textes zurück"),
            ("Was macht die Methode split()?",["Trennen", "Verbinden", "Löschen","Sortieren"],"Trennen","Teilt einen Text in mehrere Teile und gibt diese als Liste zurück"),
            ("Was macht die Methode strip()?",["Teilen", "Text kürzen", "Zählen","Leerzeichen entfernen"],"Leerzeichen entfernen","Entfernt Leerzeichen oder bestimmte Zeichen am Anfang und Ende eines Textes(\\n wäre Zeilenumbruch)"),
            ("Was macht die Methode lower()?",["klein", "groß", "löschen", "trennen"],"klein","Wandelt alle Buchstaben eines Textes in Kleinbuchstaben um"),
            ("Was macht die Methode upper()?",["anhängen", "klein", "groß", "löschen"],"groß","Wandelt alle Buchstaben eines Textes in Großbuchstaben um"),
            #Listen Funktionen
            ("Was macht die Methode append()?",["Hinzufügen", "Löschen", "Sortieren", "Teilen"],"Hinzufügen","Fügt ein neues Element am Ende einer Liste hinzu"),
            ("Was macht die Methode remove()?",["Sortieren", "Hinzufügen", "Löschen", "Kopieren"],"Löschen","Entfernt ein bestimmtes Element aus einer Liste"),
            ("Was macht die Methode pop()?",["Letztes", "Erstes", "Alles", "Sortieren"],"Letztes","Entfernt das letzte Element aus einer Liste und gibt es zurück"),
            ("Was macht die Methode sort()?",["Mischen", "Sortieren", "Löschen", "Kopieren"],"Sortieren","Sortiert die Elemente einer Liste in aufsteigender Reihenfolge"),
            ("Was ist [] in Python?",["Liste", "Text", "Zahl", "Funktion"],"Liste","Erstellt eine Liste, in der mehrere Werte gespeichert werden können"),
            ("Was macht die Methode index?",["Position", "Wert", "Sortieren", "Zählen"],"Position","Gibt die Position (Index) eines bestimmten Elements in einer Liste zurück"),
            ("Was macht der Operator in?",["Addieren", "Vergleich", "Sortieren", "Enthalten"],"Enthalten","Prüft, ob ein bestimmter Wert in einer Liste oder einem Text enthalten ist"),
            #Schleifen / range
            ("Was macht eine for-Anweisung?",["Funktion", "Bedingung", "Schleife", "Variable"],"Schleife","Wiederholt einen Codeblock für jedes Element einer Sequenz oder eine bestimmte Anzahl von Malen"),
            ("Wofür wird eine while-Schleife verwendet?",["Vergleich", "Wiederholung", "Funktion", "Import"],"Wiederholung","Wiederholt einen Codeblock so lange, wie eine Bedingung wahr ist"),
            ("Was macht break in einer Schleife?",["Stop", "Weiter", "Start", "Vergleich"],"Stop","Beendet eine Schleife sofort, auch wenn die Bedingung noch wahr ist"),
            ("Was macht continue in einer Schleife?",["Reset", "Stop", "Weiter", "Ende"],"Weiter","Überspringt den aktuellen Durchlauf einer Schleife und fährt mit dem nächsten fort"),
            ("Was macht range(5)?",["Text", "Liste löschen", "Sortieren", "Zahlenreihe"],"Zahlenreihe","Erzeugt eine Zahlenreihe von 0 bis 4."),
            ("Was gibt range(5) zurück?",["0-5", "1-5", "0-4", "1-4"], "0-4","Gibt eine Sequenz von Zahlen von 0 bis 4 zurück."),
            ("Wofür nutzt man range()?",["Speichern", "Vergleich", "Sortieren", "Wiederholung"],"Wiederholung","Wird verwendet, um eine bestimmte Anzahl von Wiederholungen in Schleifen zu erzeugen"),
            #Dateien
            ("Was macht open()?",["Datei öffnen", "Liste erstellen", "Text löschen", "Sortieren"],"Datei","Öffnet eine Datei oder erstellt sie, falls sie nicht existiert"),
            ("Was macht open('r')?",["Löschen", "Schreiben", "Lesen", "Erstellen"],"Lesen","Öffnet eine Datei im Lesemodus, um ihren Inhalt zu lesen"),
            ("Was macht open('w')?",["Lesen", "Schreiben", "Anhängen", "Vergleichen"],"Schreiben","Öffnet eine Datei im Schreibmodus und überschreibt den bestehenden Inhalt"),
            #Bedingungen
            ("Wofür wird eine if-Anweisung verwendet?",["Bedingung", "Schleife", "Funktion", "Variable"],"Bedingung","Prüft, ob eine Bedingung wahr ist und führt dann den entsprechenden Code aus"),
            ("Wofür wird else verwendet?",["Start", "Wenn", "Stop", "Sonst"],"Sonst","Führt Code aus, wenn die Bedingung von if nicht erfüllt ist"),
            ("Wofür wird elif verwendet ?",["Sonst-wenn", "Immer", "Stop", "Start"],"Sonst-wenn","Prüft eine weitere Bedingung, wenn die vorherige if-Bedingung falsch war"),
            ("Was macht der Operator ==?",["Kleiner", "Ungleich", "Vergleich", "Größer"],"Vergleich","Vergleicht zwei Werte und prüft, ob sie gleich sind"),
            ("Was macht der Operator !=?",["Zuweisung", "Gleich", "Vergleich", "Ungleich"],"Ungleich","Vergleicht zwei Werte und prüft, ob sie ungleich sind"),
            ("Was macht die Methode isalpha()?",["Leerzeichen", "Zahlen", "Buchstaben", "Symbole"],"Buchstaben","Prüft, ob ein Text nur aus Buchstaben besteht"),
            ("Was macht die Methode isdigit()?",["Zahlen", "Buchstaben", "Text", "Liste"],"Zahlen","Prüft, ob ein Text nur aus Ziffern besteht"),
            ("Was macht der Operator < ?",["gleich", "größer", "kleiner", "ungleich"],"kleiner","Prüft, ob ein Wert kleiner als ein anderer ist"),
            ("Was macht der Operator > ?",["größer", "kleiner", "gleich", "ungleich"],"größer","Prüft, ob ein Wert größer als ein anderer ist"),
            #Rechnen/Operatoren
            ("Was macht der Operator +?",["Minus", "Mal", "Plus", "Rest"],"Plus","Addiert zwei Werte miteinander"),
            ("Was macht der Operator -?",["Plus", "Minus", "Mal", "Geteilt"],"Minus","Subtrahiert einen Wert von einem anderen"),
            ("Was macht der Operator *?",["Geteilt", "Mal", "Plus", "Rest"],"Mal","Multipliziert zwei Werte miteinander"),
            ("Was macht der Operator /?",["Rest", "Mal", "Plus", "Geteilt"],"Geteilt","Teilt einen Wert durch einen anderen"),
            ("Was macht der Operator %?",["Rest", "Division", "Multiplikation", "Addition"], "Rest","Gibt den Rest einer Division zurück"),
            #GUI (tkinter)
            ("Was ist tkinter?",["Spiel", "Datenbank", "GUI", "Text"],"GUI","Eine Bibliothek zur Erstellung von grafischen Benutzeroberflächen (GUI) in Python"),
            ("Was macht die Methode pack()?",["Sortieren", "Raster", "Position", "Stapel"],"Stapel","Ordnet GUI-Elemente untereinander oder nebeneinander an"),
            ("Was macht die Methode grid()?",["Stapel", "Raster", "Liste", "Position"],"Raster","Ordnet GUI-Elemente in einer Tabellenstruktur mit Zeilen und Spalten an"),
            ("Was macht die Methode place()?",["Position", "Raster", "Stapel", "Liste"],"Position","Platziert GUI-Elemente an einer festen Position im Fenster"),
            #Entry / GUI Text
            ("Was macht die Methode entry.get()?",["Schreiben", "Lesen", "Löschen", "Sortieren"],"Lesen","Liest den aktuellen Text aus einem Eingabefeld aus"),
            ("Was macht die Methode insert()?",["Teilen","Löschen","Vergleichen","Schreiben"],"Schreiben","Fügt Text an einer bestimmten Position in ein Feld ein"),
            ("Was macht die Methode delete()?",["Ende","Trennen","Löschen","Lesen"],"Löschen","Löscht Text aus einem Eingabefeld"),
            ("Was ist ein Entry in einer GUI ?",["Feld","Vergleich","Zeile","Stapeln"],"Feld","Ein Eingabefeld in einer GUI, in das der Benutzer Text eingeben kann")
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
            mb.showinfo("Fehler","Bitte Namen eingeben")
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
        button_back = tkinter.Button(self.frame_select_player, text="Zurück", command=self.back_to_menu_select)
        button_back.pack(pady=10)

    def back_to_menu_select(self):
        self.frame_select_player.destroy()
        self.frame_buttons.pack(expand=True)

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
        self.correct_count = 0
        self.wrong_count = 0
        self.user_answers = []    #pro spiel neue liste damit alte weg sind(Start ein neues Spiel = alles zurücksetzen)

        random.shuffle(self.questions)                          #mischt Reihenfolge zufällig (fragen Reihenfolge)
        #fragenzähler frame
        self.frame_game = tkinter.Frame(self.root)
        self.frame_game.pack()
        self.progress_label = tkinter.Label(self.frame_game, text="")
        self.progress_label.pack()

        self.frame_game = tkinter.Frame(self.root)              #Container für spiel seite
        self.frame_game.pack()

        self.question_label = tkinter.Label(self.frame_game, text="")
        self.question_label.pack()

        self.button_frame = tkinter.Frame(self.frame_game)     #Container für antwort buttons 2v2
        self.button_frame.pack()

        self.back_button = tkinter.Button(self.frame_game, text="Zurück", command=self.previous_question)
        self.back_button.pack(pady=5)

        #weiter knopf
        self.next_button = tkinter.Button(self.frame_game,text="Weiter",command=self.next_question)         #knopf in game weil dan nur 1 mal erstellt wird
        self.next_button.pack_forget()

        #beenden knopf
        self.exit_button = tkinter.Button(self.frame_game,text="Beenden",command=self.back_to_menu_2)
        self.exit_button.pack(pady=10)

        #Erklärungstext
        self.explanation_label = tkinter.Label(self.frame_game, text="", fg="blue", wraplength=300)      #wraplength = ab welcher Breite der Text automatisch umbricht
        self.explanation_label.pack(pady=10)
        self.buttons = []

        self.load_question()

    def back_to_menu_2(self):
        self.save_score()
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

        self.question_counter()

    def question_counter(self):
        total = len(self.questions)
        current = self.current_question + 1
        self.progress_label.config(text=f"Frage {current} von {total}")

    def check_answer(self, selected_answer, button):
        correct_answer = self.questions[self.current_question][2]

        #Erklärung holen
        explanation = self.questions[self.current_question][3]

        if selected_answer == correct_answer:
            button.config(bg="green")
            self.score_v += 1
            self.correct_count += 1
        else:
            button.config(bg="red")
            self.wrong_count += 1

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

        if self.current_question < len(self.questions):              #<len() = bin ich noch im Bereich
            self.load_question()
        else:
            total = len(self.questions)
            prozent = (self.correct_count / total) * 100

            if prozent >= 90:
                grade = "Sehr gut"
            elif prozent >= 75:
                grade = "Gut"
            elif prozent >= 60:
                grade = "Befriedigend"
            elif prozent >= 50:
                grade = "Ausreichend"
            else:
                grade = "Verbesserungswürdig"

            mb.showinfo("Fertig,Ergebnis",f"Richtig: {self.correct_count}\n"
                                                       f"Falsch: {self.wrong_count}\n "
                                                       f"Dein Score: {self.score_v}\n"
                                                       f"Prozent: {prozent:.1f}%\n"
                                                       f"Note: {grade}")
            self.save_score()


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
        self.c.execute("SELECT player, score,games FROM quiz")
        scores = self.c.fetchall()

        # in liste eintragen
        for s in scores:
            self.listbox.insert(tkinter.END,f"{s[0]} - {s[1]} Punkte - {s[2]} Spiele")

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
            "UPDATE quiz SET score = score + ?, games = games +1 WHERE player = ?",
            (self.score_v, self.selected_player))
        self.conn.commit()

root=tkinter.Tk()
game = quiz_game(root)
root.mainloop()