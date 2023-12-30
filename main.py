import pygame
from pygame.locals import *
from pygame.sprite import Sprite, Group
import random
import math

width = 800
height = 800
cell_size = 10
no_pheremone_color = 'white'
no_of_ants = 50
ant_size = 3
ant_color = 'red'
ant_speed = 5
ant_randomness = 20
ant_hill_size = 50

pheromone_decay_strength = 0.9

screen = pygame.display.set_mode((width, height))


class Cell(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((cell_size, cell_size))
        self.image.fill(no_pheremone_color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.search_pheromone = 0
        self.food_pheromone = 0
        
    def display_pheromone(self):
        if self.search_pheromone >= 255:
            self.search_pheromone = 255
        if self.food_pheromone >= 255:
            self.food_pheromone = 255

        if self.search_pheromone <= 0:
            self.search_pheromone = 0

        if self.search_pheromone > self.food_pheromone:
            self.image.fill((0, 0, self.search_pheromone))
        else:
            self.image.fill((0, self.food_pheromone, 0))
        
        self.search_pheromone -= pheromone_decay_strength
        
    def update(self):
       self.display_pheromone() 


class Ant(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((ant_size, ant_size))
        self.image.fill(ant_color)
        self.rect = self.image.get_rect(center=(500, 500))
        self.vector = [0, 0]
        self.search_pheromone = True

    def move(self):
        self.vector = normalize_vector((self.vector[0] + random.randint(-ant_randomness, ant_randomness)/100,
                                       self.vector[1] + random.randint(-ant_randomness, ant_randomness)/100))

        prev_pos = self.rect.center 
        self.rect.move_ip(self.vector[0] * ant_speed, self.vector[1] * ant_speed)

        if self.rect.collidedict(obstacle_group.spritedict):
            self.rect.center = prev_pos
            self.vector = [self.vector[0] * -1, self.vector[1] * -1]

    def pheremone_releaser(self):
        cell = self.rect.collidedict(grid_group.spritedict)[0]
        if self.search_pheromone:
            cell.search_pheromone += 100
        else:
            cell.food_pheromone += 255 

    def update(self):
        self.move()
        # self.pheremone_releaser()


class AntHill(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((ant_hill_size, ant_hill_size))
        self.image.fill((255, 95, 64))
        self.rect = self.image.get_rect(center = (500, 500))


class Obstacle(Sprite):
    def __init__(self, size, topleft_coord):
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill('brown')
        self.rect = self.image.get_rect(topleft=topleft_coord)


def pheremone_releaser():
    data = pygame.sprite.groupcollide(grid_group, ant_group, False, False)
    for cell, ants in data.items():
        for ant in ants:
            if ant.search_pheromone:
                cell.search_pheromone += 100
            

def normalize_vector(vector):
    magnitude = math.sqrt(sum(component ** 2 for component in vector))

    if magnitude != 0:
        normalized_vector = [component / magnitude for component in vector]
        return normalized_vector
    else:
        return vector


# Make grid
grid_group = Group()
for i in range(0, width, cell_size):
    for j in range(0, height, cell_size):
        cell = Cell(i, j)
        grid_group.add(cell)

# Add obstacles
obstacle_group = Group()
top_obs = Obstacle((width, ant_size+1), (0, -ant_size-1))
bottom_obs = Obstacle((width, ant_size+1), (0, height))
left_obs = Obstacle((ant_size+1, height), (-ant_size-1, 0))
right_obs = Obstacle((ant_size+1, height), (width, 0))
obstacle_group.add(top_obs, bottom_obs, left_obs, right_obs)

# Add ants
ant_group = Group()
for _ in range(no_of_ants):
    ant = Ant()
    ant_group.add(ant)
ant_hill_group = Group()    
ant_hill_group.add(AntHill())

clock = pygame.time.Clock()
running = True
ticks = 0

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    screen.fill('pink')
    grid_group.draw(screen)
    grid_group.update()
    obstacle_group.draw(screen)
    ant_group.draw(screen)
    ant_group.update()
    ant_hill_group.draw(screen)

    if ticks > 1:
        pheremone_releaser()
        ticks = 0

    ticks += 1
    clock.tick(60)
    pygame.display.update()

pygame.quit()
