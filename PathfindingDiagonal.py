'''
Feito por David de Oliveira Lima //
Made by David de Oliveira Lima

Entre o período de // Between the period of
              2020 - 2021
'''

import pygame as pg
import time as t
import random
import json
from pygame import *
import tkinter as tk
from tkinter import filedialog


class Node:
    def __init__(self, parent, index, distance, x, y, grid_pos, state):
        self.x = x
        self.y = y
        self.grid_pos = grid_pos
        self.state = state
        self.index = index
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
            startExists = True

        elif self.state == 'Fim':
            pg.draw.rect(screen, (200, 0, 0), Rect(
                self.x, self.y, gridSize, gridSize))
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
        top_left = grid[self.grid_pos[0]-1, self.grid_pos[1]-1]
        top = grid[self.grid_pos[0], self.grid_pos[1]-1]
        top_right = grid[self.grid_pos[0]+1, self.grid_pos[1]-1]
        right = grid[self.grid_pos[0]+1, self.grid_pos[1]]
        bot_right = grid[self.grid_pos[0]+1, self.grid_pos[1]+1]
        bottom = grid[self.grid_pos[0], self.grid_pos[1]+1]
        bot_left = grid[self.grid_pos[0]-1, self.grid_pos[1]+1]
        left = grid[self.grid_pos[0]-1, self.grid_pos[1]]

        return top_left, top, top_right, right, bot_right, bottom, bot_left, left

    def setDistance(self, newDistance):
        self.distance = newDistance

    def setParent(self, newParent):
        self.parent = newParent


def iniciarBusca():
    if startExists != False and endExists != False:
        global procura_futura

        searching = True
        # Lista que vai guardar os nodes a serem analizados futuramente // List that will keep track of the Nodes which are going to be tested
        procura_futura = []

        print("Iniciando Procura...")

        # Adicionar os Nodes ao redor do ponto inicial para a lista de tentativa futura // Add the nodes around the starting point to the procura_futura(future_search) list
        for node in grid[startingPosition].getNeighbours():
            if node.state == 'Vazio':                                       # Se o node for vazio // If node is blank
                # Mudar seu estado para "Tentativa" // Change it's state to "Try"
                node.setState('Tentativa')
                # Colocar o node inicial como parente deste vizinho // Set the starting node as this neighbour's parent.
                node.setParent(grid[startingPosition])
                # Colocar a distância do vizinho como 1 // Set the neighbour distance to 1
                node.setDistance(1)
                # Colocar o node vizinho na lista de tentativa futura // Append the neighbouring node to the procura_futura list
                procura_futura.append(node)
            # Atualizar tela // Update display.
            pg.display.update()

        while searching:
            # Nodes que serão procurados nessa recursão são pegos de procura_futura // Nodes which are going to be tested in this recursion are taken from procura_futura
            procura_atual = procura_futura.copy()
            # procura_futura é limpada para que possamos adicionar os nodes da proxima recursão // procura_futura is cleared so that we can add the nodes which are going to be tested in the next recursion
            procura_futura.clear()
            # Para cada node em procura_atual // For each node in procura_atual (current_search)
            for node in procura_atual:
                # Para cada vizinho deste node em procura_atual // For each neighbour of these nodes in procura_atual
                for node_vizinho in node.getNeighbours():
                    # Se o estado do vizinho for vazio // If the neighbour's state is blank
                    if node_vizinho.state == 'Vazio':
                        # Colocar o node atual como parente do vizinho // Set the neighbour's parent as the current node
                        node_vizinho.setParent(node)
                        # Mudar o estado do vizinho para "Tentativa" // Change the neighbour's state to "Try"
                        node_vizinho.setState('Tentativa')
                        # Colocar a distância do vizinho como a distância do node atual + 1 // Set the neighbour distance to the current node's distance + 1
                        node_vizinho.setDistance(node.distance + 1)
                        # Colocar o vizinho na lista de tentativa futura // Append the neighbouring node to the "future search" list
                        procura_futura.append(node_vizinho)
                        # Colocar o estado do node atual como "visitado" // Set the current node's state to "Visitado"("Visited")
                        node.setState('Visitado')
                        # Atualizar tela // Update display.
                        pg.display.update()

                    # Se o Node vizinho tiver o estado igual a "Fim" // If the neighbour's state equals to "Fim"("End")
                    elif node_vizinho.state == 'Fim':
                        # Procura está completa // Search is done
                        searching = False
                        # Limpar a lista de tentativas atual // Clear the "current_search" list
                        procura_atual.clear()
                        # Colocar a distância do vizinho como a distância do node atual + 1 // Set the neighbour distance to the current node's distance + 1
                        node_vizinho.setDistance(node.distance + 1)
                        # Colocar o node atual como parente do vizinho // Set the neighbour's parent as the current node
                        node_vizinho.setParent(node)
                        # Imprimir na tela a localização e a distância do ponto final // Print the location and the distance of the End Node
                        print(node_vizinho.grid_pos, node_vizinho.distance)
                        # Gerar caminho ente o ponto final e o inicial // Generate the path between the End point and the Starting point
                        generatePath(node_vizinho)

                    else:
                        continue

                pg.display.update()


# Gerar caminho ente o ponto final e o inicial // Generate the path between the End point and the Starting point
def generatePath(node):
    # Criar variável "parente" // Create "parente"("parent") variable
    parent = node.parent

    # Para i vezes a distância entre o ponto final e o inicial // for i times the distance between the starting and end point
    for i in range(node.distance):
        # Se o parente é diferente de None // If parent is different than None
        if parent != None:
            # Mudar o estado do parente para "Path"("Caminho") // Change parent's state to "Path"
            parent.setState('Path')
            # Atualizar tela // Update display
            pg.display.update()
            # Parente é igual ao parente do parente do node atual // Parent now equals the parent of the parent of the current node
            parent = parent.parent
        # Esperar 0.005 segundo para vermos o caminho ser feito // Wait 0.005 so we can see the path being made
        t.sleep(0.005)
        # Se o estado do parente é "Comeco" // If the parent's state is "Comeco" ("Start")
        if parent.state == 'Comeco':
            break                                                       # Terminar // Finish


def generateObstacles():
    for i in range(50):
        randXY = (random.randrange(1, 63), random.randrange(1, 35))
        if startExists == True and endExists == True and grid[randXY].state == "Vazio":
            grid[randXY].setState("Muro")
        pg.display.update()


def generateGrid():
    global grid
    global gridlist
    global gridSize
    gridSize = 20
    grid = {}
    gridlist = []
    gdpos = 0

    rct = pg.draw.rect(screen, (0, 0, 0), Rect(0, 0, 1280, 720))
    font = pg.font.Font('freesansbold.ttf', 50)
    txt = font.render('Gerando grade...', True, (0, 255, 0))
    screen.blit(txt, (((pg.display.get_window_size()[0]//2) - (txt.get_width()/2)), (
        pg.display.get_window_size()[1]//2) - (txt.get_height()/2)))  # Centralizar Texto
    pg.display.update()

    for x in range(1280//gridSize):
        for y in range(720//gridSize):
            # Draw Walls on edges
            if x == 0 or x == 63 or y == 0 or y == 35:
                newNode = Node(None, gdpos, float('inf'), x *
                               gridSize, y*gridSize, (x, y), "muroFixo")
                gridlist.append(newNode)
                grid[newNode.grid_pos] = newNode
                gdpos += 1

            else:
                newNode = Node(None, gdpos, float('inf'), x *
                               gridSize, y*gridSize, (x, y), "Vazio")
                gridlist.append(newNode)
                grid[newNode.grid_pos] = newNode
                gdpos += 1


def onMousePress(button):
    pos = pg.mouse.get_pos()
    for item in gridlist:
        if item.x < pos[0] < (item.x+20) and item.y < pos[1] < (item.y+20):
            if startExists == False and endExists == False and item.state == "Vazio" and button == 'm1':
                global startIndex
                item.setState("Comeco")
                startIndex = item.index
                print('Comeco at:', pos)

            elif startExists == True and endExists == False and item.state == "Vazio" and button == 'm1':
                item.setState("Fim")
                print('Fim at:', pos)

            elif startExists == endExists == True and item.state == "Muro" and button == 'm2':
                item.setState("Vazio")

            elif startExists == endExists == True and item.state == "Vazio" and button == 'm1':
                item.setState("Muro")


def update():
    global running
    while running:
        pg.display.update()
        if startExists == False:
            pg.display.set_caption("Adicionar ponto de partida")

        elif endExists == False:
            pg.display.set_caption("adicionar ponto a ser procurado")

        elif startExists == True and endExists == True:
            pg.display.set_caption(
                "Desenhe muros e/ou pressione enter para começar")

        # elif searching == True:
        #     pg.display.set_caption("Procurando pelo ponto...")

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            elif pg.mouse.get_pressed()[0]:
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
                elif pg.key.name(event.key) == 'l':
                    root = tk.Tk()
                    root.withdraw()
                    try:
                        mapFile = filedialog.asksaveasfile(
                            filetypes=[('Json Files', '*.json')], defaultextension=[('Json Files', '*.json')])
                        info = {}
                        for i in gridlist:
                            if str(i.state) != 'Vazio' and str(i.state) != 'muroFixo':
                                info[str(i.grid_pos)] = str(i.state)
                        info = json.dumps(info, indent=4)
                        mapFile.pg.display.set_caption(info)
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


def Main():
    global startExists
    global endExists
    global running
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

    generateGrid()
    pg.display.update()


if __name__ == '__main__':
    Main()
    update()
    pg.quit()
