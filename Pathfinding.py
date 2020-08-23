import pygame as pg
import sys
import time as t
import random
import Algorithm
import functools
from pygame import *

sys.setrecursionlimit(4000)

class Node:
    def __init__(self,index,distance, x,y,gridpos,state):
        self.x = x
        self.y = y
        self.gridpos = gridpos
        self.state = state
        self.index = index
        self.distance = distance

        if self.state == 'Blank':
            pg.draw.rect(screen,(0,0,0),Rect(self.x,self.y, gridSize,gridSize),1) 
        
        elif self.state == 'fixedWall':
            rct = pg.draw.rect(screen,(30,15,15),Rect(self.x,self.y, gridSize,gridSize))
            font  = pg.font.Font('freesansbold.ttf',8)
            txt = font.render(str(self.getGridpos()),True, (0, 255, 255),(30,15,15))
            screen.blit(txt, rct)

    def setState(self,newState):
        self.state = newState
        if self.state == 'Start':
            global startingPosition
            global startExists

            # grid[self.gridpos[0],self.gridpos[1]].setState('Start')
            startingPosition = self.gridpos
            self.distance = 0
            rct = pg.draw.rect(screen,(0,200,0),Rect(self.x,self.y, gridSize,gridSize))
            font  = pg.font.Font('freesansbold.ttf',8)
            txt = font.render('Start',True, (0, 0, 0))
            screen.blit(txt, rct)
            startExists = True
            visited.append(self)

        if self.state == 'End':
            global endExists
            # grid[self.gridpos[0],self.gridpos[1]].setState('End')
            pg.draw.rect(screen,(200,0,0),Rect(self.x,self.y, gridSize,gridSize))
            endExists = True

        if self.state == 'Blank':
            # grid[self.gridpos[0],self.gridpos[1]].setState('Blank')
            pg.draw.rect(screen,(0,0,0),Rect(self.x,self.y, gridSize,gridSize),1)

        if self.state == 'Visited':
            rct = pg.draw.rect(screen,(1.5*self.getDistance(),0,200-(1.5*self.getDistance())),Rect(self.x,self.y, gridSize,gridSize))
            # rct = pg.draw.rect(screen,(0,0,200),Rect(self.x,self.y, gridSize,gridSize))
            font  = pg.font.Font('freesansbold.ttf',10)
            txt = font.render(str(self.getDistance()),True, (0, 255, 0))
            screen.blit(txt, rct)
            visited.append(self)
        

        if self.state == 'Wall':
            # grid[self.gridpos[0],self.gridpos[1]].setState('Wall')
            pg.draw.rect(screen,(150,150,150),Rect(self.x,self.y, gridSize,gridSize))
        
        if self.state == 'fixedWall':
            pg.draw.rect(screen,(30,15,15),Rect(self.x,self.y, gridSize,gridSize))

        if self.state == 'currentNode':
            rct = pg.draw.rect(screen,(255,0,255),Rect(self.x,self.y, gridSize,gridSize))

        if self.state == 'Tentativa':
            rct = pg.draw.rect(screen,(204,102,0),Rect(self.x,self.y, gridSize,gridSize))

        if self.state == 'Path':
            rct = pg.draw.rect(screen,(255,255,0),Rect(self.x,self.y, gridSize,gridSize))

    def getNeighbours(self):
        up = grid[self.gridpos[0],self.gridpos[1]-1]
        down = grid[self.gridpos[0],self.gridpos[1]+1]
        left = grid[self.gridpos[0]-1,self.gridpos[1]]
        right = grid[self.gridpos[0]+1,self.gridpos[1]]
    
        return up,down,right,left

    def getIndex(self):
        return self.index

    def getState(self):
        return self.state
    
    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getGridpos(self):
        return self.gridpos

    def getDistance(self):
        return self.distance

    def setDistance(self, newDistance):
        self.distance = newDistance

def Main():
    global startExists
    global endExists
    global running
    global screen
    global startingPosition
    global visited

    screen = pg.display.set_mode((1280,720))
    pg.display.set_caption("Algoritmo de Pathfinding")
    pg.display.init()
    pg.font.init()
    screen.fill((200,200,200))
    generateGrid()
    startingPosition = (0,0)

    visited = []
    startExists = False
    endExists = False
    running = True

def update():
    global running
    while running:
        pg.display.update()
        if startExists == False:
            write("Set start point")

        elif endExists == False:
            write("Set end point ")

        elif startExists == True and endExists == True:
            write("Draw walls and/or press enter to start")
        
        elif searching == True:
            write("Searching for end point...")

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        
            elif event.type == pg.MOUSEBUTTONDOWN:
                onMousePress()

            elif event.type == pg.KEYDOWN:
                if pg.key.name(event.key) == 'return':
                    initiate()
                if pg.key.name(event.key) == 'backspace':
                    generateObstacles()
                if pg.key.name(event.key) == 'escape':
                    running = False

def write(txt):
    pg.display.set_caption(txt)

def generateGrid():
    global grid
    global gridlist
    global gridSize
    gridSize = 20
    grid = {}
    gridlist = []
    gdpos = 0
    for x in range(1280):
        for y in range (720):
            #Draw Walls on edges
            if x == 0 or x == 63 or y == 0 or y == 35:
                newNode = Node(gdpos,float('inf'),x*gridSize,y*gridSize,(x,y),"fixedWall")
                gridlist.append(newNode)
                grid[newNode.getGridpos()] = newNode
                gdpos += 1
            
            else:
                newNode = Node(gdpos,float('inf'),x*gridSize,y*gridSize,(x,y),"Blank")
                gridlist.append(newNode)
                grid[newNode.getGridpos()] = newNode
                gdpos += 1

def initiate():
    if startExists == False:
        pass
    elif endExists == False:
        pass
    else:
        print("Initiating search...")

        for n in grid[startingPosition].getNeighbours():
            if n.getState() == 'Blank':
                n.setState('Tentativa')
                n.setDistance(1)
            
            print(n.getState(), n.getDistance(), n.getGridpos())

        searching = True
        
        while searching == True:
            pg.display.update()
            for item in grid:
                path = []
                if grid[item].getState() == 'Tentativa' and grid[item].getDistance() != float('inf'):
                    if Algorithm.search(grid[item]) == False:
                        path.append(grid[item])
                        for n in grid[item].getNeighbours():
                            if n.getState() == 'Blank':
                                n.setDistance(grid[item].getDistance()+1)
                                n.setState('Tentativa')
                                pg.display.update()

                            elif n.getState() == 'End':
                                n.setDistance(grid[item].getDistance()+1)
                                while Pathfind(grid[startingPosition],grid[n.getGridpos()]) == False:
                                    Pathfind(grid[startingPosition],grid[n.getGridpos()])

        # for item in grid:
        #     # if grid[item].getDistance() != float('inf'):
        #     for itemv in visited:
        #         print(itemv.getGridpos(),itemv.getState())
        #         itemv.setState('currentNode')
        #         if Algorithm.search(itemv) == False:
        #             visited.remove(itemv)
        #             for neighbour in itemv.getNeighbours():
        #                 if neighbour.getState() == 'willTry':
        #                     visited.append(neighbour)
        #                 else:
        #                     pass
        #             pass


def Pathfind(startingNode, endingNode):

    sn = startingNode
    en = endingNode

    print('Ending X:', en.getGridpos()[0],\
          '\nEnding Y:', en.getGridpos()[1],\
          '\nStarting X:', sn.getGridpos()[0],\
          '\nStating Y:', sn.getGridpos()[1])

    for i in range(sn.getGridpos()[0],en.getGridpos()[0]):
        grid[i+1,sn.getGridpos()[1]].setState('Path')

    for i in range(sn.getGridpos()[1],en.getGridpos()[1]):
        grid[en.getGridpos()[0],i+1].setState('Path')

    for i in range(en.getGridpos()[0],sn.getGridpos()[0]):
        grid[i,sn.getGridpos()[1]].setState('Path')

    for i in range(en.getGridpos()[1],sn.getGridpos()[1]):
        grid[en.getGridpos()[0],i+1].setState('Path')



def generateObstacles():
    for i in range(50):
        randXY = (random.randrange(1,63),random.randrange(1,33))
        if startExists == True and endExists == True and grid[randXY].state == "Blank":
                grid[randXY].setState("Wall")

def onMousePress():
    pos = pg.mouse.get_pos()
    for item in gridlist:
        if item.getX() < pos[0] < (item.getX()+20) and item.getY() < pos[1] < (item.getY()+20):
            if startExists == False and endExists == False and item.state == "Blank":
                global startIndex
                item.setState("Start")
                startIndex = item.getIndex()
                print('Start at:', pos)
                print('Grid Position:', item.getGridpos())


            elif startExists == True and endExists == False and item.state == "Blank":
                item.setState("End")
                print('End at:', pos)
                print('Grid Position:', item.getGridpos())

            elif startExists == True and endExists == True and item.state == "Wall":
                item.setState("Blank")

            elif startExists == True and endExists == True and item.state == "Blank":
                item.setState("Wall")
                print('Wall at:', pos)
                print('Grid Position:', item.getGridpos())
Main()
update()
pg.quit()
