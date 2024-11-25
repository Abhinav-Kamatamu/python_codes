import pickle
from re import A
import pygame
from pygame.locals import *
import random
import sys

noOfLayersOfHiddenLayers = 2
noOfNodesInHiddenLayer = 5

while True:

    clock = pygame.time.Clock()

    width = 500
    height = 500

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

        def Position(self):
            return self.x, self.y, 25, 25


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

                    chance = random.randint(1, 50)

                    if self.poweredUP:

                        snake.score += 10
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

            self.brain = []

            for i in range(1,noOfLayersOfHiddenLayers + 2):
                self.brain.append([])

            for i in range(0,399 + 6 + 1):
                self.brain[0].append([])
                for j in range (0, noOfNodesInHiddenLayer):
                    self.brain[0][i].append(random.uniform(-1,1))
            
            for i in range(1,noOfLayersOfHiddenLayers):
                for j in range(0,noOfNodesInHiddenLayer):
                    self.brain[i].append([])
                    for k in range(0,noOfNodesInHiddenLayer):
                        self.brain[i][j].append(random.uniform(-1,1))

            for i in range(0, noOfNodesInHiddenLayer):
                self.brain[-1].append([])
                for k in range(0,4 + 1):
                    self.brain[-1][i].append(random.uniform(-1,1)) 

            print(self.brain)

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

            if self.headPosition.x < 0:

                self.headPosition.x = self.side * 19

            elif self.headPosition.x + self.side > width:

                self.headPosition.x = 0

            elif self.headPosition.y < 0:

                self.headPosition.y = self.side * 19

            elif self.headPosition.y + self.side > height:

                self.headPosition.y = 0

            while snakeBlocksChecked < len(self.snake):

                if (self.snake[snakeBlocksChecked].position.x == self.headPosition.x) and (
                        self.snake[snakeBlocksChecked].position.y == self.headPosition.y):

                    gameOver = True
                    break

                else:
                    snakeBlocksChecked += 1

        def NeuralNetwork(self):

            inputs = [self.headPosition.x, self.headPosition.y, apple.Position.x, apple.Position.y, self.velocityX, self.velocityY]

            for i in range(0,399):
                if i < len(self.snake):
                    inputs.append(self.headPosition.x-self.snake[i].position.x)
                    inputs.append(self.headPositoin.y-self.snake[i].position.y)
                else:
                    inputs.append(False)
                    inputs.append(False)

            interLayers = []
            outputs = []

            for i in range(0, noOfLayersOfHiddenLayers):
                interLayers.append([])
                for j in range(0, noOfNodesInHiddenLayer):
                        interLayers[i].append(0)

            for i in range(0,5):
                outputs.append(0)

            for j in range(0,len(self.brain[0])):
                for k in range(0, len(self.brain[0][j])):
                    if inputs[j] is not False: 
                        interLayers[0][k] += inputs[j] * self.brain[0][j][k]

            for i in range(1,noOfLayersOfHiddenLayers):
                for k in range(0, noOfNodesInHiddenLayer):
                    for j in range(0, noOfNodesInHiddenLayer):
                        interLayers[i][k] += interLayers[i-1][j] * self.brain[i][j][k]
                        
            for i in range(0, len(outputs)):
                for j in range(0, noOfNodesInHiddenLayer):
                    outputs[i] += interLayers[-1][j] * self.brain[-1][j][i]

            return outputs.index(max(outputs))

    snake = Snake()

    while not gameOver:

        clock.tick(10)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        output = snake.NeuralNetwork()

        print(output)

        if output == 1 and snake.velocityY == 0:
            snake.velocityX = 0
            snake.velocityY = -1

        if output == 2 and snake.velocityX == 0:
            snake.velocityX = -1
            snake.velocityY = 0

        if output == 3 and snake.velocityY == 0:
            snake.velocityX = 0
            snake.velocityY = 1

        if output == 4 and snake.velocityX == 0:
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