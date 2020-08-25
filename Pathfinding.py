import pygame as pg
import time as t
import random
import Algorithm
from pygame import *

class Node:
    def __init__(self,parent,index,distance, x,y,gridpos,state):
        self.x = x
        self.y = y
        self.gridpos = gridpos
        self.state = state
        self.index = index
        self.distance = distance
        self.parent = parent

        if self.state == 'Blank':
            pg.draw.rect(screen,(200,200,200),Rect(self.x,self.y, gridSize,gridSize))
            pg.draw.rect(screen,(0,0,0),Rect(self.x,self.y, gridSize,gridSize),1) 
            unvisited.append(self) # Todos os Nodes 'Blank' são marcados como não visitados

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

            unvisited.remove(self)
            startingPosition = self.gridpos
            self.distance = 0
            rct = pg.draw.rect(screen,(0,200,0),Rect(self.x,self.y, gridSize,gridSize))
            font  = pg.font.Font('freesansbold.ttf',8)
            txt = font.render('Start',True, (0, 0, 0))
            screen.blit(txt, rct)
            startExists = True

        if self.state == 'End':
            global endExists
            pg.draw.rect(screen,(200,0,0),Rect(self.x,self.y, gridSize,gridSize))
            endExists = True

        if self.state == 'Blank':
            pg.draw.rect(screen,(200,200,200),Rect(self.x,self.y, gridSize,gridSize))
            pg.draw.rect(screen,(0,0,0),Rect(self.x,self.y, gridSize,gridSize),1)
            unvisited.append(self) # Todos os Nodes 'Blank' são marcados como não visitados

        if self.state == 'Visited':
            rct = pg.draw.rect(screen,(1.5*self.getDistance(),0,200-(1.5*self.getDistance())),Rect(self.x,self.y, gridSize,gridSize))
            font  = pg.font.Font('freesansbold.ttf',10)
            txt = font.render(str(self.getDistance()),True, (0, 255, 0))
            screen.blit(txt, rct)
        

        if self.state == 'Wall':
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

    def getParent(self):
        return self.parent

    def setParent(self, newParent):
        self.parent = newParent

def Main():
    global startExists
    global endExists
    global running
    global screen
    global startingPosition
    global unvisited

    icon = pg.Surface((32,32))
    icon.set_colorkey((0,0,0))
    rawicon = pg.image.load('ico.ico')
    for i in range(0,32):
        for j in range(0,32):
            icon.set_at((i,j),rawicon.get_at((i,j)))
    
    pg.display.set_icon(icon)
    screen = pg.display.set_mode((1280,720))
    pg.display.set_caption("Algoritmo de Pathfinding")
    pg.display.init()
    pg.font.init()
    screen.fill((200,200,200))
    startingPosition = (0,0)

    unvisited = []
    startExists = False
    endExists = False
    running = True
    
    generateGrid()
    pg.display.update()

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
                newNode = Node(None,gdpos,float('inf'),x*gridSize,y*gridSize,(x,y),"fixedWall")
                gridlist.append(newNode)
                grid[newNode.getGridpos()] = newNode
                gdpos += 1
            
            else:
                newNode = Node(None,gdpos,float('inf'),x*gridSize,y*gridSize,(x,y),"Blank")
                gridlist.append(newNode)
                grid[newNode.getGridpos()] = newNode
                gdpos += 1


def initiate():
    if startExists == False:
        pass
    elif endExists == False:
        pass
    else:
        global shortestPath
        print("Initiating search...")

        for n in grid[startingPosition].getNeighbours():
            if n.getState() == 'Blank':
                n.setState('Tentativa')
                n.setParent(grid[startingPosition])
                n.setDistance(1)
            pg.display.update()

        searching = True
        shortestPath = 999
        while searching == True:
            pg.display.update()
            for item in grid:
                if grid[item].getState() == 'Tentativa' and grid[item].getDistance() != float('inf'):
                    if Algorithm.search(grid[item]) == False:
                        for n in grid[item].getNeighbours():
                            
                            if n.getState() == 'Blank':
                                n.setDistance(grid[item].getDistance()+1)
                                n.setParent(grid[item])
                                
                                n.setState('Tentativa')
                                pg.display.update()


                            elif n.getState() == 'End':
                                n.setDistance(grid[item].getDistance()+1)
                                n.setParent(grid[item])

                                if n.getDistance() < shortestPath:
                                    print('Short distance updated(',shortestPath,'->',n.getDistance(),')')
                                    shortestPath = n.getDistance()
                                    
                                    for item in grid:
                                        if grid[item].getState() == 'Path':
                                            grid[item].setState('Blank')

                                    Pathfind(n)


def Pathfind(node):
        parent = node.getParent()

        for i in range(node.getDistance()):
            if parent != None:
                parent.setState('Path')
                pg.display.update()
                parent = parent.getParent()



def generateObstacles():
    for i in range(50):
        randXY = (random.randrange(1,63),random.randrange(1,33))
        if startExists == True and endExists == True and grid[randXY].state == "Blank":
                grid[randXY].setState("Wall")
        pg.display.update()

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
