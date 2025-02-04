import pygame
import sys

# import all constants
from constants import *
from physics import Car

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("TurboNafta 3D")
clock = pygame.time.Clock()

car1 = Car(300, 300, RED, {
    'up': pygame.K_w,
    'down': pygame.K_s,
    'left': pygame.K_a,
    'right': pygame.K_d
})

car2 = Car(700, 300, BLUE, {
    'up': pygame.K_UP,
    'down': pygame.K_DOWN,
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT
})

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update
    car1.update()
    car2.update()

    # Draw
    screen.fill(WHITE)
    car1.draw(screen)
    car2.draw(screen)
    pygame.display.flip()

    clock.tick(FPS)
