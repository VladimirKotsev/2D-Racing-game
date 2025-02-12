import sys

from physics import *

# Create player entity!
# Display player's name while playing

pygame.init()
from utils import *

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_icon(icon)
pygame.display.set_caption(GAME_NAME)

clock = pygame.time.Clock()

background = pygame.image.load(BACKGROUND_IMAGE_PATH).convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
background.set_alpha(10)

player1_input = TextInput(
    INPUT1_X,
    INPUT1_PLACEHOLDER
)

player2_input = TextInput(
    INPUT2_X,
    INPUT2_PLACEHOLDER
)

track = Track()

car1 = Car(track.p1_start[0], track.p1_start[1], track.angular_velocity, RED, {
    'up': pygame.K_w,
    'down': pygame.K_s,
    'left': pygame.K_a,
    'right': pygame.K_d
})
car2 = Car(track.p2_start[0], track.p2_start[1], track.angular_velocity, BLUE, {
    'up': pygame.K_KP8 or pygame.K_UP,
    'down': pygame.K_KP5 or pygame.K_DOWN,
    'left': pygame.K_KP4 or pygame.K_LEFT,
    'right': pygame.K_KP6 or pygame.K_RIGHT
})

# Create cameras
camera1 = Camera(car1.position.x, car1.position.y)
camera2 = Camera(car2.position.x, car2.position.y)

# Create POV's
player1_pov = pygame.Rect(0, 0, SPLIT_WIDTH, SCREEN_HEIGHT)
player2_pov = pygame.Rect(SPLIT_WIDTH, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

# Create button with image
play_button = Button(
    SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2,
    SCREEN_HEIGHT // 2 - BUTTON_HEIGHT // 2,
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
)

current_state = 1

while True:
    mouse_pos = pygame.mouse.get_pos()  # Get current mouse position

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if current_state == MENU:
            player1_input.handle_event(event)
            player2_input.handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_state == MENU and play_button.is_clicked(event.pos):
                current_state = COUNTDOWN  # Switch to countdown state
            if current_state == END_GAME:
                current_state = MENU
                car1.play_again(track.p1_start[0], track.p1_start[1], track.angular_velocity)
                car2.play_again(track.p2_start[0], track.p2_start[1], track.angular_velocity)
                pygame.display.update()

    if car1.is_winner:
        screen.fill(GRAY)
        screen.blit(background, (0, 0))
        draw_text(f"{str(player1_input)} is the winner!", game_font, GREEN, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.display.update()
        current_state = END_GAME
    if car2.is_winner:
        screen.fill(GRAY)
        screen.blit(background, (0, 0))
        draw_text(f"{str(player2_input)} is the winner!", game_font, GREEN, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.display.update()
        current_state = END_GAME

    if current_state == MENU:
        screen.blit(background, (0, 0))
        player1_input.draw(screen)
        player2_input.draw(screen)
        play_button.update(mouse_pos)  # Update button hover state
        play_button.draw(screen)
    elif current_state == COUNTDOWN:
        run_countdown(screen, background)
        current_state = GAME
    elif current_state == GAME:
        car1.check_collision(car2)

        car1.update(track.outer_bounds, track)
        car2.update(track.outer_bounds, track)
        camera1.update(car1.position.x - SPLIT_WIDTH / 2, car1.position.y - SCREEN_HEIGHT / 2)
        camera2.update(car2.position.x - SPLIT_WIDTH / 2, car2.position.y - SCREEN_HEIGHT / 2)

        track.draw(screen, camera1.position, player1_pov)
        car1.draw(screen, camera1.position, player1_pov)
        car2.draw(screen, camera1.position, player1_pov)
        track.draw(screen, camera2.position, player2_pov)
        car1.draw(screen, camera2.position, player2_pov)
        car2.draw(screen, camera2.position, player2_pov)

        screen.blit(text1, textRect1)
        screen.blit(text2, textRect2)

        pygame.draw.line(screen, BLACK, (SPLIT_WIDTH, 0), (SPLIT_WIDTH, SCREEN_HEIGHT), 2)
        pygame.display.flip()

        clock.tick(FPS)