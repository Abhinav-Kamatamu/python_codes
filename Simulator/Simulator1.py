import pygame
from pygame.locals import *
import random
import sys
import time

pygame.init()

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
                    0, 150, 0,
                    0, 0, 255,
                    200, 200, 0
                 ]

    _00, _01, _02, _03, _04, _05 = [], [], [], [], [], []
    _10, _11, _12, _13, _14, _15 = [], [], [], [], [], []
    _20, _21, _22, _23, _24, _25 = [], [], [], [], [], []
    _30, _31, _32, _33, _34, _35 = [], [], [], [], [], []
    _40, _41, _42, _43, _44, _45 = [], [], [], [], [], []
    _50, _51, _52, _53, _54, _55 = [], [], [], [], [], []

    chunks = [

        _00, _01, _02, _03, _04, _05,
        _10, _11, _12, _13, _14, _15,
        _20, _21, _22, _23, _24, _25,
        _30, _31, _32, _33, _34, _35,
        _40, _41, _42, _43, _44, _45,
        _50, _51, _52, _53, _54, _55,

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
            self.chunk = None
            self.chunkIndex = None

        def DrawParticle(self):

            pygame.draw.rect(win, self.color, self.position.rect())

        def UpdateChunk(self):

            global chunks

            if self.chunk is not None:

                self.chunk[self.chunkIndex].remove(self)

            chunkX = int(self.position.x // width/sqrt(len(chunks)))
            chunkY = int(self.position.y // height/sqrt(len(chunks)))

            self.self.chunkIndex = chunkY * 6 + chunkX

            self.chunk = chunks[self.chunkIndex]
            chunks[self.chunkIndex].append(self)

        def Move(self):

            self.velocity.x = random.randint(-1,1) * (random.random() ** 3)
            self.velocity.y = random.randint(-1,1) * (random.random() ** 3)

            if 0 < self.position.x + self.velocity.x < height - 2:
                self.position.x += self.velocity.x
            if 0 < self.position.y + self.velocity.y < height - 2:
                self.position.y += self.velocity.y

            self.UpdateChunk()

    def UpdateCaption():

        global particles

        particlesCounted = 0

        scores = [0, 0, 0, 0]

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

        global chunks

        #I'm reworking on this
        #I have succefully calculated the chunk of each particles now
        #So i hope it should work

        UpdateCaption()


    def redraw():

        win.fill((0, 0, 0))
        _type_ = pygame.font.Font('freesansbold.ttf', 100)
        text = _type_.render('Simulation', True, (255, 0, 0))
        textrect = text.get_rect()
        textrect.topleft = (30, 230)
        win.blit(text, textrect)

    def init():

        global win

        win.fill((0, 0, 0))

        redraw()
        pygame.display.update()

        time.sleep(3)
        fade = pygame.Surface((600, 600))
        fade.fill((255, 255, 255))

        for alpha in range(0, 100):
            fade.set_alpha(alpha)
            win.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(30)
            pygame.display.update()

    def Initiate():

        global particles

        teamNum = 0

        pygame.display.set_caption("SIMULATION")

        #init()

        while teamNum < 4:

            praticlesInstantiated = 0

            while praticlesInstantiated < 100:

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

