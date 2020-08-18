import pickle
import pygame
from pygame.locals import *
import random
import sys

while True:

    clock = pygame.time.Clock()

    width = 500
    height = 500

    blue = (133, 180, 255)
    yellow = (255, 255, 165)
    darkYellow = (255, 255, 0)
    red = (255, 150, 150)

    gameOver = False
    new_highscore = False
    restart = False

    win = pygame.display.set_mode((500, 500))
    win.fill((255, 255, 255))


    class Coordinate:

        def __init__(self, x, y):
            self.x = int(x)
            self.y = int(y)

        def Coordinate(self, x, y):
            self.x = int(x)
            self.y = int(y)

        def Position(self):
            return self.x, self.y, 25, 25


    class SnakeBlock:

        def __init__(self):
            self.position = Coordinate(0, 0)

        def updateSnakeBlock(self):
            pygame.draw.rect(win, yellow, self.position.Position())


    class Snake:

        def __init__(self):

            self.side = 25
            self.headPosition = Coordinate(self.side * 9, self.side * 9)
            self.velocityX = 1
            self.velocityY = 0
            self.score = 0

            self.snake = []
            self.timestampsX = []
            self.timestampsY = []

        def updateSnake(self):

            snakeBlocksDrawn = 0

            self.timestampsX.append(self.headPosition.x)
            self.timestampsY.append(self.headPosition.y)

            self.headPosition.x += self.velocityX * self.side
            self.headPosition.y += self.velocityY * self.side

            if len(self.timestampsX) > 400:
                self.timestampsX.pop(0)
                self.timestampsY.pop(0)

            while snakeBlocksDrawn < len(self.snake):
                self.snake[snakeBlocksDrawn].position.Coordinate(self.timestampsX[-(snakeBlocksDrawn + 1)],
                                                                 self.timestampsY[-(snakeBlocksDrawn + 1)])
                self.snake[snakeBlocksDrawn].updateSnakeBlock()

                snakeBlocksDrawn += 1

            pygame.draw.rect(win, darkYellow, self.headPosition.Position())

            pygame.display.set_caption("Score:{}".format(self.score))

            pygame.display.update()

        def die(self):

            global gameOver

            snakeBlocksChecked = 0

            if (self.headPosition.x < 0) or (self.headPosition.x + self.side > width) or (self.headPosition.y < 0) or (
                    self.headPosition.y + self.side > height):
                gameOver = True

            while snakeBlocksChecked < len(self.snake):

                if (self.snake[snakeBlocksChecked].position.x == self.headPosition.x) and (
                        self.snake[snakeBlocksChecked].position.y == self.headPosition.y):

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

                if (self.Position.x == snake.headPosition.x) and (self.Position.y == snake.headPosition.y):

                    chance = random.randint(1, 15)

                    if self.poweredUP:

                        snake.score += 3
                        snake.snake.append(SnakeBlock())
                        snake.snake.append(SnakeBlock())
                        snake.snake.append(SnakeBlock())

                    else:

                        snake.score += 1
                        snake.snake.append(SnakeBlock())

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

                pygame.draw.rect(win, blue, self.Position.Position())

            else:

                pygame.draw.rect(win, red, self.Position.Position())


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

        if keys[K_ESCAPE]:
            exit()

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

        if keys[pygame.K_RETURN]:
            restart = True
