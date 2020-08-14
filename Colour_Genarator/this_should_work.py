import pygame
from time import sleep

win = pygame.display.set_mode((255, 255))
win.fill((255, 255, 255))

pixelsFilled = 0

class pos():

    def __init__(self):

        self.x = 0
        self.y = 0

class color():

    def __init__(self):

        self.r = 255
        self.g = 255
        self.b = 255
        self.rgb = self.r,self.g,self.b

    def ReturnColor(self):

        return self.rgb

color = color()
pos = pos()


def stop():
    for i in pygame.event.get():
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_ESCAPE:
                exit()
        if i.type == pygame.QUIT:
            exit()

def fill():

    global pixelsFilled

    while pixelsFilled <= 65025 :
        
        pygame.draw.rect(win,color.ReturnColor(),(pos.x,pos.y,1,1))

        if pos.x < 255:

            pos.x += 1

            color.r -= 1
            color.g -= 1

        elif pos.x >= 255:

            pos.x = 0
            pos.y -= 1

            color.r -= 1
            color.g -= 1
            color.b -= 1
 
        pixelsFilled += 1

        pygame.display.update()

fill()

while True:
    stop()
