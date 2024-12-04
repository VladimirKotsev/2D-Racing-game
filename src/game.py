# Example file showing a basic pygame "game loop"
import pygame
from constants import *

def movePlayers(keys):
    if keys[pygame.K_w]:
        player_pos1.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos1.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos1.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos1.x += 300 * dt

    if keys[pygame.K_UP]:
        player_pos2.y -= 300 * dt
    if keys[pygame.K_DOWN]:
        player_pos2.y += 300 * dt
    if keys[pygame.K_LEFT]:
        player_pos2.x -= 300 * dt
    if keys[pygame.K_RIGHT]:
        player_pos2.x += 300 * dt

# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
background = pygame.image.load(MAP).convert()
car = pygame.image.load(CAR).convert()

dt = 0

player_pos1 = pygame.Vector2(screen.get_width() - screen.get_width() / 4, screen.get_height() / 2)
player_pos2 = pygame.Vector2(screen.get_width() / 2 / 2, screen.get_height() / 2)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    #screen.fill("purple")

    pygame.draw.line(screen, BLACK, (MIDDLE_SEPARATOR, 0), (MIDDLE_SEPARATOR, SCREEN_HEIGHT), 10)

    screen.blit(car, (1, 0))
    screen.blit(car, (5, 0))
    screen.blit(background, player_pos1)
    screen.blit(background, player_pos2)

    pygame.draw.circle(screen, "red", player_pos1, 20)
    pygame.draw.circle(screen, "blue", player_pos2, 20)

    # moves players position on each input
    keys = pygame.key.get_pressed()
    movePlayers(keys)

    # flip() the display to put your work on screen
    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()