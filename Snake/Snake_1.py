import pygame
import random as rand
import time
from pygame.locals import *

pygame.init()

#                                             ------------Variables------------

w = 500
h = w
win = pygame.display.set_mode((w, h))


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
        self.leng = 3
        self.list = []
        for i in range(self.leng):
            self.list.append((self.x - 5 * i, self.y))
            print(self.list[i][0], self.list[i][1])

    def draw(self):
        for i in range(self.leng):
            pygame.draw.rect(win, (255, 255, 255), (self.list[i][0], self.list[i][1], 5, 5))
            pygame.display.update()

    def move(self):
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_d]:
            print("hi")
            # for i in range(self.leng - 1):
            #   self.list[i][0] = self.list[i + 1]
            #   print(self.list[i])
            # self.list[-1] = self.list[-1] + 5


#                                             -------------Classes-------------


snake = Snake()
while True:
    snake.draw()
    snake.move()
