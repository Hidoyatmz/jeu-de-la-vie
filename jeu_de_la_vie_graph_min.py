# Zaidi Mehdi
# Projet final python : Jeu de la vie
# Début : 08/04/2021 13:50
# Fin   : 09/04/2021 16:30

# Dépendances
from random import random, randint
from time import sleep
from copy import deepcopy
from graphics import *

def generateGrid(lines, columns, p):
    """Créé une grille de 'lines' lignes et 'columns' colonnes.
    Param : (int) lines   : nombre de lignes
            (int) columns : nombre de colonnes
            (float) p     : chance d'avoir une célulle vivante.
    Contrainte : La grille ne doit pas etre vide.
    Return: (list) grid : une liste de dimension lines contenant chacune columns éléments.
    """
    grid = []
    isAlive = False
    for ligne in range(lines):
        grid.append([])
        for _ in range(columns):
            chance = random()
            if(chance < p):
                isAlive = True
            if(isAlive):
                grid[ligne].append(1)
            else:
                grid[ligne].append(0)
            isAlive = False
    return grid

def getVerticalBoxes(grid):
    """Renvoi le nombre de cases vertical d'une grille.
    Param : (list) grid : Grille
    Contrainte : La grille ne doit pas etre vide.
    Return : (int) : Nombre de cases de la grille verticalement
    """
    return len(grid)

def getHorizontalBoxes(grid):
    """Renvoi le nombre de cases horizontal d'une grille.
    Param : (list) grid : Grille
    Contrainte : La grille ne doit pas etre vide.
    Return : (int) : Nombre de cases de la grille horinzontalement
    """
    return len(grid[0])

def displayGrid(grid):
    """Affiche ligne par ligne une grille existante en remplacent les 1 par des O et les 0 par des _.
    Param : (list) grid : Grille
    Contrainte : La grille ne doit pas etre vide.
    """
    caractere = ""
    for ligne in grid:
        for element in ligne:
            if(element == 1):
                caractere = "O"
            else:
                caractere = "_"
            print(caractere, end =" ")
        print("\n")

def getBoxNeighbours(grid,x,y):
    """ Retourne le nombre de voisins par element de la grille.
        Le nombre est affiché dans une liste gardant la même position que l'element.
        Param : (list) grid : La grille
                (int)  x    : La ligne de l'element
                (int)  y    : La colonne de l'element
        Contrainte : La grille ne doit pas etre vide et un element doit exister a la position donné.
        Return : (list) Une grille comportant le nombre de voisins a l'emplcement de chaque elements.
    """
    neighbours = []
    totalColumns = getHorizontalBoxes(grid)-1 # Un tableau commence à 0.
    totalLines = getVerticalBoxes(grid)-1 # Un tableau commence à 0.
    for line in range(x-1,x+2):
        if(line >= 0 and not line > totalLines):
            for column in range(y-1,y+2):
                if(column >= 0 and not column > totalColumns):
                    if(line != x or column != y):
                        neighbours.append(grid[line][column])
    return neighbours

def getBoxNeighboursAlive(grid,x,y):
    """ Retourne le nombre de voisin pour un element de la grille pour une position donnée.
        Param : (list) grid : La grille
                (int)  x    : La ligne de l'element
                (int)  y    : La colonne de l'element
        Contrainte : La grille ne doit pas etre vide et un element doit exister a la position donné.
        Return : (int) le nombre de voisins de l'element donné.
    """
    neighbours = getBoxNeighbours(grid,x,y)
    alive = 0
    for k in neighbours:
        if(k == 1):
            alive += 1
    return alive

def displayGridFormat(grid):
    """ Affiche une grille ligne par ligne, séparé de tirets et comportant le numero de la ligne avant les elements.
        Param : (list) grid : La grille à afficher.
        Contrainte : La grille ne doit pas etre vide.
        Exemple :
          -------------------------
        0)|  0  |  1  |  0  |  1  |
          -------------------------
    """
    lineIndex = 0
    separator = "------"
    for line in range(getVerticalBoxes(grid)):
        print("   "+separator*getHorizontalBoxes(grid),"\n")
        print(str(lineIndex)+")|", end =" ")
        for column in range(getHorizontalBoxes(grid)):
            print(" "+str(grid[line][column])+"  |", end =" ")
        print("\n")
        print("   "+separator*getHorizontalBoxes(grid),"\n")
        lineIndex += 1

def displayNeighboursAliveGrid(grid):
    """ Affiche une grille ligne par ligne, séparé de tirets et comportant le numero de la ligne avant les elements.
        De plus, les éléments sont remplacé par leur nombre de voisins.
        Param : (list) grid : La grille à afficher.
        Contrainte : La grille ne doit pas etre vide.
        Exemple :
          -------------------------
        0)|  3  |  2  |  3  |  1  |
          -------------------------
    """
    lineIndex = 0
    separator = "------"
    for line in range(getVerticalBoxes(grid)):
        print("   "+separator*getHorizontalBoxes(grid),"\n")
        print(str(lineIndex)+")|", end =" ")
        for column in range(getHorizontalBoxes(grid)):
            print(" "+str(getBoxNeighboursAlive(grid,line,column))+"  |", end =" ")
        print("\n")
        print("   "+separator*getHorizontalBoxes(grid),"\n")
        lineIndex += 1

def displayGridChecker(grid):
    """ Affiche une grille ligne par ligne, séparé de tirets et comportant le numero de la ligne avant les elements.
        Param : (list) grid : La grille à afficher.
        Contrainte : La grille ne doit pas etre vide.
        Exemple :
          -------------------------
        0)|  0  |  1  |  0  |  1  |
          -------------------------
    """
    lineIndex = 0
    nextGeneration = generateNextGen(grid)
    separator = "   -----------------------------------------------------------------------------------"
    for line in range(getVerticalBoxes(grid)):
        print(separator,"\n")
        print(str(lineIndex)+")|", end =" ")
        for column in range(getHorizontalBoxes(grid)):
            print(" "+str(grid[line][column])+"  |", end =" ")
        print("| | | ", end =" ")
        for column in range(getHorizontalBoxes(grid)):
            print(""+str(getBoxNeighboursAlive(grid,line,column))+"  |", end =" ")
        print("| | | ", end =" ")
        for column in range(getHorizontalBoxes(grid)):
            print(""+str(nextGeneration[line][column])+"  |", end =" ")
        print("\n")
        print(separator,"\n")
        lineIndex += 1

def generateNextGen(grid,window,cellsInfo):
    """ Genere une nouvelle grille étant celle de la prochaine génération en respectant les 3 conditions de remplacement des éléments.
    Param : (list) grid : La grille servant pour generer la prochaine génération.
    Contrainte : (list) grid : La grille ne doit pas etre vide.
    Return : (list) Grille de la nouvelle génération.
    """
    newGrid = deepcopy(grid)
    voisins = 0
    totalCells = getHorizontalBoxes(grid)*getVerticalBoxes(grid)
    currentCellsAlive = 0
    availableColors = ["white","#00ffff","#00FF00"]
    colorIndex = 0
    for line in range(getVerticalBoxes(grid)):
        for column in range(getHorizontalBoxes(grid)):
            voisins = getBoxNeighboursAlive(grid,line,column)
            colorIndex = randint(0,len(availableColors)-1)
            if(voisins == 3):
                newGrid[line][column] = 1
                Point(line+50-(getVerticalBoxes(grid)/2), column+50-(getHorizontalBoxes(grid)/2)).draw(window).setFill(availableColors[colorIndex])
            elif(voisins < 2 or voisins > 3):
                newGrid[line][column] = 0
                Point(line+50-(getVerticalBoxes(grid)/2), column+50-(getHorizontalBoxes(grid)/2)).draw(window).setFill("#141414")
            if(newGrid[line][column] == 1):
                currentCellsAlive +=1
            if(currentCellsAlive < 10):
                cellsInfo.setText("Cellules en vie : 0"+str(currentCellsAlive)+"/"+str(totalCells))
            else:
                cellsInfo.setText("Cellules en vie : "+str(currentCellsAlive)+"/"+str(totalCells))
    return newGrid

def gridEvolution(grid,n,window):
    print("Grille initiale :\n",grid)
    newGrid = deepcopy(grid)
    generationIndex = 0
    generation = Text(Point(90,2), '')
    generation.setTextColor("white")
    generation.draw(window)
    cellsInfo = Text(Point(15,2), '')
    cellsInfo.setTextColor("white")
    cellsInfo.draw(window)
    sleep(0.1)
    for i in range(n):
        sleep(0.5)
        generationIndex += 1
        generation.setText('Generation '+str(generationIndex)+"/"+str(n))
        newGrid = generateNextGen(newGrid,window,cellsInfo)
        print("Génération n°",i+1,"\n",newGrid) # Dans la version graphique, cette ligne sert uniquement de visualisation dans le shell.
        if(generationIndex == n):
            endMessage = Text(Point(50,30), "Terminé ! :)")
            endMessage.setTextColor("white")
            endMessage.setSize(36)
            endMessage.draw(window)
            sleep(3)
            window.close()

def simulate_loading():
    print("Génération en cours...")
    sleep(2)
    print("3", end=" ")
    sleep(1)
    print("2", end=" ")
    sleep(1)
    print("1", end=" ")
    sleep(1)

def main():
    print("-------------------------")
    print("----- Jeu de la vie -----")
    print("-------------------------")
    print("Le jeu de la vie est une modélisation simpliste de la vie de cellules dans l’espace.")
    choix = int(input("1. Définir les options\n2. Mode alternance de forme\nChoix (1 ou 2) : "))
    if(choix == 2):
        generations = int(input("Entrez un entier, servant de nombre de générations : "))
        simulate_loading()
        win = GraphWin("Jeu de la vie",width = 800, height = 800)
        win.setBackground("#141414")
        win.setCoords(100,100,0,0)
        author = Text(Point(93,98), 'Zaidi Mehdi')
        author.setTextColor("white")
        author.draw(win)
        version = Text(Point(3,98), 'v0.5')
        version.setTextColor("white")
        version.draw(win)
        gridEvolution([[0, 0, 1, 0], [1, 0, 0, 1], [1, 0, 0, 1], [0, 1, 0, 0]],generations,win)
    else:
        lines = int(input("Entrez un entier, servant de nombre de lignes : "))
        columns = int(input("Entrez un entier, servant de nombre de colonnes : "))
        chance = float(input("Entrez un flotant (0-1), servant du taux de probabilité de présence d'une céllule : "))
        generations = int(input("Entrez un entier, servant de nombre de générations : "))
        simulate_loading()
        win = GraphWin("Jeu de la vie",width = 800, height = 800)
        win.setBackground("#141414")
        win.setCoords(100,100,0,0)
        author = Text(Point(93,98), 'Zaidi Mehdi')
        author.setTextColor("white")
        author.draw(win)
        version = Text(Point(3,98), 'v0.5.2')
        version.setTextColor("white")
        version.draw(win)
        grid = generateGrid(lines,columns,chance)
        gridEvolution(grid,generations,win)
