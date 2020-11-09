import pygame
from pygame.locals import *
import random
import sys

restart = True

while restart:

    particles = []
    tempParticles = []

    clock = pygame.time.Clock()

    restart = False

    width = 600
    height = 600

    scores = [0, 0, 0, 0]

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

            if 0 < self.position.x + self.velocity.x < height - 2:
                self.position.x += self.velocity.x
            if 0 < self.position.y + self.velocity.y < height - 2:
                self.position.y += self.velocity.y

    def UpdateCaption():

        global particles

        particlesCounted = 0

        while particlesCounted < len(particles):

            if particles[particlesCounted].team == 0:
                scores[0] += 1
            if particles[particlesCounted].team == 1:
                scores[1] += 1
            if particles[particlesCounted].team == 2:
                scores[2] += 1
            if particles[particlesCounted].team == 3:
                scores[3] += 1

            particlesCounted += 1

        pygame.display.set_caption(f"RED:{scores[0]}   GREEN:{scores[1]}   BLUE:{scores[2]}   YELLOW:{scores[3]}")

    def CheckReaction():

        global particles, tempParticles

        particlesChecked = 0
        particlesReacted = 0

        while particlesChecked < len(particles):

            while particlesReacted < len(particles):

                if (particles[particlesChecked].team == particles[particlesReacted].team and (-4 < particles[particlesChecked].position.x - particles[particlesReacted].position.x < 4 and -4 < particles[particlesChecked].position.y - particles[particlesReacted].position.y < 4)) and (particlesReacted != particlesChecked):

                    tempParticles.append( Particle(particles[particlesChecked].position.x + random.randint(-100,100), particles[particlesChecked].position.y + random.randint(-100,100), particles[particlesChecked].team))
                    UpdateCaption()

                if (particles[particlesChecked].position.x == particles[particlesReacted].position.x) and (particles[particlesChecked].position.y == particles[particlesReacted].position.y) and particles[particlesChecked].team != particles[particlesChecked].team and scores[particles[particlesChecked].team] > scores [particles[particlesReacted.team]]:

                    del(particles[particlesReacted])
                    pop(particles[particlesReacted])
                    UpdateCaption()

                particlesReacted += 1

            particlesChecked += 1

        particlesAdded = 0

        while particlesAdded < len(tempParticles):

            particles.append(tempParticles[particlesAdded])
            del(tempParticles[particlesAdded])

            particlesAdded += 1


    def Initiate():

        global particles

        teamNum = 0

        while teamNum < 4:

            praticlesInstantiated = 0

            while praticlesInstantiated < 300:

                particles.append(Particle(random.randint(0, width - 2), random.randint(0, height - 2), teamNum))

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

        clock.tick(70000)

        CheckReaction()

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

    while not restart:

        main()

