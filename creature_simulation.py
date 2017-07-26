global CARNIVORE_FEED
global HERBIVORE_FEED
global PLANT_FEED
CARNIVORE_FEED = [[], []]
HERBIVORE_FEED = [[], []]
PLANT_FEED = [[], []]

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from random import random

def read_feed(label):
    global CARNIVORE_FEED
    global HERBIVORE_FEED
    global PLANT_FEED
    plt.plot(PLANT_FEED[0], PLANT_FEED[1], "o")
    plt.plot(HERBIVORE_FEED[0], HERBIVORE_FEED[1], "o")
    plt.plot(CARNIVORE_FEED[0], CARNIVORE_FEED[1], "o")
    CARNIVORE_FEED = [[],[]]
    HERBIVORE_FEED = [[],[]]
    PLANT_FEED = [[],[]]
    print('gen ', label)
    plt.savefig("GENS/generation"+str(label)+".png")
    plt.close()

class Grid:
    def __init__(self, dim):
        self.x = dim[0]
        self.y = dim[1]
    def populate(self, pieces):
        self.pieces = pieces
    def placeCounters(self):
        for piece in pieces:
            Counter(piece, self)
    def playTurn(self):
        self.makeGrid()
        self.movePhase()
        self.placeCounters()
    def movePhase(self):
        for piece in self.pieces:
            piece.move()
    def makeGrid(self):
        grid = []
        for X in range(self.x):
            row = []
            for Y in range(self.y):
                row.append([])
            grid.append(row)
        self.grid = grid
    def isFilled(self, xcoor, ycoor):
        return type(self.grid[xcoor][ycoor]) == GridObject
    def match(self, p1, p2coor):
        p2 = self.grid[p2coor[0]][p2coor[1]]
        if type(p1) == type(p2):
            del p1
            del p2
        elif type(p1.face) == Herbivore and type(p2.face) == Carnivore:
            p1.face.die()
        elif type(p1.face) == Carnivore and type(p2.face) == Herbivore:
            p2.face.die()
        elif type(p1.face) == Plant and type(p2) == Herbivore:
            p1.face.die()
        elif type(p1) == Herbivore and type(p2) == Plant:
            p2.face.die()
    def game(self, length):
        for turn in range(length):
            self.playTurn()
            read_feed(turn)

def InitializeMatrix():
    return [[random() for x in range(100)] for y in range(100)]

class GridObject:
    def __init__(self, x, y):
        self.ycoor = y
        self.xcoor = x
    def makeCounter(self, grid):
        return Counter(self, grid)
class Creature(GridObject):
    def __init__(self, x, y, jump, matrix):
        GridObject.__init__(self, x, y)
        self.jump = jump
        self.map = matrix
    def move(self):
        points = []
        ratings = []
        try:
            ratings.append(self.map[self.xcoor + self.jump][self.ycoor])
            points.append([self.xcoor+self.jump, self.ycoor])
        except:
            pass
        try:
            ratings.append(self.map[self.xcoor - self.jump][self.ycoor])
            points.append([self.xcoor-self.jump, self.ycoor])
        except:
            pass
        try:
            ratings.append(self.map[self.xcoor][self.ycoor + self.jump])
            points.append([self.xcoor, self.ycoor+self.jump])
        except:
            pass
        try:
            ratings.append(self.map[self.xcoor][self.ycoor - self.jump])
            points.append([self.xcoor, self.ycoor-self.jump])
        except:
            pass
        x = self.xcoor; y = self.ycoor
        self.xcoor, self.ycoor = points[ratings.index(max(ratings))]
        
class Plant(GridObject):
    def __init__(self, x, y):
        GridObject.__init__(self, x,y)
    def move(self):
        global PLANT_FEED
        PLANT_FEED[0].append(self.xcoor)
        PLANT_FEED[1].append(self.ycoor)
    def die(self):
        print("DEATH OF PLANT AT ("+self.xcoor+", "+self.ycoor+")")
        del self

class Carnivore(Creature):
    def __init__(self, x, y, jump, matrix):
        Creature.__init__(self, x, y, jump, matrix)
    def move(self):
        Creature.move(self)
        global CARNIVORE_FEED
        CARNIVORE_FEED[0].append(self.xcoor)
        CARNIVORE_FEED[1].append(self.ycoor)
    def die(self):
        print("DEATH OF PREDATOR AT ({}, {})".format(self.xcoor, self.ycoor))
        del self

class Herbivore(Creature):
    def __init__(self, x, y, jump, matrix):
        Creature.__init__(self, x, y, jump, matrix)
    def move(self):
        Creature.move(self)
        global HERBIVORE_FEED
        HERBIVORE_FEED[0].append(self.xcoor)
        HERBIVORE_FEED[1].append(self.ycoor)
    def die(self):
        print("DEATH OF PREDATOR AT ({}, {})".format(self.xcoor, self.ycoor))

class Counter(GridObject):
    def __init__(self, item, grid):
        GridObject.__init__(self, item.xcoor, item.ycoor)
        self.face = item
        self.grid = grid
        self.place()
    def place(self):
        if self.grid.isFilled(self.ycoor, self.xcoor):
            self.grid.match(self, [self.xcoor, self.ycoor])
        self.grid.grid[self.xcoor][self.ycoor] = self

if __name__ == "__main__":
    grid = Grid((100, 100))
    plants = [Plant(int(random()*100), int(random() *100)) for i in range(50*50)]
    herbivores = [Herbivore(int(random()*100), int(random() *100), int(random()*10), InitializeMatrix()) for i in range(25*25)]
    carnivores = [Carnivore(int(random()*100), int(random() *100), int(random()*10), InitializeMatrix()) for i in range(12*12)]
    pieces = plants + herbivores + carnivores
    grid.populate(pieces)
    grid.game(1000)
