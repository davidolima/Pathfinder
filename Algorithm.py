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
            # for n in node.getNeighbours():
                # n.setDistance(node.getDistance()+1)

            node.setState('Visited')
            return False

    for n in node.getNeighbours():
        n.setDistance(node.getDistance()+1)
        if n.getState() == 'Blank':
            node.setState('currentNode')
            n.setState('Tentativa')
            pg.display.update()
            # t.sleep(0.05)


            # if n.getDistance() < shortestPath:
            #         neighbourDistances[n.getDistance()] = n
            #         shortestPath = n.getDistance()
                    
            if n.getDistance() == node.getDistance()+1:
                node.setState('Visited')
                pg.display.update()
            # node.setState('Visited')
            # pg.display.update()
            return False
        
        elif n.getState() == 'End':
            print("End found!")
            print(n.getDistance())
            return True

        elif n.getState() == 'Visited' or n.getState() == 'Tentativa':
            pass

        elif n.getState() == 'Wall' or\
            n.getState() == 'fixedWall':
            return False

