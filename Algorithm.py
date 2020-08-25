import pygame as pg
import time as t
import math

def search(node):
    global shortestPath
    global neighbourDistances
    n = node.getNeighbours()
    neighbourDistances = {}
    shortestPath = []

    if n[0].getState() != 'Blank' and n[1].getState() != 'Blank' and n[2].getState() != 'Blank' and n[3].getState() != 'Blank':
            node.setState('Visited')
            pg.display.update()
            return False

    for n in node.getNeighbours():
        n.setDistance(node.getDistance()+1)
        if n.getState() == 'Blank':
            node.setState('currentNode')
            n.setParent(node)
            n.setState('Tentativa')
            pg.display.update()
                    
            if n.getDistance() == node.getDistance()+1:
                node.setState('Visited')
                pg.display.update()

            return False
        
        elif n.getState() == 'End':
            pg.display.update()
            n.setParent(node)
            print("End found!")
            print(n.getGridpos())
            pg.display.update()
            return False

        elif n.getState() == 'Visited' or n.getState() == 'Tentativa':
            pg.display.update()
            pass

        elif n.getState() == 'Wall' or\
            n.getState() == 'fixedWall':
            pg.display.update()
            return False

