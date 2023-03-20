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
pipeDeadZone = 250
pipeGap = 200
pipeCount = 3
pipeDistance = 450

scoreSize = 36
scorePosition = ((width/2) - scoreSize, 50)

globalMutationFactor = 0.1

noOfInterNodes = 5

rad2deg = 57.2957795131
#--------------------------

#'global variables---------
groundParameter = 0
pipeParameter = width

pipes = []

birdsPerGeneration = 30

generation =  1
MLrunning = True

globalFitness = 0
globalBirdCount = birdsPerGeneration

bestBrain = None
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
arielFont = pygame.font.SysFont("ariel", scoreSize)
#--------------------------

display = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

pygame.display.set_caption("Flappy Bird")

class FlappyBird():

    def __init__(self):

        self.xPos = birdBlitPosition[0]
        self.yPos = birdBlitPosition[1] + random.randint(-50,50)

        self.yVelocity = 0

        self.trueRotation = 0
        self.pseudoRotation = 0

        self.score = 0
        self.scoreGiven = False
        self.gameOver = False
        self.fitness = 0

        self.brain = [[],[]]

        i = 0
        while i < noOfInterNodes:

            self.brain[0].append([])

            j = 0

            while j < noOfInterNodes:
                self.brain[0][i].append(random.uniform(-1,1))
                j += 1
            
            i += 1

        i = 0
        while i < noOfInterNodes:
            self.brain[1].append(random.uniform(-1,1))
            i += 1

    def updatePosition(self, jump):
        
        if not self.gameOver:
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

            self.fitness += 0.1

        else:

            self.xPos -= globalBirdXVelocity * visualGroundSpeedFactor

    def rotatedImage(self):

        rotatedImage = pygame.transform.rotate(flappyBirdImage, self.pseudoRotation)
        rotatedImageRect = rotatedImage.get_rect()
        rotatedImageRect.center = (self.xPos + birdSize[0]/2, self.yPos + birdSize[1]/2)
        return rotatedImage, rotatedImageRect

    def checkForDeath(self):

        global globalBirdCount

        if not self.gameOver:

            if self.yPos <= -birdCollisionTolerancy or self.yPos + birdSize[1] >= (height - groundSize[1]) + (birdCollisionTolerancy*2):
                self.gameOver = True
                globalBirdCount -= 1

            elif pipeParameter <= birdBlitPosition[0] + birdSize[0] - birdCollisionTolerancy and pipeParameter + pipeSize[0] >= birdBlitPosition[0] + birdCollisionTolerancy:
                if self.yPos < pipes[0] - (pipeGap/2) - birdCollisionTolerancy or self.yPos + birdSize[1] > pipes[0] + (pipeGap/2) + birdCollisionTolerancy:
                    self.gameOver = True
                    globalBirdCount -= 1

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

    def Mutate(self, localMutationFactor):

        i = 0
        while i < len(self.brain[0]):
            j = 0
            while j < len(self.brain[0][i]):
                self.brain[0][j][i] += random.uniform(-1,1) * localMutationFactor
                j += 1
            i += 1
        i = 0
        while i < len(self.brain[1]):
            self.brain[1][i] += random.uniform(-1,1) * localMutationFactor
            i += 1

    def returnBrain(self):

        clonedBrain = [[],[]]
        i = 0
        while i < noOfInterNodes:

            clonedBrain[0].append([])

            j = 0

            while j < noOfInterNodes:
                clonedBrain[0][i].append(self.brain[0][i][j])
                j += 1
            
            i += 1

        i = 0
        while i < noOfInterNodes:
            clonedBrain[1].append(self.brain[1][i])
            i += 1

        return clonedBrain
        
FlappyBirds = []

i = 0
while i < birdsPerGeneration:
    FlappyBirds.append(FlappyBird())
    i += 1

def initiatePipes():

    global pipes

    pipes = []

    i = 0
    while i < pipeCount:
        pipes.append(random.randint(pipeDeadZone, height - (groundSize[1] + pipeDeadZone)))
        i += 1

initiatePipes()

def GeneratePipes():

    global pipeParameter, pipes

    pipeParameter -= globalBirdXVelocity*visualGroundSpeedFactor

    if pipeParameter <= -pipeSize[0]:

        pipeParameter = pipeDistance - pipeSize[0]
        pipes.pop(0)
        pipes.append(random.randint(pipeDeadZone, height - (groundSize[1] + pipeDeadZone)))

def SetGroundParameter():

    global groundParameter, FlappBirds

    groundParameter -= globalBirdXVelocity*visualGroundSpeedFactor
    if groundParameter <= -groundSize[0]:
        groundParameter = 0

def UpdateScreen():

    display.blit(backGroundImage, (0,0))
    display.blit(backGroundImage, (backGroundSize[0],0))

    for pipe in pipes:

        display.blit(topPipeImage, (pipeParameter + (pipeDistance * pipes.index(pipe)), pipe - ((pipeGap/2) + pipeSize[1])))
        display.blit(bottomPipeImage, (pipeParameter + (pipeDistance * pipes.index(pipe)), pipe + (pipeGap/2)))

    for groundPosition in groundPositions:
        display.blit(groundImage, (groundPosition[0] + groundParameter, groundPosition[1]))

    for flappyBird in FlappyBirds:

        rotatedImage = flappyBird.rotatedImage()
        display.blit(rotatedImage[0], rotatedImage[1])
        
    generationImage = arielFont.render(f'generation: {generation}', True, (255,255,255))
    birdAliveImage = arielFont.render(f'birds alive: {globalBirdCount}', True, (255,255,255))
    fitnessImage = arielFont.render(f'fitness: {globalFitness//1}', True, (255,255,255))

    display.blit(generationImage, (0,0))
    display.blit(birdAliveImage, (0,scoreSize))
    display.blit(fitnessImage, (0,scoreSize*2))

    pygame.display.update()

def ReproduceBirds():

    global FlappyBirds, bestBrain

    FlappyBirds.sort(key=lambda x: x.fitness)

    bestBrain = FlappyBirds[-1].brain

    i = 0
    while i < (birdsPerGeneration)//2:
        deletedFlappyBird = FlappyBirds[0]
        FlappyBirds.pop(0)
        del deletedFlappyBird
        i += 1  

    i = 0
    while i < birdsPerGeneration//2:
        offspring = FlappyBird()
        FlappyBirds.append(offspring)
        offspring.brain = FlappyBirds[i].returnBrain()
        offspring.Mutate(globalMutationFactor)
        i += 1

def ResetGeneration():

    global pipeParameter, groundParameter, FlappyBirds, globalBirdCount, generation, globalFitness

    ReproduceBirds()

    generation += 1
    globalFitness = 0

    for flappyBird in FlappyBirds:

        flappyBird.xPos = birdBlitPosition[0]
        flappyBird.yPos = birdBlitPosition[1] + random.randint(-50,50)

        flappyBird.yVelocity = 0

        flappyBird.trueRotation = 0
        flappyBird.pseudoRotation = 0

        flappyBird.score = 0
        flappyBird.scoreGiven = False
        flappyBird.gameOver = False
        flappyBird.fitness = 0

    pipeParameter = width
    groundParameter = 0

    globalBirdCount = birdsPerGeneration

    initiatePipes()

def getBrain():

    FlappyBirds.sort(key=lambda x: x.fitness)

    return FlappyBirds[-1].returnBrain()

while MLrunning:

    clock.tick(gameFps)

    for event in pygame.event.get():
    
        if event.type == pygame.QUIT:

            ReproduceBirds()
            print(bestBrain)

            pygame.quit()
            sys.exit()

    for flappyBird in FlappyBirds:
    
        jump = flappyBird.NeuralNetwork()

        flappyBird.updatePosition(jump)
        flappyBird.checkForDeath()

    globalFitness += 0.1

    if globalBirdCount <= 0:

        ResetGeneration()

    GeneratePipes()
    SetGroundParameter()
    UpdateScreen()

