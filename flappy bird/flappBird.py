import pygame
import sys
import math

pygame.init()

#'static variables---------
height = 800
width = 1400

birdSize = (112,67)
birdBlitPosition = (200, height/10)

gravity = 0.015
globalBirdXVelocity = 1
globalBirdYJumpAcceleration = -1.75
globalBirdRotateSpeed = 0.05

groundSize = (545,80)
groundPositions = [

                     (0, height - groundSize[1]), 
                     (groundSize[0], height - groundSize[1]), 
                     (groundSize[0]*2, height - groundSize[1]),  
                     (groundSize[0]*3, height - groundSize[1]),

                    ]

backGroundSize = (1440,806)

rad2deg = 57.2957795131
#--------------------------

#'global variables---------
groundParameter = 0
#--------------------------

#'images-------------------
flappyBirdImage = pygame.image.load('flappy bird.png')
flappyBirdImage = pygame.transform.scale(flappyBirdImage, birdSize)

groundImage = pygame.image.load('ground.png')
groundImage = pygame.transform.scale(groundImage, groundSize)

backGroundImage = pygame.image.load('background.png')
backGroundImage = pygame.transform.scale(backGroundImage, backGroundSize)
#--------------------------

display = pygame.display.set_mode((width, height))

class FlappyBird():

    def __init__(self):

        self.xPos = birdBlitPosition[0]
        self.yPos = birdBlitPosition[1]

        self.yVelocity = 0

        self.trueRotation = 0
        self.pseudoRotation = 0

        self.gameOver = False

    def updatePosition(self, jump):
        
        if not jump:
            self.yVelocity += gravity
        else:
            self.yVelocity = globalBirdYJumpAcceleration

        self.yPos += self.yVelocity
        self.trueRotation = math.atan(-self.yVelocity/globalBirdXVelocity) * rad2deg

        self.pseudoRotation += (self.trueRotation - self.pseudoRotation/abs(self.trueRotation - self.pseudoRotation)) * globalBirdRotateSpeed
        if self.trueRotation - self.pseudoRotation < globalBirdRotateSpeed:
            self.pseudoRotation = self.trueRotation

    def rotatedImage(self):

        rotatedImage = pygame.transform.rotate(flappyBirdImage, self.trueRotation)
        return rotatedImage

MainBird = FlappyBird()

def setGroundParameter():

    global groundParameter

    groundParameter -= globalBirdXVelocity
    if groundParameter <= -groundSize[0]:
        groundParameter = 0

def UpdateScreen():
    
    display.blit(backGroundImage, (0,0))
    display.blit(MainBird.rotatedImage(), (MainBird.xPos, MainBird.yPos))

    for groundPosition in groundPositions:
        display.blit(groundImage, (groundPosition[0] + groundParameter, groundPosition[1]))

    pygame.display.update()

while True:

    jump = False

    for event in pygame.event.get():
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jump = True

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    MainBird.updatePosition(jump)

    setGroundParameter()
    UpdateScreen()