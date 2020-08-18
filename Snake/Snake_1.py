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
        self.size = 20
        self.list = []
        self.direction = 'right'
        for i in range(self.length):
            self.list.append([self.x - self.size * i, self.y])

    def draw(self):
        pygame.display.update()
        win.fill((255, 255, 255))
        for i in range(self.length):
            pygame.draw.rect(win, (0, 0, 0), (self.list[i][0], self.list[i][1], self.size, self.size))

    def move(self):
        self.change_direction()
        if self.direction == 'right':
            self.list[-1][0] += self.size
        if self.direction == 'left':
            self.list[-1][0] -= self.size
        if self.direction == 'up':
            self.list[-1][1] -= self.size
        if self.direction == 'down':
            self.list[-1][1] += self.size

        for i in range(self.length -1):
            self.list[i][0] = self.list[i + 1][0]
            self.list[i][1] = self.list[i + 1][1]

    def change_direction(self):
        keys = pygame.key.get_pressed()
        if keys[K_UP] and self.direction != 'down':
            self.direction = 'up'
        if keys[K_RIGHT] and self.direction != 'left':
            self.direction = 'right'
        if keys[K_LEFT] and self.direction != 'right':
            self.direction = 'left'
        if keys[K_DOWN] and self.direction != 'up':
            self.direction = 'down'


#                                             -------------Classes-------------


snake = Snake()
while True:
    snake.move()
    snake.draw()
    clock.tick(10)
    stop()
