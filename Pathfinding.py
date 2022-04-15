# Djikstra Pathfinding Algorithm in Python

import random
import json
import pygame as pg
from pygame import *
import tkinter as tk
from tkinter import filedialog


class Node:
    def __init__(self, parent, distance, x, y, grid_pos, state):
        self.x = x
        self.y = y
        self.grid_pos = grid_pos
        self.state = state
        self.parent = parent
        self.distance = distance

        if self.state == 'Vazio':
            pg.draw.rect(screen, (200, 200, 200), Rect(
                self.x, self.y, gridSize, gridSize))
            pg.draw.rect(screen, (0, 0, 0), Rect(
                self.x, self.y, gridSize, gridSize), 1)

        elif self.state == 'muroFixo':
            pg.draw.rect(screen, (30, 15, 15), Rect(self.x, self.y, gridSize, gridSize))
            font = pg.font.Font('freesansbold.ttf', 8)

            if self.grid_pos[0] == 0 or self.grid_pos[0] == 63:
                txt = font.render(
                    str(self.grid_pos[1]), True, (0, 255, 255), (30, 15, 15))
            elif self.grid_pos[1] == 0 or self.grid_pos[1] == 35:
                txt = font.render(
                    str(self.grid_pos[0]), True, (0, 255, 255), (30, 15, 15))
            else:
                txt = font.render(str(self.grid_pos), True,
                                  (0, 255, 255), (30, 15, 15))

            pos = self.grid_pos[0] * 20 + 6, self.grid_pos[1]*20 + 6
            screen.blit(txt, pos)

    def setState(self, newState):
        global startingPosition
        global startExists
        global endExists

        self.state = newState

        if self.state == 'Comeco':
            startingPosition = self.grid_pos
            self.distance = 0
            rct = pg.draw.rect(screen, (0, 200, 0), Rect(
                self.x, self.y, gridSize, gridSize))
            font = pg.font.Font('freesansbold.ttf', 8)
            txt = font.render('Cmco', True, (0, 0, 0))
            screen.blit(txt, rct)
            pg.display.update()
            startExists = True

        elif self.state == 'Fim':
            pg.draw.rect(screen, (200, 0, 0), Rect(
                self.x, self.y, gridSize, gridSize))
            pg.display.update()
            endExists = True

        elif self.state == 'Vazio':
            pg.draw.rect(screen, (200, 200, 200), Rect(
                self.x, self.y, gridSize, gridSize))
            pg.draw.rect(screen, (0, 0, 0), Rect(
                self.x, self.y, gridSize, gridSize), 1)

        elif self.state == 'Visitado':
            cor = (max(min(self.distance, 255), 50), 10, 200)
            rct = pg.draw.rect(screen,
                               cor,
                               Rect(self.x, self.y, gridSize, gridSize))

            font = pg.font.Font('freesansbold.ttf', 10)
            txt = font.render(str(self.distance), True, (0, 255, 0))
            screen.blit(
                txt, (self.grid_pos[0] * 20 + 6, self.grid_pos[1]*20 + 6))

        elif self.state == 'Muro':
            pg.draw.rect(screen, (150, 150, 150), Rect(
                self.x, self.y, gridSize, gridSize))
            pg.display.update()

        elif self.state == 'muroFixo':
            pg.draw.rect(screen, (30, 15, 15), Rect(
                self.x, self.y, gridSize, gridSize))

        elif self.state == 'currentNode':
            rct = pg.draw.rect(screen, (255, 0, 255), Rect(
                self.x, self.y, gridSize, gridSize))

        elif self.state == 'Tentativa':
            rct = pg.draw.rect(screen, (204, 102, 0), Rect(
                self.x, self.y, gridSize, gridSize))

        elif self.state == 'Path':
            rct = pg.draw.rect(screen, (255, 255, 0), Rect(
                self.x, self.y, gridSize, gridSize))

    def getNeighbours(self):
        up = grid[self.grid_pos[0], self.grid_pos[1]-1]
        down = grid[self.grid_pos[0], self.grid_pos[1]+1]
        left = grid[self.grid_pos[0]-1, self.grid_pos[1]]
        right = grid[self.grid_pos[0]+1, self.grid_pos[1]]

        return up, down, right, left

def Main():
    global startExists
    global endExists
    global running
    global is_searching
    global screen
    global startingPosition

    screen = pg.display.set_mode((1280, 720))

    startingPosition = (0, 0)
    startExists = False
    endExists = False
    running = True
    is_searching = False

    icon = pg.Surface((32, 32))
    rawicon = pg.image.load('ico.ico')

    icon.set_colorkey((0, 0, 0))
    for i in range(0, 32):
        for j in range(0, 32):
            icon.set_at((i, j), rawicon.get_at((i, j)))

    pg.display.set_icon(icon)
    pg.display.set_caption(
        "Implementação do Algoritmo Dijkstra de Pathfinding em Python - David de Oliveira Lima")
    pg.display.init()
    pg.font.init()
    screen.fill((200, 200, 200))

    generateGrid()

def iniciarBusca():
    global is_searching
    global procura_futura

    if startExists and endExists:
        is_searching = True
        procura_futura = []

        print("Iniciando Procura...")

        for node in grid[startingPosition].getNeighbours():
            if node.state == 'Vazio':
                node.setState('Tentativa')
                node.parent = grid[startingPosition]
                node.distance = 1
                procura_futura.append(node)

            elif node.state == 'Fim':
                is_searching = False
                node.distance = 1
                print(node.grid_pos, node.distance)

            pg.display.update()

        while is_searching:
            procura_atual = procura_futura.copy()
            procura_futura.clear()
            for node in procura_atual:
                pg.event.pump()
                for node_vizinho in node.getNeighbours():
                    if node_vizinho.state == 'Vazio':
                        node_vizinho.parent = node
                        node_vizinho.setState('Tentativa')
                        node_vizinho.distance = node.distance + 1
                        procura_futura.append(node_vizinho)
                        node.setState('Visitado')

                    elif node_vizinho.state == 'Fim':
                        is_searching = False
                        procura_atual.clear()

                        node_vizinho.distance = node.distance + 1
                        node_vizinho.parent = node

                        print("Fim Encontrado!",
                              "\nLocalização:", node_vizinho.grid_pos,
                              "\nDistância:", node_vizinho.distance)
                        generatePath(node_vizinho)
                        limpar()

                    else:
                        node.setState('Visitado')

            pg.display.update()

            if len(procura_futura) == 0 and is_searching:
                is_searching = False
                print("Não encontrado!")
                return


def generatePath(node):
    global running
    parent = node.parent

    for i in range(node.distance):
        if parent != None:
            parent.setState('Path')
            pg.display.update()
            parent = parent.parent
        if parent.state == 'Comeco':
            return


def generateObstacles():
    for i in range(50):
        randXY = (random.randrange(1, 63), random.randrange(1, 35))
        if startExists and endExists and grid[randXY].state == "Vazio":
            grid[randXY].setState("Muro")
        pg.display.update()


def generateGrid():
    global grid
    global gridSize
    gridSize = 20
    grid = {}

    pg.draw.rect(screen, (0, 0, 0), Rect(0, 0, 1280, 720))
    font = pg.font.Font('freesansbold.ttf', 50)
    txt = font.render('Gerando grade...', True, (0, 255, 0))
    screen.blit(txt, (((pg.display.get_window_size()[
                0]//2) - (txt.get_width()/2)), (pg.display.get_window_size()[1]//2) - (txt.get_height()/2)))
    pg.display.update()

    for x in range(1280//gridSize):
        for y in range(720//gridSize):

            if x == 0 or x == 63 or y == 0 or y == 35:
                newNode = Node(None, float('inf'), x*gridSize,
                               y*gridSize, (x, y), "muroFixo")
                grid[newNode.grid_pos] = newNode

            else:
                newNode = Node(None, float('inf'), x*gridSize,
                               y*gridSize, (x, y), "Vazio")
                grid[newNode.grid_pos] = newNode
    pg.display.update()

def limpar():
    global startExists
    global endExists
    global running
    global is_searching
    global screen
    global startingPosition

    grid.clear()
    procura_futura.clear()

    startingPosition = (0, 0)
    startExists = False
    endExists = False
    is_searching = False

def reiniciar():
    limpar()
    # pg.display.init()
    screen.fill((200, 200, 200))
    generateGrid()


def onMousePress(button):
    pos = pg.mouse.get_pos()
    for item in grid.values():
        if item.x < pos[0] < (item.x+20) and item.y < pos[1] < (item.y+20):
            if not startExists and not endExists \
               and item.state == "Vazio" and button == 'm1':
                global startIndex
                item.setState("Comeco")

            elif startExists and not endExists \
                    and item.state == "Vazio" and button == 'm1':
                item.setState("Fim")

            elif startExists and endExists \
                    and item.state == "Muro" and button == 'm2':
                item.setState("Vazio")

            elif startExists and endExists \
                    and item.state == "Vazio" and button == 'm1':
                item.setState("Muro")


def update():
    global running

    while running:
        if not is_searching:
            if not startExists:
                pg.display.set_caption("Adicionar ponto de partida")

            elif not endExists:
                pg.display.set_caption("adicionar ponto a ser procurado")

            elif startExists and endExists:
                pg.display.set_caption(
                    "Desenhe muros e/ou pressione enter para começar")

        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                running = False

            elif not is_searching:
                if pg.mouse.get_pressed()[0]:
                    onMousePress('m1')
                elif pg.mouse.get_pressed()[2]:
                    onMousePress('m2')

                elif evento.type == pg.KEYDOWN:
                    if pg.key.name(evento.key) == 'return':
                        iniciarBusca()
                    elif pg.key.name(evento.key) == 'backspace':
                        generateObstacles()
                    elif pg.key.name(evento.key) == 'escape':
                        running = False
                    elif pg.key.name(evento.key) == 'r':
                        reiniciar()
                    elif pg.key.name(evento.key) == 'u':
                        pg.display.update()
                    elif pg.key.name(evento.key) == 'i':
                        root = tk.Tk()
                        root.withdraw()
                        try:
                            mapFile = filedialog.asksaveasfile(
                                filetypes=[('Json Files', '*.json')],
                                defaultextension=[('Json Files', '*.json')])
                            info = {}

                            for i in grid.values():
                                if str(i.state) != 'Vazio' and str(i.state) != 'muroFixo':
                                    info[str(i.grid_pos)] = str(i.state)

                            info = json.dumps(info, indent=4)
                            mapFile.write(info)
                            mapFile.close()

                        except Exception as e:
                            print(e)

                    elif pg.key.name(evento.key) == 'o':
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
                                grid[(x, y)].setState(mapFile[i])
                        except Exception as e:
                            print(e)


if __name__ == '__main__':
    Main()
    update()
    pg.quit()
