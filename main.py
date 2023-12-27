import pygame
from pygame.locals import *
from pygame.sprite import Sprite, Group

width = 500
height = 500

screen = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    screen.fill('pink')

    clock.tick(60)
    pygame.display.update()

pygame.quit()
