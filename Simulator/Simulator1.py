import pygame
from pygame.locals import *
import random
import sys

restart = True

while restart:

    particles = []

    clock = pygame.time.Clock()

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
            self.velocity = Coordinate (0 ,0)
            self.team = teamNo
            self.color = (teamColors[3 * teamNo], teamColors[3 * teamNo + 1], teamColors[3 * teamNo + 2])

        def DrawParticle(self):

            pygame.draw.rect(win, self.color, self.position.rect())

        def Move(self):

            self.velocity.x = random.randint(-1,1)
            self.velocity.y = random.randint(-1,1)

            if self.position.x + self.velocity.x > 0 or self.position.x + self.velocity.x < 598:
                self.position.x += self.velocity.x

            if self.position.y + self.velocity.y > 0 or self.position.y + self.velocity.y < 598:
                self.position.y += self.velocity.y


    def UpdateCaption():

        global particles

        redScore = 0
        blueScore = 0
        greenScore = 0
        yellowScore = 0

        particlesCounted = 0

        while particlesCounted < len(particles):

            if particles[particlesCounted].team == 0:
                redScore += 1
            if particles[particlesCounted].team == 1:
                greenScore += 1
            if particles[particlesCounted].team == 2:
                blueScore += 1
            if particles[particlesCounted].team == 3:
                yellowScore += 1

        pygame.diplay.set_caption(f"RED:{redScore} GREEN:{greenScore} BLUE:{blueScore} YELLOW:{yellowScore}")


    def Initiate():

        global particles

        teamNum = 0

        while teamNum < 4:

            praticlesInstantiated = 0

            while praticlesInstantiated < 300:

                particles.append(Particle(random.randint(0, 598), random.randint(0, 598), teamNum))

                praticlesInstantiated += 1

            teamNum += 1

        UpdateCaption()

    Initiate()

    def redrawWindowScreen():

        global particles

        particlesDrawn = 0

        win.fill(white)

        while particlesDrawn < len(particles):

            particles[particlesDrawn].DrawParticle()
            particles[particlesDrawn].Move()

            particlesDrawn += 1

    def main():

        global restart

        clock.tick(144)

        redrawWindowScreen()
        pygame.display.update()

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if keys[K_ESCAPE]:
            pygame.quit()
            sys.exit()

        if keys[pygame.K_RETURN]:
            restart = True
            pause = True

    while not restart:

        main()

