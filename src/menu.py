import pygame
import time

from constants import *
from utils import TextInput, Button, game_font, draw_text, menu_font

class Menu:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Menu, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize menu components."""
        self.background = pygame.image.load(BACKGROUND_IMAGE_PATH).convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.set_alpha(10)

        self.player1_input = TextInput(INPUT1_X, INPUT1_PLACEHOLDER)
        self.player2_input = TextInput(INPUT2_X, INPUT2_PLACEHOLDER)

        self.play_button = Button(
            SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2,
            SCREEN_HEIGHT // 2 - BUTTON_HEIGHT // 2,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
        )

    def handle_events(self, event):
            self.player1_input.handle_event(event)
            self.player2_input.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button.is_clicked(event.pos):
                    return True
            return False

    def display_winner(self, screen, background, player):
        screen.fill(GRAY)
        screen.blit(background, (0, 0))
        draw_text(f"{player} is the winner!", game_font, GREEN, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.display.update()

    def update(self, mouse_pos):
        """Update menu state."""
        self.play_button.update(mouse_pos)

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        self.player1_input.draw(screen)
        self.player2_input.draw(screen)
        self.play_button.draw(screen)

    def get_player_names(self):
        """Get player names from input fields."""
        return str(self.player1_input), str(self.player2_input)

    def run_countdown(self, screen):
        """Run countdown animation."""
        for i in range(3, 0, -1):
            screen.fill(GRAY)
            screen.blit(self.background, (0, 0))
            draw_text(str(i), menu_font, GREEN, screen,
                     SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            pygame.display.update()
            time.sleep(1)

        screen.fill(GRAY)
        screen.blit(self.background, (0, 0))
        draw_text("Go!", menu_font, GREEN, screen,
                 SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.display.update()
        time.sleep(1)