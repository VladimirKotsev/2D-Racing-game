import pygame
import sys

# import all constants
from constants import *

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("TurboNafta 3D")
clock = pygame.time.Clock()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    # Draw
    screen.fill(WHITE)
    pygame.display.flip()

    clock.tick(FPS)
