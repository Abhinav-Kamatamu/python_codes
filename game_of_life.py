import math
import sys
import pygame
from pygame.locals import *

pygame.init()

width = 800
height = 800

black = (255, 255, 255)
white = (0, 0, 0)

window = pygame.display.set_mode((width, height))
window.fill(white)
pygame.display.set_caption("Initizialing...")

clock = pygame.time.Clock()

restart = False
drawMode = True

Cells = []


def DrawDivisions():
    global height, width

    numberOfLinesDrawn = 0
    numberOfLinesRequired = 98

    currentX = 16

    while numberOfLinesDrawn <= numberOfLinesRequired:
        pygame.draw.line(window, black, (currentX, 0), (currentX, height))

        currentX += 16
        numberOfLinesDrawn += 1

    numberOfLinesDrawn = 0

    currentY = 16

    while numberOfLinesDrawn <= numberOfLinesRequired:
        pygame.draw.line(window, black, (0, currentY), (height, currentY))

        currentY += 16
        numberOfLinesDrawn += 1


class Coordinate():

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def Position(self):
        return (self.x, self.y)


class Cell():

    def __init__(self, x, y):

        self.neighbours = []
        self.position = Coordinate(x, y)
        self.alive = False
        self.tempAlive = False

    def UpdateCell(self):

        if (self.alive):

            color = black

        else:

            color = white

        pygame.draw.rect(window, color, (self.position.x, self.position.y, 16, 16))


def CreateCells():
    global width, height, Cells

    maximumNumberOfCells = 50 ** 2
    numberOfCellsCreated = 0

    currentX = 0
    currentY = 0

    while numberOfCellsCreated < maximumNumberOfCells:

        if (currentX > (width - 16)):
            currentY += 16
            currentX = 0

        currentCell = Cell(currentX, currentY)

        Cells.append(currentCell)

        currentX += 16
        numberOfCellsCreated += 1


def UpdateCells():
    global Cells

    numberOfCellsUpdated = 0

    while numberOfCellsUpdated < len(Cells):
        Cells[numberOfCellsUpdated].UpdateCell()

        numberOfCellsUpdated += 1


def DefineNeighbours():
    global Cells;

    i = 0

    while i < len(Cells):

        j = 0

        while j < len(Cells):

            if (i != j):

                if (abs(Cells[i].position.x - Cells[j].position.x) <= 16 and abs(
                        Cells[i].position.y - Cells[j].position.y) <= 16):
                    Cells[i].neighbours.append(Cells[j])

            j += 1

        i += 1


def Draw():
    global Cells, drawMode

    if pygame.mouse.get_pressed()[0]:

        mousePos = pygame.mouse.get_pos()

        i = 0

        while i < len(Cells):

            if Cells[i].position.x < mousePos[0] and (Cells[i].position.x + 16) > mousePos[0]:
                if Cells[i].position.y < mousePos[1] and (Cells[i].position.y + 16) > mousePos[1]:
                    Cells[i].alive = True

            i += 1

    UpdateCells()

    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if pygame.mouse.get_pressed()[2]:
            drawMode = False


def Simulate():
    global clock, Cells

    clock.tick(10)

    i = 0

    while i < len(Cells):

        numberOfAliveCells = 0
        j = 0

        while j < len(Cells[i].neighbours):

            if Cells[i].neighbours[j].alive:
                numberOfAliveCells += 1

            j += 1

        if Cells[i].alive:

            if 2 <= numberOfAliveCells <= 3:

                Cells[i].tempAlive = True

            else:

                Cells[i].tempAlive = False

        elif not Cells[i].alive:

            if numberOfAliveCells == 3:

                Cells[i].tempAlive = True

            else:

                Cells[i].tempAlive = False

        i += 1

    i = 0

    while i < len(Cells):
        Cells[i].alive = Cells[i].tempAlive

        i += 1

    UpdateCells()
    pygame.display.update()

    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()


CreateCells()
DefineNeighbours()
pygame.display.set_caption("John Conway's Game Of Life[Draw your pattern][Right Click to Proceed after Drawing]")

while not restart:

    UpdateCells()
    DrawDivisions()

    while drawMode:
        Draw()
        DrawDivisions()

        pygame.display.update()

    while not drawMode:
        pygame.display.set_caption("John Conway's Game Of Life")
        Simulate()

    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
