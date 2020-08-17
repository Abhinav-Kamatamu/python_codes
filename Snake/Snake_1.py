import pygame
import random as rand
import time
from pygame.locals import *

pygame.init()

#                                             ------------Variables------------

w = 500
h = w
win = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()


#                                             ------------Variables------------

#                                             ------------Functions------------

def stop():
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()


#                                             ------------Functions------------

#                                             -------------Classes-------------

class Snake:
    def __init__(self):
        self.x = rand.randint(0, w)
        self.y = rand.randint(0, h)
        self.length = 10
        self.list = []
        for i in range(self.length):
            self.list.append([self.x - 5 * i, self.y])

    def draw(self):
        win.fill((0, 0, 0))
        for i in range(self.length):
            pygame.draw.rect(win, (255, 255, 255), (self.list[i][0], self.list[i][1], 5, 5))
            pygame.display.update()

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            for i in range(self.length - 1):
                self.list[i][0] = self.list[i + 1][0]
            self.list[-1][0] = self.list[-1][0] + 5
        if keys[pygame.K_w]:
            for i in range(self.length - 1):
                self.list[i][1] = self.list[i + 1][1]
            self.list[-1][1] = self.list[-1][1] - 5
        if keys[pygame.K_s]:
            for i in range(self.length - 1):
                self.list[i][1] = self.list[i + 1][1]
            self.list[-1][1] = self.list[-1][1] + 5
        if keys[pygame.K_a]:
            for i in range(self.length - 1):
                self.list[i][0] = self.list[i + 1][0]
            self.list[-1][0] = self.list[-1][0] - 5


#                                             -------------Classes-------------


snake = Snake()
while True:
    snake.draw()
    snake.move()
    clock.tick(60)
    stop()
