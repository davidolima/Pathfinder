'''
Feito por David de Oliveira Lima //
Made by David de Oliveira Lima

Entre o período de // Between the period of
              2020 - 2021
'''

import random
import json
import json
import pygame as pg
import time as t
from pygame import *
import tkinter as tk
from tkinter import filedialog


class Node:
    def __init__(self, parent, distance, x, y, grid_pos, state):
        self.x = x
        self.y = y
        self.grid_pos = grid_pos
        self.state = state
        self.distance = distance
        self.parent = parent

        if self.state == 'Vazio':
            pg.draw.rect(screen, (200, 200, 200), Rect(
                self.x, self.y, gridSize, gridSize))
            pg.draw.rect(screen, (0, 0, 0), Rect(
                self.x, self.y, gridSize, gridSize), 1)

        elif self.state == 'muroFixo':
            rct = pg.draw.rect(screen, (30, 15, 15), Rect(
                self.x, self.y, gridSize, gridSize))
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

            screen.blit(
                txt, (self.grid_pos[0] * 20 + 6, self.grid_pos[1]*20 + 6))

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
            try:
                rct = pg.draw.rect(
                    screen, (50+self.distance, 10, 200), Rect(self.x, self.y, gridSize, gridSize))
            except:
                rct = pg.draw.rect(screen, (255, 10, 200), Rect(
                    self.x, self.y, gridSize, gridSize))
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
    global searching
    global screen
    global startingPosition

    icon = pg.Surface((32, 32))
    icon.set_colorkey((0, 0, 0))
    rawicon = pg.image.load('ico.ico')
    for i in range(0, 32):
        for j in range(0, 32):
            icon.set_at((i, j), rawicon.get_at((i, j)))

    pg.display.set_icon(icon)
    screen = pg.display.set_mode((1280, 720))
    pg.display.set_caption(
        "Implementação do Algoritmo Dijkstra de Pathfinding em Python - David de Oliveira Lima")
    pg.display.init()
    pg.font.init()
    screen.fill((200, 200, 200))

    startingPosition = (0, 0)
    startExists = False
    endExists = False
    running = True
    searching = False

    generateGrid()

def iniciarBusca():
    global searching
    global procura_futura

    if startExists != False and endExists != False:
        searching = True
        procura_futura = []

        print("Iniciando Procura...")

        for node in grid[startingPosition].getNeighbours():
            if node.state == 'Vazio':
                node.setState('Tentativa')
                node.parent = grid[startingPosition]
                node.distance = 1
                procura_futura.append(node)

            elif node.state == 'Fim':
                searching = False
                node.distance = 1
                print(node.grid_pos, node.distance)

            pg.display.update()

        while searching:
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
                        searching = False
                        procura_atual.clear()
                        node_vizinho.distance = node.distance + 1
                        node_vizinho.parent = node
                        print(
                            "Fim Encontrado!",
                            "\nLocalização:", node_vizinho.grid_pos,
                            "\nDistância:", node_vizinho.distance)
                        generatePath(node_vizinho)

                    else:
                        node.setState('Visitado')

                    pg.display.update()

            if len(procura_futura) == 0 and searching == True:
                searching = False
                print("Não encontrado!")
                break


def generatePath(node):
    global running
    parent = node.parent

    for i in range(node.distance):
        if parent != None:
            parent.setState('Path')
            pg.display.update()
            parent = parent.parent
        t.sleep(0.005)
        if parent.state == 'Comeco':
            break


def generateObstacles():
    for i in range(50):
        randXY = (random.randrange(1, 63), random.randrange(1, 35))
        if startExists == True and endExists == True and grid[randXY].state == "Vazio":
            grid[randXY].setState("Muro")
        pg.display.update()


def generateGrid():
    global grid
    global gridSize
    gridSize = 20
    grid = {}

    rct = pg.draw.rect(screen, (0, 0, 0), Rect(0, 0, 1280, 720))
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


def onMousePress(button):
    pos = pg.mouse.get_pos()
    for item in grid.values():
        if item.x < pos[0] < (item.x+20) and item.y < pos[1] < (item.y+20):
            if startExists == False and endExists == False and item.state == "Vazio" and button == 'm1':
                global startIndex
                item.setState("Comeco")

            elif startExists == True and endExists == False and item.state == "Vazio" and button == 'm1':
                item.setState("Fim")

            elif startExists == endExists == True and item.state == "Muro" and button == 'm2':
                item.setState("Vazio")

            elif startExists == endExists == True and item.state == "Vazio" and button == 'm1':
                item.setState("Muro")


def update():
    global running

    while running:
        if not searching:
            if startExists == False:
                pg.display.set_caption("Adicionar ponto de partida")

            elif endExists == False:
                pg.display.set_caption("adicionar ponto a ser procurado")

            elif startExists == True and endExists == True:
                pg.display.set_caption(
                    "Desenhe muros e/ou pressione enter para começar")

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            elif not searching:
                if pg.mouse.get_pressed()[0]:
                    onMousePress('m1')
                elif pg.mouse.get_pressed()[2]:
                    onMousePress('m2')

                elif event.type == pg.KEYDOWN:
                    if pg.key.name(event.key) == 'return':
                        iniciarBusca()
                    elif pg.key.name(event.key) == 'backspace':
                        generateObstacles()
                    elif pg.key.name(event.key) == 'escape':
                        running = False
                    elif pg.key.name(event.key) == 'r':
                        Main()
                    elif pg.key.name(event.key) == 'u':
                        pg.display.update()
                    elif pg.key.name(event.key) == 'i':
                        root = tk.Tk()
                        root.withdraw()
                        try:
                            mapFile = filedialog.asksaveasfile(
                                filetypes=[('Json Files', '*.json')], defaultextension=[('Json Files', '*.json')])
                            info = {}
                            for i in grid.values():
                                if str(i.state) != 'Vazio' and str(i.state) != 'muroFixo':
                                    info[str(i.grid_pos)] = str(i.state)
                            print(info)
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
                                grid[(x, y)].setState(mapFile[i])
                        except Exception as e:
                            print(e)
                            pass


if __name__ == '__main__':
    Main()
    update()
    pg.quit()
