import sys
import pygame

from physics import Track, Car, Player
from constants import *

pygame.init()
from menu import Menu
from utils import icon, draw_text, game_font

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_icon(icon)
pygame.display.set_caption(GAME_NAME)

clock = pygame.time.Clock()

menu = Menu()

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

# Create POV's
player1_pov = pygame.Rect(0, 0, SPLIT_WIDTH, SCREEN_HEIGHT)
player2_pov = pygame.Rect(SPLIT_WIDTH, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

player1_name, player2_name = menu.get_player_names()
player1 = Player(player1_name, car1, player1_pov)
player2 = Player(player2_name, car2, player2_pov)

current_state = 1

while True:
    mouse_pos = pygame.mouse.get_pos()  # Get current mouse position
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if current_state == MENU:
            if menu.handle_events(event):
                # Play button is clicked
                current_state = COUNTDOWN
        elif event.type == pygame.MOUSEBUTTONDOWN and current_state == END_GAME:
            current_state = MENU
            player1.rematch()
            player2.rematch()
            pygame.display.update()

    if player1.is_winner():
        menu.display_winner(screen, player1)
        current_state = END_GAME
    if player2.is_winner():
        menu.display_winner(screen, player2)
        current_state = END_GAME

    if current_state == MENU:
        menu.update(mouse_pos)
        menu.draw(screen)
    elif current_state == COUNTDOWN:
        menu.run_countdown(screen)
        current_state = GAME
        player1.nickname, player2.nickname = menu.get_player_names()
    elif current_state == GAME:
        player1.check_collision(player2)

        player1.update(track)
        player2.update(track)

        track.draw(screen, player1.camera.position, player1_pov)
        player1.draw(screen, car2)
        track.draw(screen, player2.camera.position, player2_pov)
        player2.draw(screen, car1)

        draw_text(f"{str(player1)}", game_font, GRAY, screen, *GAME_NAME_1_POS)
        draw_text(f"{str(player2)}", game_font, GRAY, screen, *GAME_NAME_2_POS)

        pygame.draw.line(screen, BLACK, (SPLIT_WIDTH, 0), (SPLIT_WIDTH, SCREEN_HEIGHT), 2)
        pygame.display.flip()

        clock.tick(FPS)