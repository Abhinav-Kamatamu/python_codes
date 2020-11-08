import pygame
from pygame.locals import *
import random
import sys

restart = True

while restart:

    particles = []

    clock = pygame.time.Clock()

    pause = False
    restart = False

    width = 600
    height = 600

    teamColors = [
                    255, 0, 0,
                    0, 255, 0,
                    0, 0, 255,
                    255, 255, 0
                 ]

    white = (255, 255, 255)

    win = pygame.display.set_mode((width, height))
    win.fill(white)

    class Coordinate:

        def __init__(self, x, y):

            self.x = x
            self.y = y

        def rect(self):

            return self.x, self.y, 2, 2

    class Particle:

        def __init__(self, x, y, teamNo):

            self.position = Coordinate(x, y)
            self.team = teamNo
            self.color = (teamColors[3 * teamNo], teamColors[3 * teamNo + 1], teamColors[3 * teamNo + 2])

        def DrawParticle(self):

            pygame.draw.rect(win, self.color, self.position.rect())

    def Initiate():

        global particles

        teamNum = 0

        while teamNum < 4:

            praticlesInstantiated = 0

            while praticlesInstantiated < 50:

                particles.append(Particle(random.randint(0, 598), random.randint(0, 598), teamNum))

                praticlesInstantiated += 1

            teamNum += 1


    Initiate()

    def redrawWindowScreen():

        global particles

        particlesDrawn = 0

        win.fill(white)

        while particlesDrawn < len(particles):

            particles[particlesDrawn].DrawParticle()

            particlesDrawn += 1

    def main():

        global restart, pause

        clock.tick(5)

        redrawWindowScreen()
        pygame.display.update()

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if keys[K_SPACE]:

            pause = True

        if keys[K_ESCAPE]:
            pygame.quit()
            sys.exit()

        if keys[pygame.K_RETURN]:
            restart = True
            pause = True

    while not pause:

        main()