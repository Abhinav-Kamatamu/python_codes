import pygame
import random as rand
import time

pygame.init()

#                                             ------------Variables------------

w = 500
h = w
win = pygame.display.set_mode((w, h))


#                                             ------------Variables------------


#                                             -------------Classes-------------

class Snake():
    def __init__(self):
        self.x = rand.randint(0, w)
        self.y = rand.randint(0, h)
        self.leng = 3
        self.x_list = []
        for i in range(self.leng):
            self.x_list.append((self.x-5*i))

    def draw(self):
        for i in range(self.leng):
            pygame.draw.rect(win,(255,255,255),(self.x_list[i],self.y,5,5))
            pygame.display.update()


#                                             -------------Classes-------------


snake = Snake()
snake.draw()