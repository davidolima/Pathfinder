import pygame as pg
import time as t
import math

def search(node):
    global shortestPath
    global neighbourDistances
    n = node.getNeighbours()
    if n[0].getState() != 'Blank' and n[1].getState() != 'Blank' and n[2].getState() != 'Blank' and n[3].getState() != 'Blank':
        t.sleep(5)
        pass
   
    elif node.getState() == 'End':
        print("End found!")
        return int(shortestPath)

    elif node.getState() == 'Wall' or\
        node.getState() == 'fixedWall' or\
        node.getState() == 'Visited':
        pass
    
    else:
        neighbourDistances = {}
        shortestPath = math.inf
        for neighbour in node.getNeighbours():
            neighbour.setDistance(node.getDistance()+1)
            node.setState('Visited')

            if neighbour.getDistance() < shortestPath:
                neighbourDistances[neighbour.getDistance()] = neighbour
                shortestPath = neighbour.getDistance()
        
        for neighbour in node.getNeighbours():
            if neighbour.getDistance() == node.getDistance()+1:
                pg.display.update()
                search(neighbour)
                t.sleep(0.10)

        pg.display.update()
