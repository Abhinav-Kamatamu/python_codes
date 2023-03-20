MainBrain = []

import pygame
import sys
import math
import random

pygame.init()

#'static variables---------
height = 1000
width = 800

gameFps = 144

birdSize = (85,50)
birdBlitPosition = (200, height/10)
birdCollisionTolerancy = 10

gravity = 0.2
globalBirdXVelocity = 8
globalBirdYJumpAcceleration = -7
globalBirdRotateSpeed = 15

visualGroundSpeedFactor = 0.15

groundSize = (450,80)
groundPositions = [

                     (0, height - groundSize[1]), 
                     (groundSize[0], height - groundSize[1]), 
                     (groundSize[0]*2, height - groundSize[1]),  

                    ]

backGroundSize = (576,1024)

pipeSize = (100,1265)
pipeDeadZone = 150
pipeGap = 200
pipeCount = 3
pipeDistance = 450

scoreSize = 36
scorePosition = ((width/2) - scoreSize, 50)

noOfInterNodes = 5

rad2deg = 57.2957795131
#--------------------------

#'global variables---------
groundParameter = 0
pipeParameter = width

pipes = []
#--------------------------

#'images-------------------
flappyBirdImage = pygame.image.load('flappy bird.png')
flappyBirdImage = pygame.transform.scale(flappyBirdImage, birdSize)

groundImage = pygame.image.load('ground.png')
groundImage = pygame.transform.scale(groundImage, groundSize)

backGroundImage = pygame.image.load('background.png')
backGroundImage = pygame.transform.scale(backGroundImage, backGroundSize)

topPipeImage = pygame.image.load('top pipe.png')
topPipeImage = pygame.transform.scale(topPipeImage, pipeSize)
bottomPipeImage = pygame.transform.rotate(topPipeImage, 180)

impactFont = pygame.font.SysFont("impact", scoreSize)
#--------------------------

display = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

pygame.display.set_caption("Flappy Bird")

class FlappyBird():

    def __init__(self):

        self.xPos = birdBlitPosition[0]
        self.yPos = birdBlitPosition[1]

        self.yVelocity = 0

        self.trueRotation = 0
        self.pseudoRotation = 0

        self.score = 0
        self.scoreGiven = False
        self.gameOver = False

    def updatePosition(self, jump):
        
        if not jump:
            self.yVelocity += gravity
        else:
            self.yVelocity = globalBirdYJumpAcceleration

        self.yPos += self.yVelocity
        self.trueRotation = math.atan(-self.yVelocity/globalBirdXVelocity) * rad2deg

        if abs(self.trueRotation - self.pseudoRotation) < globalBirdRotateSpeed:
            self.pseudoRotation = self.trueRotation
        elif self.trueRotation - self.pseudoRotation > globalBirdRotateSpeed:
            self.pseudoRotation += globalBirdRotateSpeed
        else:
            self.pseudoRotation -= globalBirdRotateSpeed

    def rotatedImage(self):

        rotatedImage = pygame.transform.rotate(flappyBirdImage, self.pseudoRotation)
        rotatedImageRect = rotatedImage.get_rect()
        rotatedImageRect.center = (self.xPos + birdSize[0]/2, self.yPos + birdSize[1]/2)
        return rotatedImage, rotatedImageRect

    def checkForDeath(self):

        if self.yPos <= -birdCollisionTolerancy or self.yPos + birdSize[1] >= (height - groundSize[1]) + (birdCollisionTolerancy*2):
            self.gameOver = True

        elif pipeParameter <= birdBlitPosition[0] + birdSize[0] - birdCollisionTolerancy and pipeParameter + pipeSize[0] >= birdBlitPosition[0] + birdCollisionTolerancy:
            if self.yPos < pipes[0] - (pipeGap/2) - birdCollisionTolerancy or self.yPos + birdSize[1] > pipes[0] + (pipeGap/2) + birdCollisionTolerancy:
                self.gameOver = True

    def NeuralNetwork(self):

        pipe = pipes[0]
        distanceFromPipe = pipeParameter
        if pipeParameter + pipeSize[0] < birdBlitPosition[0]:
            pipe = pipes[1]
            distanceFromPipe = pipeParameter + pipeDistance

        inputs = [self.yPos, self.yVelocity, pipe - (pipeGap/2) - birdCollisionTolerancy, pipe + (pipeGap/2) - birdSize[1] + birdCollisionTolerancy, distanceFromPipe]

        interNodes = [0, 0, 0, 0, 0]
        
        i = 0
        while i < noOfInterNodes:
            
            j = 0
            while j < len(inputs):

                interNodes[i] += inputs[j] * self.brain[0][i][j]
                j += 1

            i += 1

        output = False
        trigger = 0

        i = 0
        while i < len(interNodes):
            trigger += interNodes[i] * self.brain[1][i]
            i += 1

        if trigger >= 2.5:
            output = True

        return output

MainBird = FlappyBird()
MainBird.brain = MainBrain

i = 0
while i < pipeCount:
    pipes.append(random.randint(pipeDeadZone, height - (groundSize[1] + pipeDeadZone)))
    i += 1

def GeneratePipes():

    global pipeParameter, pipes

    pipeParameter -= globalBirdXVelocity*visualGroundSpeedFactor

    if pipeParameter <= -pipeSize[0]:

        pipeParameter = pipeDistance - pipeSize[0]
        pipes.pop(0)
        pipes.append(random.randint(pipeDeadZone, height - (groundSize[1] + pipeDeadZone)))

def SetGroundParameter():

    global groundParameter, MainBird

    groundParameter -= globalBirdXVelocity*visualGroundSpeedFactor
    if groundParameter <= -groundSize[0]:
        groundParameter = 0
        MainBird.scoreGiven = False

    if pipeParameter + pipeSize[0] <= birdBlitPosition[0] and not MainBird.scoreGiven:
        MainBird.score += 1
        MainBird.scoreGiven = True

def UpdateScreen():

    display.blit(backGroundImage, (0,0))
    display.blit(backGroundImage, (backGroundSize[0],0))

    for pipe in pipes:

        display.blit(topPipeImage, (pipeParameter + (pipeDistance * pipes.index(pipe)), pipe - ((pipeGap/2) + pipeSize[1])))
        display.blit(bottomPipeImage, (pipeParameter + (pipeDistance * pipes.index(pipe)), pipe + (pipeGap/2)))

    for groundPosition in groundPositions:
        display.blit(groundImage, (groundPosition[0] + groundParameter, groundPosition[1]))

    rotatedImage = MainBird.rotatedImage()
    display.blit(rotatedImage[0], rotatedImage[1])

    scoreImage = impactFont.render(str(MainBird.score), True, (255,255,255))
    display.blit(scoreImage, scorePosition)

    pygame.display.update()

while not MainBird.gameOver:

    clock.tick(gameFps)

    jump = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    jump = MainBird.NeuralNetwork()
    MainBird.updatePosition(jump)
    MainBird.checkForDeath()

    GeneratePipes()
    SetGroundParameter()
    UpdateScreen()

jump = True
while True:

    clock.tick(gameFps)

    pygame.display.set_caption("Game Over")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    MainBird.updatePosition(jump)
    jump = False

    UpdateScreen()