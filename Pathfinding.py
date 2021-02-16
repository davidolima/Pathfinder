import pygame as pg
import time as t
import math, random, json
from pygame import *
import tkinter as tk
from tkinter import filedialog

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
        global startingPosition
        global startExists
        global endExists

        self.state = newState

        if self.state == 'Start':

            unvisited.remove(self)
            startingPosition = self.gridpos
            self.distance = 0
            rct = pg.draw.rect(screen,(0,200,0),Rect(self.x,self.y, gridSize,gridSize))
            font  = pg.font.Font('freesansbold.ttf',8)
            txt = font.render('Start',True, (0, 0, 0))
            screen.blit(txt, rct)
            startExists = True

        elif self.state == 'End':
            pg.draw.rect(screen,(200,0,0),Rect(self.x,self.y, gridSize,gridSize))
            endExists = True

        elif self.state == 'Blank':
            pg.draw.rect(screen,(200,200,200),Rect(self.x,self.y, gridSize,gridSize))
            pg.draw.rect(screen,(0,0,0),Rect(self.x,self.y, gridSize,gridSize),1)
            unvisited.append(self) # Todos os Nodes 'Blank' são marcados como não visitados

        elif self.state == 'Visited':
            try:
                rct = pg.draw.rect(screen,(50+self.getDistance(), 10, 200),Rect(self.x,self.y, gridSize,gridSize))
            except:
                rct = pg.draw.rect(screen,(255,10,200),Rect(self.x,self.y, gridSize,gridSize))
            font  = pg.font.Font('freesansbold.ttf',10)
            txt = font.render(str(self.getDistance()),True, (0, 255, 0))
            screen.blit(txt, rct)

        elif self.state == 'Wall':
            pg.draw.rect(screen,(150,150,150),Rect(self.x,self.y, gridSize,gridSize))
        
        elif self.state == 'fixedWall':
            pg.draw.rect(screen,(30,15,15),Rect(self.x,self.y, gridSize,gridSize))

        elif self.state == 'currentNode':
            rct = pg.draw.rect(screen,(255,0,255),Rect(self.x,self.y, gridSize,gridSize))

        elif self.state == 'Tentativa':
            rct = pg.draw.rect(screen,(204,102,0),Rect(self.x,self.y, gridSize,gridSize))

        elif self.state == 'Path':
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

def write(txt):
    pg.display.set_caption(txt)

def initiate():
    if startExists == False:
        pass
    elif endExists == False:
        pass
    else:
        global shortestPath
        print("Iniciando Procura...")

        for n in grid[startingPosition].getNeighbours():
            if n.getState() == 'Blank':
                n.setState('Tentativa')
                n.setParent(grid[startingPosition])
                n.setDistance(1)
            pg.display.update()

        searching = True
        shortestPath = 999
        while searching == True:
            for item in grid:
                if grid[item].getState() == 'Tentativa' and grid[item].getDistance() != float('inf'):
                    if search(grid[item]) == False:
                        for n in grid[item].getNeighbours():
                            if n.getState() == 'Blank':
                                n.setDistance(grid[item].getDistance()+1)
                                n.setParent(grid[item])
                                n.setState('Tentativa')
                                pg.display.update()


                            elif n.getState() == 'End':
                                n.setDistance(grid[item].getDistance()+1)
                                n.setParent(grid[item])
                                search(n)
                                print(n.getDistance(), shortestPath)
                                if n.getDistance() < shortestPath:
                                    print('Short distance updated(',shortestPath,'->',n.getDistance(),')')
                                    shortestPath = n.getDistance()
                                    caminho(n)
                                    searching = False
                                    break
                if not searching:
                    break

def search(node):
    global neighbourDistances
    n = node.getNeighbours()
    neighbourDistances = {}

    if n[0].getState() != 'Blank' and n[1].getState() != 'Blank' and n[2].getState() != 'Blank' and n[3].getState() != 'Blank':
        node.setState('Visited')
        return False

    elif node.getState() == 'End':
        return node.getNeighbours()

    else:
        for n in node.getNeighbours():
            n.setDistance(node.getDistance()+1)
            if n.getState() == 'Blank':
                node.setState('currentNode')
                n.setParent(node)
                n.setState('Tentativa')
                        
                if n.getDistance() == node.getDistance()+1:
                    node.setState('Visited')

                return False
            
            elif n.getState() == 'End':
                pg.display.update()
                n.setParent(node)
                print("End found!")
                print(n.getDistance())
                return False

            elif n.getState() == 'Visited' or n.getState() == 'Tentativa':
                pass

            elif n.getState() == 'Wall' or\
                n.getState() == 'fixedWall':
                return False


def caminho(node):
        parent = node.getParent()
        for item in grid:
            if grid[item].getState() == 'Path':
                grid[item].setState('Blank')

        for i in range(node.getDistance()):
            if parent != None:
                parent.setState('Path')
                pg.display.update()
                parent = parent.getParent()
            t.sleep(0.005)
            if parent.getState() == 'Start':
                break

def generateObstacles():
    for i in range(50):
        randXY = (random.randrange(1,63),random.randrange(1,35))
        if startExists == True and endExists == True and grid[randXY].state == "Blank":
            grid[randXY].setState("Wall")
        pg.display.update()

def generateGrid():
    global grid
    global gridlist
    global gridSize
    gridSize = 20
    grid = {}
    gridlist = []
    gdpos = 0

    rct = pg.draw.rect(screen,(0,0,0),Rect(0,0, 1280,720))
    font  = pg.font.Font('freesansbold.ttf',50)
    txt = font.render('Gerando grade...',True, (0, 255, 0))
    screen.blit(txt, rct)
    pg.display.update()

    for x in range(1280//gridSize):
        for y in range (720//gridSize):
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


def onMousePress(button):
    pos = pg.mouse.get_pos()
    for item in gridlist:
        if item.getX() < pos[0] < (item.getX()+20) and item.getY() < pos[1] < (item.getY()+20):
            if startExists == False and endExists == False and item.state == "Blank" and button == 'm1':
                global startIndex
                item.setState("Start")
                startIndex = item.getIndex()
                print('Start at:', pos)

            elif startExists == True and endExists == False and item.state == "Blank" and button == 'm1':
                item.setState("End")
                print('End at:', pos)

            elif startExists == endExists == True and item.state == "Wall" and button == 'm2':
                item.setState("Blank")

            elif startExists == endExists == True and item.state == "Blank" and button == 'm1':
                item.setState("Wall")
                print('Wall at:', pos)

def update():
    global running
    while running:
        pg.display.update()
        if startExists == False:
            write("Adicionar ponto de partida")

        elif endExists == False:
            write("adicionar ponto a ser procurado")

        elif startExists == True and endExists == True:
            write("Desenhe muros e/ou pressione enter para começar")
        
        elif searching == True:
            write("Procurando pelo ponto...")

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            elif pg.mouse.get_pressed()[0]:
                onMousePress('m1')
            elif pg.mouse.get_pressed()[2]:
                onMousePress('m2')

            elif event.type == pg.KEYDOWN:
                if pg.key.name(event.key) == 'return':
                    initiate()
                elif pg.key.name(event.key) == 'backspace':
                    generateObstacles()
                elif pg.key.name(event.key) == 'escape':
                    running = False
                elif pg.key.name(event.key) == 'r':
                    Main()
                elif pg.key.name(event.key) == 'l':
                    root = tk.Tk()
                    root.withdraw()
                    try:
                        mapFile = filedialog.asksaveasfile(filetypes=[('Json Files', '*.json')], defaultextension=[('Json Files', '*.json')])
                        info = {}
                        for i in gridlist:
                            if str(i.getState()) != 'Blank' and str(i.getState()) != 'fixedWall':
                                info[str(i.getGridpos())] = str(i.getState())
                        info = json.dumps(info, indent=4)
                        mapFile.write(info)
                        mapFile.close()
                    except Exception as e:
                        print(e)
                        pass
                elif pg.key.name(event.key) == 'o':
                    root = tk.Tk()
                    root.withdraw()
                    try:
                        mapFile = filedialog.askopenfile()
                        mapFile = json.load(mapFile)
                        Main()
                        for i in mapFile:
                            for c in i:
                                x = int(i[i.index('(')+1:i.index(',')])
                                y = int(i[i.index(' ')+1:i.rindex(')')])
                            grid[(x,y)].setState(mapFile[i])

                    except Exception as e:
                        print(e)
                        pass
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

if __name__ == '__main__':
    Main()
    update()
    pg.quit()