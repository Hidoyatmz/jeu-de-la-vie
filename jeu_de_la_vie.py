# Zaidi Mehdi
# Projet final python : Jeu de la vie
# Début : 08/04/2021 13:50
# Fin   : 09/04/2021 16:30

# Dépendances
from random import random
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
        grid.append([]) # Creation d'une nouvelle ligne.
        for _ in range(columns):
            chance = random()
            if(chance < p):
                isAlive = True
            if(isAlive):
                grid[ligne].append(1) # Insertion dans la ligne, d'une célulle vivante
            else:
                grid[ligne].append(0) # Insertion dans la ligne, d'une célulle morte
            isAlive = False
    return grid

def getVerticalBoxes(grid):
    """Renvoi le nombre de cases vertical d'une grille.
    Param : (list) grid : Grille
    Contrainte : La grille ne doit pas etre vide.
    Return : (int) : Nombre de cases de la grille verticalement
    """
    return len(grid) # Nombre d'éléments vertical (<=> nombre de lignes)

def getHorizontalBoxes(grid):
    """Renvoi le nombre de cases horizontal d'une grille.
    Param : (list) grid : Grille
    Contrainte : La grille ne doit pas etre vide.
    Return : (int) : Nombre de cases de la grille horinzontalement
    """
    return len(grid[0]) # Nombre d'éléments dans une ligne (<=> nombre de colonnes)

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
        print("\n") # Retour à la ligne après affichage d'une ligne avec les colonnes cotes à cotes.

def getBoxNeighbours(grid,x,y):
    """ Retourne le nombre de voisins pour un element de la grille.
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
                    if(line != x or column != y): # Verification que l'element n'est pas lui même.
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
    neighbours = getBoxNeighbours(grid,x,y) # Recuperation de tout les voisins de l'element.
    alive = 0
    for k in neighbours:
        if(k == 1):
            alive += 1 # Le voisin en question est une cellule vivante, on incrémente le compteur.
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
    separator = "-------"
    for line in range(getVerticalBoxes(grid)):
        print("   "+separator*(getHorizontalBoxes(grid)*3),"\n")
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
        print("   "+separator*(getHorizontalBoxes(grid)*3),"\n")
        lineIndex += 1

def generateNextGen(grid):
    """ Genere une nouvelle grille étant celle de la prochaine génération en respectant les 3 conditions de remplacement des éléments.
    Param : (list) grid : La grille servant pour generer la prochaine génération.
    Contrainte : (list) grid : La grille ne doit pas etre vide.
    Return : (list) Grille de la nouvelle génération.
    """
    newGrid = deepcopy(grid) # Copie de la grille sans garder la meme reference memoire.
    voisins = 0
    for line in range(getVerticalBoxes(grid)):
        for column in range(getHorizontalBoxes(grid)):
            voisins = getBoxNeighboursAlive(grid,line,column)
            if(voisins == 3): # Si elle a trois voisines vivantes, elle devient vivante
                newGrid[line][column] = 1
            elif(voisins < 2 or voisins > 3): # Si elle a moins de 2 voisines vivantes ou plus de 3, elle meurt
                newGrid[line][column] = 0
            # Sinon elle ne change pas
    return newGrid

def gridEvolution(grid,n):
    """ Génère des grilles pour les n prochaines générations.
    Param : (list) grid : La grille servant pour generer les générations.
            (int)  n    : Le nombre de générations suivante à générer.
    Contrainte : (list) grid : La grille ne doit pas etre vide.
    Return : (list) Grille de la nouvelle génération.
    """
    print("Grille initiale\n",displayGrid(grid))
    newGrid = deepcopy(grid)
    sleep(1)
    for i in range(n):
        newGrid = generateNextGen(newGrid)
        print("Génération n°",i+1,"\n",displayGrid(newGrid))
        sleep(1)

def main():
    print("-------------------------")
    print("----- Jeu de la vie -----")
    print("-------------------------")
    print("Le jeu de la vie est une modélisation simpliste de la vie de cellules dans l’espace.")
    lines = int(input("Entrez un entier, servant de nombre de lignes : "))
    columns = int(input("Entrez un entier, servant de nombre de colonnes : "))
    chance = float(input("Entrez un flotant (0-1), servant du taux de probabilité de présence d'une céllule : "))
    generations = int(input("Entrez un entier, servant de nombre de générations : "))
    grid = generateGrid(lines,columns,chance)
    gridEvolution(grid,generations)

def scenario():
    # Creation de la grille & affichage non formaté
    print("Creation de la grille & affichage non formaté")
    grille = generateGrid(5,5,0.5)
    print(grille)
    sleep(5)
    # Affichage de la grille
    print("Affichage de la grille")
    displayGrid(grille)
    sleep(5)
    # Affichage formaté de la grille
    print("Affichage formaté de la grille")
    displayGridFormat(grille)
    sleep(5)
    # Affichage formaté du nombre de voisins en vie pour chaque elements de la grille
    print("Affichage formaté du nombre de voisins en vie pour chaque elements de la grille")
    displayNeighboursAliveGrid(grille)
    sleep(5)
    # Affichage de la grille, ses voisins, la prochaine grille.
    print("Affichage de la grille, ses voisins, la prochaine grille.")
    displayGridChecker(grille)
    sleep(5)
    # Affichage de la prochaine génération de la grille.
    print("Affichage de la prochaine génération de la grille.")
    generateNextGen(grille)
    sleep(5)
    # Affichage des 5 prochaines générations de la grille.
    print("Affichage des 5 prochaines générations de la grille.")
    gridEvolution(grille,5)
    sleep(3)
    print("Scénario terminé ! Merci :)")