import sys
import time

from physics import *
pygame.init()
from utils import *

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_icon(icon)
pygame.display.set_caption(GAME_NAME)

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

#track_img = pygame.image.load('../assets/images/map/Austria.png')
track = Track()

# Create cameras
camera1 = Camera(car1.position.x, car1.position.y)
camera2 = Camera(car2.position.x, car2.position.y)

# Create POV's
player1_pov = pygame.Rect(0, 0, SPLIT_WIDTH, SCREEN_HEIGHT)
player2_pov = pygame.Rect(SPLIT_WIDTH, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

play_button = Button(SCREEN_WIDTH // 2 - 180 // 2, SCREEN_HEIGHT // 2 - 90 // 2, 180, 90, 'Play')

current_state = 1

def run_countdown():
    for i in range(3, 0, -1):
        screen.fill(GRAY)
        draw_text(str(i), menu_font,  GREEN, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.display.update()
        time.sleep(1)

    screen.fill(GRAY)
    draw_text("Go!", menu_font, GREEN, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    pygame.display.update()
    time.sleep(1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_state == MENU and play_button.is_clicked(event.pos):
                current_state = COUNTDOWN  # Switch to countdown state

    if current_state == MENU:
        screen.fill(GRAY)
        play_button.draw(screen)
    elif current_state == COUNTDOWN:
        # Run the countdown and then proceed to the game
        run_countdown()
        current_state = GAME  # After countdown, go to the game state
    elif current_state == GAME:
        car1.update(track.outer_bounds, track)
        car2.update(track.outer_bounds, track)
        car1.check_collision(car2)
        camera1.update(car1.position.x - SPLIT_WIDTH / 2, car1.position.y - SCREEN_HEIGHT / 2)
        camera2.update(car2.position.x - SPLIT_WIDTH / 2, car2.position.y - SCREEN_HEIGHT / 2)

        #screen.fill(BLACK)

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
