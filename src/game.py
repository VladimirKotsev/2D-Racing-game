import pygame
import sys

# Initialize Pygame
pygame.init()

track_image = pygame.image.load('../assets/images/Test_track.jpg')

pygame.mixer.init()

screen_width = 1000
screen_height = 650
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Turbo Nafta")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

car_width = 50
car_height = 50

car_x = 375
car_y = 275

crash_sound = pygame.mixer.Sound('../assets/sounds/crash_sound.wav')
#off_track_sound = pygame.mixer.Sound('./assets/sounds/off_track_sound.wav')

clock = pygame.time.Clock()

running = True

# Track boundaries
track_left = 0
track_right = screen_width
track_top = 0
track_bottom = screen_height

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Clear the screen
        screen.fill((0, 0, 0))
        # Draw the racing track
        screen.blit(track_image, (0, 0))  # (0, 0) is the top-left corner of the screen
        # Update the display
        pygame.display.flip()
        # Cap the frame rate to 60 FPS
        clock.tick(60)

    # Check if the car goes outside the track
    if car_x < track_left or car_x + car_width > track_right or car_y < track_top or car_y + car_height > track_bottom:
        #off_track_sound.play()  # Play off-track sound
        print("Car went off track!")
        car_x = 375  # Reset car position (example)
        car_y = 275

    # Simulate a car crash (e.g., check for collisions with other objects or boundaries)
    if car_x > screen_width // 2 - car_width // 2 and car_x < screen_width // 2 + car_width // 2 and car_y > screen_height // 2 - car_height // 2 and car_y < screen_height // 2 + car_height // 2:
        crash_sound.play()  # Play crash sound
        print("Car crashed!")
        car_x = 375  # Reset car position (example)
        car_y = 275

    # Handle keys to move car (for demo purposes)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        car_x -= 5
    if keys[pygame.K_RIGHT]:
        car_x += 5
    if keys[pygame.K_UP]:
        car_y -= 5
    if keys[pygame.K_DOWN]:
        car_y += 5

    # Fill screen with white
    screen.fill(WHITE)

    # Draw car (red rectangle)
    pygame.draw.rect(screen, RED, (car_x, car_y, car_width, car_height))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
