import pygame
from pygame.locals import *
import sys
import random

width = 1000
height = 500

clock = pygame.time.Clock()

white = (255, 255, 255)
yellow = (255, 255, 150)

restart = True
gameOver = False
jumpAble = True

screen = pygame.display.set_mode((width, height))
screen.fill(white)

pygame.display.update()

while restart:

    restart = False

    class Coordinate:

        def __init__(self, x, y):

            self.x = int(x)
            self.y = int(y)

        def ReturnRect(self, width, height):

            return self.x, self.y, width, height

    class FlappyBird:

        def __init__(self):

            self.height = 50
            self.width = 65
            self.position = Coordinate(width/4, height/2 - (self.height/2))
            self.velocity = 0

        def Draw(self):

            screen.fill(white)

            pygame.draw.ellipse(screen, yellow, self.position.ReturnRect(self.width, self.height))

            pygame.display.update()

        def Jump(self):

            global jumpAble

            jumpAble = False

            instataneousVelocity = 10

            while instataneousVelocity >= -10:

                self.velocity = 0
                self.velocity = instataneousVelocity
                self.position.y += self.velocity

                self.Draw()

                instataneousVelocity -= 1

            self.velocity = 0
            jumpAble = True

    bird = FlappyBird()

    while not gameOver:

        clock.tick(60)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if keys[K_SPACE] and jumpAble:

            bird.Jump()

        bird.Draw()
