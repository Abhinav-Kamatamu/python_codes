import pygame
from pygame.locals import *
import random
import sys
import time
from math import *

pygame.init()

restart = True

while restart:

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

    _00, _01, _02, _03, _04, _05, _06, _07, _08, _09, _010, _011             = [], [], [], [], [], [], [], [], [], [], [], []
    _10, _11, _12, _13, _14, _15, _16, _17, _18, _19, _110, _111             = [], [], [], [], [], [], [], [], [], [], [], []
    _20, _21, _22, _23, _24, _25, _26, _27, _28, _29, _210, _211             = [], [], [], [], [], [], [], [], [], [], [], []
    _30, _31, _32, _33, _34, _35, _36, _37, _38, _39, _310, _311             = [], [], [], [], [], [], [], [], [], [], [], []
    _40, _41, _42, _43, _44, _45, _46, _47, _48, _49, _410, _411             = [], [], [], [], [], [], [], [], [], [], [], []
    _50, _51, _52, _53, _54, _55, _56, _57, _58, _59, _510, _511             = [], [], [], [], [], [], [], [], [], [], [], []
    _60, _61, _62, _63, _64, _65, _66, _67, _68, _69, _610, _611             = [], [], [], [], [], [], [], [], [], [], [], []
    _70, _71, _72, _73, _74, _75, _76, _77, _78, _79, _710, _711             = [], [], [], [], [], [], [], [], [], [], [], []
    _80, _81, _82, _83, _84, _85, _86, _87, _88, _89, _810, _811             = [], [], [], [], [], [], [], [], [], [], [], []
    _90, _91, _92, _93, _94, _95, _96, _97, _98, _99, _910, _911             = [], [], [], [], [], [], [], [], [], [], [], []
    _100, _101, _102, _103, _104, _105, _106, _107, _108, _109, _1010, _1011 = [], [], [], [], [], [], [], [], [], [], [], []
    _110, _111, _112, _113, _114, _115, _116, _117, _118, _119, _1110, _1111 = [], [], [], [], [], [], [], [], [], [], [], []

    chunks = [

    _00, _01, _02, _03, _04, _05, _06, _07, _08, _09, _010, _011,
    _10, _11, _12, _13, _14, _15, _16, _17, _18, _19, _110, _111,
    _20, _21, _22, _23, _24, _25, _26, _27, _28, _29, _210, _211,
    _30, _31, _32, _33, _34, _35, _36, _37, _38, _39, _310, _311,
    _40, _41, _42, _43, _44, _45, _46, _47, _48, _49, _410, _411,
    _50, _51, _52, _53, _54, _55, _56, _57, _58, _59, _510, _511,
    _60, _61, _62, _63, _64, _65, _66, _67, _68, _69, _610, _611,
    _70, _71, _72, _73, _74, _75, _76, _77, _78, _79, _710, _711,
    _80, _81, _82, _83, _84, _85, _86, _87, _88, _89, _810, _811,
    _90, _91, _92, _93, _94, _95, _96, _97, _98, _99, _910, _911,
    _100, _101, _102, _103, _104, _105, _106, _107, _108, _109, _1010, _1011,
    _110, _111, _112, _113, _114, _115, _116, _117, _118, _119, _1110, _1111,

    ]

    tempParticles = []

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
            self.reacted = True
            self.cooldown = 0

        def DrawParticle(self):

            pygame.draw.rect(win, self.color, self.position.rect())

        def ClampPos(self):

            if self.position.x < 0:
                self.position.x = 0 + random.randint(0,10)
            if self. position.x > (width - 2):
                self.position.x = (width - random.randint(2,12))
            if self.position.y < 0:
                self.position.y = 0 + random.randint(0,10)
            if self. position.y > (height - 2):
                self.position.y = (height - (random.randint(2,12)))

        def UpdateChunk(self):

            global chunks

            self.ClampPos()

            if self.chunk is not None and self in self.chunk:

                self.chunk.remove(self)

            chunkX = int(self.position.x // 50)
            chunkY = int(self.position.y // 50)

            self.chunkIndex = chunkY * 12 + chunkX

            self.chunk = chunks[self.chunkIndex]
            chunks[self.chunkIndex].append(self)

        def Move(self):

            self.velocity.x = random.randint(-1,1) * (random.random() ** 3)
            self.velocity.y = random.randint(-1,1) * (random.random() ** 3)

            if 0 < self.position.x + self.velocity.x < height - 2:
                self.position.x += self.velocity.x
            if 0 < self.position.y + self.velocity.y < height - 2:
                self.position.y += self.velocity.y

            self.cooldown -= 1

            if self.cooldown <= 0:

                self.reacted = False

    def UpdateCaption():

        global chunks

        scores = [0, 0, 0, 0]

        i = 0

        while i < len(chunks):

            currentChunk = chunks[i]
            particlesCounted = 0

            while particlesCounted < len(currentChunk):

                if currentChunk[particlesCounted].team == 0:
                    scores[0] += 1
                if currentChunk[particlesCounted].team == 1:
                    scores[1] += 1
                if currentChunk[particlesCounted].team == 2:
                    scores[2] += 1
                if currentChunk[particlesCounted].team == 3:
                    scores[3] += 1

                particlesCounted += 1

            i += 1

        pygame.display.set_caption(f"RED:{scores[0]}   GREEN:{scores[1]}   BLUE:{scores[2]}   YELLOW:{scores[3]}")

    def CheckReaction():

        global chunks, width, height, tempParticles

        i = 0

        while i < len(chunks):

            j = 0
            currentChunk = chunks[i]

            while j < len(currentChunk):

                k = 0
                currentParticle = currentChunk[j]

                while k < len(chunks[i]):

                    l = 0
                    currentReactant = currentChunk[k]

                    if (-1 < (currentParticle.position.x - currentReactant.position.x) < 1) and (-1 < (currentParticle.position.y - currentReactant.position.y) < 1) and (currentParticle.team == currentReactant.team) and (j != k):

                        if not currentParticle.reacted and not currentReactant.reacted:

                            tempParticles.append(Particle(currentParticle.position.x + random.randint(-100,100),currentParticle.position.y + random.randint(-100,100),currentParticle.team))

                            currentParticle.reacted = True
                            currentReactant.reacted = True

                            currentParticle.cooldown = random.randint(1000000,1500000)
                            currentParticle.cooldown = random.randint(1000000,1500000)

                        while l < len(currentChunk):

                            currentDeletant = currentChunk[l]

                            if (-1 < (currentDeletant.position.x - currentReactant.position.x) < 1) and (-1 < (currentDeletant.position.y - currentReactant.position.y) < 1) and (currentDeletant.team != currentReactant.team):

                                if currentDeletant in currentChunk:

                                    currentChunk.remove(currentDeletant)
                                    del currentDeletant

                            l += 1

                    k += 1

                j += 1

            i += 1

        while len(tempParticles) > 0:

            tempParticles[0].UpdateChunk()
            chunks[tempParticles[0].chunkIndex].append(tempParticles[0])
            tempParticles.pop(0)

        UpdateCaption()


    def redraw():

        win.fill((0, 0, 0))

        image = pygame.image.load('simulation.png')
        win.blit(image, (0, 0))

    def init():

        global win

        win.fill((0, 0, 0))

        redraw()
        pygame.display.update()

        time.sleep(3)
        fade = pygame.Surface((600, 600))
        fade.fill((255, 255, 255))

        for alpha in range(0, 50):
            fade.set_alpha(alpha)
            win.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(30)
            pygame.display.update()

    def Initiate():

        global tempParticles

        teamNum = 0

        pygame.display.set_caption("SIMULATION")

        #init()

        while teamNum < 4:

            praticlesInstantiated = 0

            while praticlesInstantiated < 100:

                tempParticles.append(Particle(random.randint(0, width - 2), random.randint(0, height - 2), teamNum))
                tempParticles[0].UpdateChunk()
                tempParticles.pop(0)

                praticlesInstantiated += 1

            teamNum += 1

        UpdateCaption()

    Initiate()

    def redrawWindowScreen():

        global tempParticles, chunks

        i = 0

        win.fill(white)

        while i < len(chunks):

            currentChunk = chunks[i]

            particlesDrawn = 0

            while particlesDrawn < len(currentChunk):

                currentChunk[particlesDrawn].Move()
                currentChunk[particlesDrawn].DrawParticle()

                particlesDrawn += 1

            i += 1

        i = 0

        while i < len(chunks):

            particlesDrawn = 0

            while particlesDrawn < len(currentChunk):

                currentChunk[particlesDrawn].UpdateChunk()

                particlesDrawn += 1

            i += 1


    def main():

        global restart

        clock.tick(70)

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

