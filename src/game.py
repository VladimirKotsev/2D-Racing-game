import pygame
import sys

# import all constants
from constants import *
from physics import *

pygame.init()

icon = pygame.image.load(WINDOW_ICON_PATH)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_icon(icon)
pygame.display.set_caption("TurboNafta 3D")
clock = pygame.time.Clock()

car1 = Car(300, 300, RED, {
    'up': pygame.K_w,
    'down': pygame.K_s,
    'left': pygame.K_a,
    'right': pygame.K_d
})

car2 = Car(850, 300, BLUE, {
    'up': pygame.K_KP8 or pygame.K_UP,
    'down': pygame.K_KP5 or pygame.K_DOWN,
    'left': pygame.K_KP4 or pygame.K_LEFT,
    'right': pygame.K_KP6 or pygame.K_RIGHT
})

track = Track()

# Create cameras
camera1 = Camera(car1.position.x, car1.position.y)
camera2 = Camera(car2.position.x, car2.position.y)

# Create POV's
player1_pov = pygame.Rect(0, 0, SPLIT_WIDTH, SCREEN_HEIGHT)
player2_pov = pygame.Rect(SPLIT_WIDTH, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update
    car1.update()
    car2.update()
    camera1.update(car1.position.x - SPLIT_WIDTH / 2, car1.position.y - SCREEN_HEIGHT / 2)
    camera2.update(car2.position.x - SPLIT_WIDTH / 2, car2.position.y - SCREEN_HEIGHT / 2)

    # Draw
    screen.fill(WHITE)
    car1.draw(screen)
    car2.draw(screen)

    track.draw(screen, camera1.position, player1_pov)
    car1.draw(screen, camera1.position, player1_pov)
    car2.draw(screen, camera1.position, player1_pov)

    track.draw(screen, camera2.position, player2_pov)
    car1.draw(screen, camera2.position, player2_pov)
    car2.draw(screen, camera2.position, player2_pov)

    pygame.draw.line(screen, BLACK, (SPLIT_WIDTH, 0), (SPLIT_WIDTH, SCREEN_HEIGHT), 2)
    pygame.display.flip()

    clock.tick(FPS)
