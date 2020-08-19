import pygame
from pygame import *
from pygame.locals import *
import sys
import random

pygame.init()

width = 1000
height = 700

jumpCount = 0
gravityCount = 0

clock = pygame.time.Clock()

white = (255, 255, 255)
yellow = (255, 255, 150)

restart = True
gameOver = False

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

            self.velocity = 5
            self.mass = 1
            self.force = None
            self.gravity = -1

            self.jumpAble = True
            self.isJumping = False

        def Draw(self):

            global gravityCount

            if not self.isJumping:

                gravityCount += 1

                if gravityCount % 20 == 0 and self.gravity > -20:

                    self.gravity -= 1

                self.position.y -= self.gravity

            else:

                self.gravity = 0

            screen.fill(white)

            ellipse = pygame.draw.ellipse(screen, yellow, self.position.ReturnRect(self.width, self.height))


            pygame.display.update()

        def Jump(self):

            global jumpCount

            self.force = (1/2 * self.mass) * (self.velocity ** 2)

            if self.velocity < 0:

                self.force = -self.force

            jumpCount += 1

            if int(self.force) == 0 and jumpCount % 5 == 0:

                self.force = 1

            if jumpCount % 10 == 0:

                self.velocity -= 1

            self.position.y -= int(self.force)

            if self.velocity == 0:

                self.jumpAble = True

            if self.velocity == -6:

                self.gravity = -12
                self.isJumping = False

    bird = FlappyBird()

    while not gameOver:

        clock.tick(120)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if keys[K_SPACE] and bird.jumpAble:

            bird.velocity = 5
            jumpCount = 0

            bird.jumpAble = False
            bird.isJumping = True

        if bird.isJumping:

            bird.Jump()

        bird.Draw()
