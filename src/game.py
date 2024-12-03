# Example file showing a basic pygame "game loop"
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

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
    screen.fill("purple")

    pygame.draw.circle(screen, "red", player_pos1, 40)
    pygame.draw.circle(screen, "red", player_pos2, 40)

    keys = pygame.key.get_pressed()
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

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()