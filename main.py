import csv
from collections import deque
import time
import os

def einlesenDesSpielfelds(startfeld):

    file_path = "spielfeldtest.txt"

    with open (file_path) as csv_file:
        
        csv_reader = csv.reader(csv_file, delimiter=";")
        
        lineCounter = 0

        for ersterEintrag in csv_reader:

            y_höhe = int(ersterEintrag[0])
            x_breite = int(ersterEintrag[1])
            break
        

        spielfeld = [[]] * y_höhe

        for row in csv_reader:
            spielfeld[lineCounter]=row
            lineCounter += 1
            #print(lineCounter)
        
        if lineCounter != y_höhe:
            return "Y-Falsch" 

        if len(spielfeld[0]) != x_breite: 
            return "X-Falsch" 

        try:
            if (spielfeld[startfeld[0] -1 ][startfeld[1]- 1 ] == "0"): # Wichtig String, kein Integer.
                spielfeld[startfeld[0] -1 ][startfeld[1]- 1 ] = "S" # Minus eins, wegen der Nullindexierung.
            
            elif (spielfeld[startfeld[0] -1 ][startfeld[1]- 1 ] == "1"):
                print("Dieses Feld ist ein Wandfeld, bitte geben sie ein Pfadfeld als Startpunkt an.")
                return 42 # Fehlercode für die weitere Verarbeitung.


        except:
            print("Das angegebene Feld ist nicht im Bereich des Spielfelds, bitte geben sie ein enthaltenes Feld an.")
            return 42 # Fehlercode für die weitere Verarbeitung.

    
    return spielfeld, file_path

def nutzerEingabeStartpunkt():

    try:

        y = int(input("Bitte geben sie die y-Koordinate des Startpunktes ein: "))

        if y < 1:
            print("Eingabe fehlerhaft. Bitte wähle eine y-Koordinate größer 0.")
            y, x = nutzerEingabeStartpunkt()

        else: x = int(input("Bitte geben sie die x-Koordinate des Startpuntes ein: "))

        if x < 1:

            print("Eingabe fehlerhaft. Bitte wähle eine x-Koordinate größer 0.")
            y, x = nutzerEingabeStartpunkt()

    except:

        print("Eingabe fehlerhaft. Bitte gib eine natürliche Zahl ein.")
        y, x = nutzerEingabeStartpunkt()
    startfeld = [y, x]

    return startfeld

def nutzerEingabeZeit():
    try:
        i=input("Bitte wähle die Aktualisierungsrate der Schritte in Sekunden: ")
        i=int(i)
        return i
    except:
        print("Bitte gebe eine natürliche Zahl ein")
        i=nutzerEingabeZeit()
        return i

# In den Vorgaben ist vorrausgesetzt, dass es einen Endpunkt gibt.
def sucheEndpunkt(spielfeld):

    i = 0
    j = 0

    for zeile in spielfeld:
        
        for feld in zeile:
            
            if feld == "X":
                endfeld = [i,j]
                return endfeld # Rückgabe mit Nullindexierung.
            elif feld != "X":
                j += 1
        j = 0 # Zurücksetzen der X-Koordinate.
        i += 1

def checkInputCorrect(spielfeld, file_path):

    while spielfeld == 42:                       # 42 wegen dem Fehlercode der von uns zurück gegeben wird.
        startfeld = nutzerEingabeStartpunkt()
        spielfeld = einlesenDesSpielfelds(file_path, startfeld)

    if spielfeld == "X-Falsch" or spielfeld == "Y-Falsch": #Change
        print("Die Dimensionen des geladenen Spielfelds stimmen nicht mit den tatsächlichen Dimensionen über ein.")
        print("Bitte starten sie das Programm nach Anpassungen neu.")
        time.sleep(10000)

def bfsAlgorithmus(spielfeld, start, ende): 

    # Erstelle double ended queue für den Algorithmus.
    queue = deque()
    queue.append(start)
    
    # Menge für die schon begangenen Felder.
    visited = set()
    visited.add(tuple(start))

    # Menge für die parent-node.
    parent = {}
    parent[tuple(start)] = None


    ende[0] = ende[0] + 1 # Anpassung für die Darstellungsform.
    ende[1] = ende[1] + 1

    # Starte BSF-Algorithmus
    while queue:
    # Neue Node zuweisen.
        node = queue.popleft()

        

    # Checken ob das Ende erreicht wurde.
        if tuple(node) == tuple(ende):
        # Ausbauen des Ergebnispfades
            path = []
            while node:
                path.append(node)
                node = parent[tuple(node)]
            path.reverse()
            return path
    
        # Nachbarn auslesen aus der anderen Methode.
        neighbors = findeNachbarn(spielfeld, node)

        # Hinzufügen der noch nicht begangenen Nachbarfelder:
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = node
                queue.append(neighbor)

    # Wenn diese Stelle erreicht wird, gibt es keinen Lösungsweg und es wird nun returned.
    return None

def findeNachbarn(spielfeld, node):
    # Dimensionen des Spielfelds:
    zeilen = len(spielfeld)  + 1
    spalten = len(spielfeld[0]) + 1

    # Auslesen der Position der Node.
    zeile, spalte = node

    # Auflistung der möglichen Bewegungen auf dem Spielfeld:
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Nachbarn auslesen:
    neighbors = []
    for move in moves:
        new_row = zeile + move[0]
        new_col = spalte + move[1]

        # Die ausgelesenen Felder in der CSV-Datei werden immer als Stings ausgelesen, deswegen hier nicht auf int, sondern aus String prüfen.
        if spielfeld[new_row -1][new_col -1] == "0" or spielfeld[new_row -1][new_col -1] == "X":
            if 0 <= new_row < zeilen and 0 <= new_col < spalten and spielfeld[new_row -1][new_col - 1] != "#": # Wichtigste Prüfenung für den Nachbarn.
                neighbors.append((new_row, new_col))
        elif spielfeld[new_row -1][new_col -1 ] == "1": # Wenn es ein Wandfeld ist, dann hier nur mit der Schleife weiter machen.
            continue

    return neighbors

def bildschirmAusgabe(ergebnisRoute, spielfeld, aktualisierungsrate):

    durchlauf = 0

    if ergebnisRoute == None:
        print("Das Spielfeld hat keine Ergebnisroute und ist damit in dieser Form nicht lösbar. Bitte nehmen sie Anpassungen vor.")

    elif ergebnisRoute != None:
        os.system("cls")
        # Auslesen der einzelnen Schritte:
        for menge in ergebnisRoute:
            wertepaar = []
            for element in menge:
                wertepaar.append(element)
            y = wertepaar[0]
            x = wertepaar[1]

            spielfeld[y-1][x-1] = "#"
            
            # Ausgabe nur für das Ausgangsspielfeld:
            if(durchlauf == 0):
                os.system("cls")
                durchlauf += 1
                print("Anfangsspielfeld:\n")
                for zeile in spielfeld: 
                    print(zeile)
                print("\nSpielfeld wird nach der Zeitvorgabe geladen...")
                time.sleep(aktualisierungsrate)
            
            # Ausgabe für alle anderen Schritte:
            elif(durchlauf != 0):
                os.system("cls")
                print("Schritt: " + str(durchlauf) + "\n")
                for zeile in spielfeld: 
                    print(zeile)
                print("\nSpielfeld wird nach der Zeitvorgabe geladen...")
                durchlauf += 1
                time.sleep(aktualisierungsrate
                )
        # Ausgabe nur von dem Endergebnis:
        os.system("cls")
        print("Endergebnis: \n")
        for zeile in spielfeld:
            print(zeile)
        print("\nZielroute:", ergebnisRoute)

        if(len(ergebnisRoute) == 1):
            print("\nDas Startfeld ist gleich dem Zielfeld!")

        print("")

def nochmalSpielen():
    time.sleep(2)
    b = True
    while (b):
        i=input("Nochmal spielen? Schreiben Sie Ja/Nein: ")
        if (i=="Ja" or i=="ja" or i=="jo" or i=="Yessssir"):
            main()
            b=False 
        elif (i=="Nein" or i=="Ne" or i=="nein"):
            print("\nAuf Wiedersehen!")
            b = False
            break
            
        else:
            print("Bitte geben sie eine der beiden Auswahlmöglichkeiten ein (Ja/Nein)")

def main():

    startfeld = nutzerEingabeStartpunkt()
    
    aktualisierungsrate = nutzerEingabeZeit()

    spielfeld, file_path = einlesenDesSpielfelds(startfeld)

    checkInputCorrect(spielfeld, file_path)

    endfeld = sucheEndpunkt(spielfeld)
    
    ergebnisRoute = bfsAlgorithmus(spielfeld, startfeld, endfeld)

    bildschirmAusgabe(ergebnisRoute, spielfeld, aktualisierungsrate)

    nochmalSpielen()
    
if __name__ == "__main__":
    main() 