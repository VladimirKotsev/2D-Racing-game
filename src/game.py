import os
import pygame
from constants import *

# Move players function: updates the player's world position
def move_players(keys, dt, player_pos1, player_pos2):
    speed = 300 * dt  # Movement speed factor

    # Player 1 movement
    if keys[pygame.K_w]:
        player_pos1.y -= speed
    if keys[pygame.K_s]:
        player_pos1.y += speed
    if keys[pygame.K_a]:
        player_pos1.x -= speed
    if keys[pygame.K_d]:
        player_pos1.x += speed

    # Player 2 movement
    if keys[pygame.K_UP] or keys[pygame.K_KP8]:
        player_pos2.y -= speed
    if keys[pygame.K_DOWN] or keys[pygame.K_KP5]:
        player_pos2.y += speed
    if keys[pygame.K_LEFT] or keys[pygame.K_KP4]:
        player_pos2.x -= speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_KP6]:
        player_pos2.x += speed

# Draw the portion of the map around the player
def draw_camera(screen, background, player_pos, zoom_level, offset_x, offset_y, screen_area):
    # Calculate the camera size (the zoomed area to display)
    camera_width = screen_area.width // zoom_level
    camera_height = screen_area.height // zoom_level

    # Define the top-left corner of the camera view so that the player is centered
    camera_x = int(player_pos.x - camera_width // 2)
    camera_y = int(player_pos.y - camera_height // 2)

    # Ensure the camera doesn't go outside the boundaries of the background
    if camera_x < 0:
        camera_x = 0
    if camera_y < 0:
        camera_y = 0

    if camera_x + camera_width > background.get_width():
        camera_width = background.get_width() - camera_x  # Adjust width to fit remaining area
    if camera_y + camera_height > background.get_height():
        camera_height = background.get_height() - camera_y  # Adjust height to fit remaining area

    # Get the visible part of the map (camera view)
    camera_rect = pygame.Rect(camera_x, camera_y, camera_width, camera_height)

    # Make sure we only subsurface within valid boundaries
    camera_view = background.subsurface(camera_rect)

    # Scale the camera view to fit the screen area
    scaled_view = pygame.transform.scale(camera_view, (screen_area.width, screen_area.height))

    # Draw the scaled map portion to the screen at the specified offset
    screen.blit(scaled_view, (offset_x, offset_y))

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

background = pygame.image.load(MAP).convert()
car_images = [pygame.image.load('../assets/images/car/' + img) for img in os.listdir('../assets/images/car')]
dt = 0

# Initial player positions (centered on the map)
player_pos1 = pygame.Vector2(background.get_width() / 2, background.get_height() / 2)
player_pos2 = pygame.Vector2(background.get_width() / 2 - 100, background.get_height() / 2 - 100)

# Screen areas for each player
player1_area = pygame.FRect(0, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT)  # Left half of the screen
player2_area = pygame.FRect(SCREEN_WIDTH // 2, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT)  # Right half of the screen

# Fixed positions where the players are always displayed on the screen
player1_screen_pos = (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)  # Player 1 in the center of the left half
player2_screen_pos = (3 * SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)  # Player 2 in the center of the right half

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the pressed keys and move players accordingly
    keys = pygame.key.get_pressed()
    move_players(keys, dt, player_pos1, player_pos2)

    # Fill the screen with black to clear the previous frame
    screen.fill(BLACK)

    # Draw the dividing line in the middle
    pygame.draw.line(screen, BLACK, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 10)

    # Draw the map with zoom around each player
    draw_camera(screen, background, player_pos1, ZOOM_LEVEL, 0, 0, player1_area)  # Player 1 on left side
    draw_camera(screen, background, player_pos2, ZOOM_LEVEL, SCREEN_WIDTH // 2, 0, player2_area)  # Player 2 on right side

    # Draw players on top of the zoomed map (they are fixed at a screen position)
    pygame.draw.circle(screen, "red", player1_screen_pos, 20)  # Player 1 on left side
    pygame.draw.circle(screen, "blue", player2_screen_pos, 20)  # Player 2 on right side
    print(player1_screen_pos)

    # Flip the display to update the screen
    pygame.display.flip()

    # Update the delta time
    dt = clock.tick(60) / 1000

pygame.quit()
