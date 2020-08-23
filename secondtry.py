import pygame as pg
from pygame import *
import time

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

def onMousePress():
    pos = pg.mouse.get_pos()
    print(pos)
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
    generateGrid()
    startingPosition = (0,0)

    unvisited = []
    startExists = False
    endExists = False
    running = True

    while running:
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            elif event.type == pg.KEYDOWN:
                if event.type == pg.MOUSEBUTTONDOWN:
                    onMousePress()
                
                elif pg.key.name(event.key) == 'escape':
                    running = False



if __name__ == "__main__":
    Main()
    pg.display.update()