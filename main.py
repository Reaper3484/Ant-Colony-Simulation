import pygame
from pygame.locals import *
from pygame.sprite import Sprite, Group
import random
import math

width = 1200
height = 800
cell_size = 10
no_pheremone_color = 'white'
ant_size = 5
ant_color = 'red'
ant_speed = 4
ant_randomness = 20

screen = pygame.display.set_mode((width, height))


class Cell(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((cell_size, cell_size))
        self.image.fill(no_pheremone_color)
        self.rect = self.image.get_rect(topleft=(x, y))


class Ant(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((ant_size, ant_size))
        self.image.fill(ant_color)
        self.rect = self.image.get_rect(center=(500, 500))
        self.vector = [0, 0]

    def move(self):
        self.vector = normalize_vector((self.vector[0] + random.randint(-ant_randomness, ant_randomness)/100,
                                       self.vector[1] + random.randint(-ant_randomness, ant_randomness)/100))

        self.rect.move_ip(self.vector[0] * ant_speed, self.vector[1] * ant_speed)

    def update(self):
        self.move()


def normalize_vector(vector):
    magnitude = math.sqrt(sum(component ** 2 for component in vector))

    if magnitude != 0:
        normalized_vector = [component / magnitude for component in vector]
        return normalized_vector
    else:
        return vector


ant_group = Group()
ant = Ant()
ant_group.add(ant)

# Make grid
grid_group = Group()
for i in range(0, width, cell_size):
    for j in range(0, height, cell_size):
        cell = Cell(i, j)
        grid_group.add(cell)

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    screen.fill('pink')
    grid_group.draw(screen)
    ant_group.draw(screen)
    ant_group.update()

    clock.tick(60)
    pygame.display.update()

pygame.quit()
