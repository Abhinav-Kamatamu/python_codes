import pygame
from pygame.locals import *
import random

pygame.init()

WIDTH = 700
HEIGHT = WIDTH
GRID_SIZE = 25
CELL_SIZE = WIDTH // GRID_SIZE

WINDOW_COLOUR = (255, 255, 255)

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

FPS = 60
speed = 1
speed_factor = 10
clock = pygame.time.Clock()


def get_coordinates(position):
    return (position[0] - 1) * CELL_SIZE, (position[1] - 1) * CELL_SIZE


class Snake:
    def __init__(self):
        self.head_pos = (9, 13)
        self.tail_pos = [(5,13),(6,13), (7,13),(8,13)]
        self.direction = (1, 0)
        self.head_colour = (0, 255, 0)
        self.tail_colour = (200, 255, 200)

        self.grow = False

    def move(self):
        self.tail_pos.append(self.head_pos)
        if not self.grow:
            del self.tail_pos[0]
        self.head_pos = (self.head_pos[0] + self.direction[0], self.head_pos[1] + self.direction[1])
        self.grow = False

    def eat(self):
        self.grow = True

    def turn(self, direction):
        if direction is not None:
            if direction != tuple(-x for x in self.direction):
                self.direction = direction

    def check_over(self):
        if (
                (self.head_pos[0] > GRID_SIZE) or
                (self.head_pos[0] < 0) or
                (self.head_pos[1] > GRID_SIZE) or
                (self.head_pos[1] == 0)
        ):
            return True
        for tail in self.tail_pos:
            if (self.head_pos[0] + self.direction[0], self.head_pos[1] + self.direction[1]) == tail and tail != \
                    self.tail_pos[0]:
                return True

    def draw(self):
        pygame.draw.rect(WINDOW, self.head_colour, get_coordinates(self.head_pos) + (CELL_SIZE, CELL_SIZE))
        for tail in self.tail_pos:
            pygame.draw.rect(WINDOW, self.tail_colour, get_coordinates(tail) + (CELL_SIZE, CELL_SIZE))

class Apple:
    def __init__(self):
        self.apple_colour = (255,0,0)
        self.pos = (16,9)

    def draw(self):
        pygame.draw.rect(WINDOW, self.apple_colour, get_coordinates(self.pos) + (CELL_SIZE, CELL_SIZE))

    def eaten(self,snakie):
       if self.pos == snakie.head_pos:
            snakie.eat()
            self.pos = (random.randint(1,GRID_SIZE), random.randint(1,GRID_SIZE))


def get_input():
    global direction
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()
    keys = pygame.key.get_pressed()
    if keys[K_UP]:
        direction =( 0, -1)
    if keys[K_DOWN]:
        direction=(0, 1)
    if keys[K_LEFT]:
        direction=(-1, 0)
    if keys[K_RIGHT]:
        direction=(1, 0)


snake = Snake()
apple = Apple()
last_second_time = pygame.time.get_ticks()
direction = None

while True:
    get_input()

    current_time = pygame.time.get_ticks()

    if current_time - last_second_time >= 1000//speed_factor:

        WINDOW.fill(WINDOW_COLOUR)
        apple.draw()
        snake.draw()
        pygame.display.update()

        apple.eaten(snake)
        snake.turn(direction)
        if snake.check_over():
            quit()
        snake.move()

        last_second_time = current_time
