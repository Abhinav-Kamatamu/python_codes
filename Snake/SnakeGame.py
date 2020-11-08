import pickle
import pygame
from pygame.locals import *
import random
import sys

while True:

    clock = pygame.time.Clock()

    width = 500
    height = 500

    short = 25

    blue = (255, 255, 125)
    yellow = (184, 255, 203)
    darkYellow = (100, 255, 100)
    red = (255, 150, 150)

    gameOver = False
    new_highscore = False
    restart = False

    win = pygame.display.set_mode((width, height))
    win.fill((255, 255, 255))


    class Coordinate:

        def __init__(self, x, y):
            self.x = int(x)
            self.y = int(y)

        def Coordinate(self, x, y):
            self.x = int(x)
            self.y = int(y)

        def Position(self, xOffset, yOffset, w, h):
            return self.x + xOffset, self.y + yOffset, w, h


    class SnakeBlock:

        def __init__(self):
            self.position = Coordinate(0, 0)
            self.neighbours = []

        def updateSnakeBlock(self):

            i = 0

            while i < 2:

                if self.neighbours[i].position.x < self.position.x:
                    pygame.draw.rect(win, yellow, self.position.Position(0, 2, 23, 21))

                if self.neighbours[i].position.x > self.position.x:
                    pygame.draw.rect(win, yellow, self.position.Position(2, 2, 23, 21))

                if self.neighbours[i].position.y < self.position.y:
                    pygame.draw.rect(win, yellow, self.position.Position(2, 0, 21, 23))

                if self.neighbours[i].position.y > self.position.y:
                    pygame.draw.rect(win, yellow, self.position.Position(2, 2, 21, 23))

                if len(self.neighbours) < 2:
                    break

                i += 1


    class Snake:

        def __init__(self):

            self.side = 25
            self.position = Coordinate(self.side * 9, self.side * 9)
            self.velocityX = 1
            self.velocityY = 0
            self.score = 0

            self.blockEaten = False

            self.snake = []
            self.timestampsX = []
            self.timestampsY = []

        def updateSnake(self):

            snakeBlocksDrawn = 0

            self.timestampsX.append(self.position.x)
            self.timestampsY.append(self.position.y)

            self.position.x += self.velocityX * self.side
            self.position.y += self.velocityY * self.side

            if len(self.timestampsX) > 400:
                self.timestampsX.pop(0)
                self.timestampsY.pop(0)

            while snakeBlocksDrawn < len(self.snake):
                self.snake[snakeBlocksDrawn].position.Coordinate(self.timestampsX[-(snakeBlocksDrawn + 1)],
                                                                 self.timestampsY[-(snakeBlocksDrawn + 1)])

                self.snake[snakeBlocksDrawn].updateSnakeBlock()

                snakeBlocksDrawn += 1

            if not self.blockEaten:

                pygame.draw.rect(win, darkYellow, self.position.Position(2, 2, 21, 21))

            else:

                if self.snake[0].position.x < self.position.x:

                    pygame.draw.rect(win, darkYellow, self.position.Position(0, 2, 23, 21))

                if self.snake[0].position.x > self.position.x:

                    pygame.draw.rect(win, darkYellow, self.position.Position(2, 2, 23, 21))

                if self.snake[0].position.y < self.position.y:

                    pygame.draw.rect(win, darkYellow, self.position.Position(2, 0, 21, 23))

                if self.snake[0].position.y > self.position.y:

                    pygame.draw.rect(win, darkYellow, self.position.Position(2, 2, 21, 23))

            pygame.display.set_caption("Score:{}".format(self.score))

            pygame.display.update()

        def die(self):

            global gameOver

            snakeBlocksChecked = 0

            if self.position.x < 0:

                self.position.x = self.side * 19

            elif self.position.x + self.side > width:

                self.position.x = 0

            elif self.position.y < 0:

                self.position.y = self.side * 19

            elif self.position.y + self.side > height:

                self.position.y = 0

            while snakeBlocksChecked < len(self.snake):

                if (self.snake[snakeBlocksChecked].position.x == self.position.x) and (
                        self.snake[snakeBlocksChecked].position.y == self.position.y):

                    gameOver = True
                    break

                else:

                    snakeBlocksChecked += 1


    snake = Snake()


    class Food:

        def __init__(self):

            self.poweredUP = False
            self.side = 25
            self.Position = Coordinate(random.randint(0, 19) * self.side, random.randint(0, 19) * self.side)

        def UpdatePos(self):

            global snake, red

            ok = False
            snakeBlocksChecked = 0

            while not ok:

                if (self.Position.x == snake.position.x) and (self.Position.y == snake.position.y):

                    chance = random.randint(1, 50)

                    if self.poweredUP:

                        snake.score += 10

                        snake.snake.append(SnakeBlock())

                        if not snake.blockEaten:

                            snake.snake[-1].neighbours.append(snake)
                            snake.snake[-2].neighbours.append(snake.snake[-1])

                        else:

                            snake.snake[-1].neighbours.append(snake.snake[-2])

                        snake.snake.append(SnakeBlock())
                        snake.snake[-1].neighbours.append(snake.snake[-2])
                        snake.snake[-2].neighbours.append(snake.snake[-1])

                        snake.snake.append(SnakeBlock())
                        snake.snake[-1].neighbours.append(snake.snake[-2])
                        snake.snake[-2].neighbours.append(snake.snake[-1])

                    else:

                        snake.score += 1

                        snake.snake.append(SnakeBlock())

                        if not snake.blockEaten:

                            snake.snake[-1].neighbours.append(snake)

                        else:

                            snake.snake[-1].neighbours.append(snake.snake[-2])
                            snake.snake[-2].neighbours.append(snake.snake[-1])

                    snake.blockEaten = True
                    self.poweredUP = False
                    self.Position.Coordinate(random.randint(0, 19) * self.side, random.randint(0, 19) * self.side)

                    if chance == 1:
                        self.poweredUP = True

                while snakeBlocksChecked < len(snake.snake):

                    if (self.Position.x == snake.snake[snakeBlocksChecked].position.x) and (
                            self.Position.y == snake.snake[snakeBlocksChecked].position.y):

                        self.Position.Coordinate(random.randint(0, 19) * self.side, random.randint(0, 19) * self.side)
                        break

                    else:

                        snakeBlocksChecked += 1

                else:

                    ok = True

            win.fill((255, 255, 255))

            if self.poweredUP:

                pygame.draw.rect(win, blue, self.Position.Position(2, 2, 21, 21))

            else:

                pygame.draw.rect(win, red, self.Position.Position(2, 2, 21, 21))


    apple = Food()

    while not gameOver:

        clock.tick(10)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if (keys[pygame.K_w] or keys[K_UP]) and snake.velocityY == 0:
            snake.velocityX = 0
            snake.velocityY = -1

        if (keys[pygame.K_a] or keys[K_LEFT]) and snake.velocityX == 0:
            snake.velocityX = -1
            snake.velocityY = 0

        if (keys[pygame.K_s] or keys[K_DOWN]) and snake.velocityY == 0:
            snake.velocityX = 0
            snake.velocityY = 1

        if (keys[pygame.K_d] or keys[K_RIGHT]) and snake.velocityX == 0:
            snake.velocityX = 1
            snake.velocityY = 0

        apple.UpdatePos()
        snake.updateSnake()
        snake.die()

    try:

        with open('score.dat', 'rb') as file:
            highscore = pickle.load(file)

    except:

        highscore = 0

    if highscore < snake.score:

        highscore = snake.score
        new_highscore = True

    elif highscore >= snake.score:

        new_highscore = False

    with open('score.dat', 'wb') as file:
        pickle.dump(highscore, file)

    if not new_highscore:

        pygame.display.set_caption(
            "Game Over (score: {}, highscore: {}) *press enter to restart*".format(snake.score, highscore))

    else:

        pygame.display.set_caption(
            "Game Over (score: {}, highscore: {} [NEW HIGHSCORE!])".format(snake.score, highscore))

    while not restart:

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
