import pygame
from constants import *

icon = pygame.image.load(WINDOW_ICON_PATH)
font = pygame.font.Font('freesansbold.ttf', 32)
text1 = font.render('Player1', True, GRAY)
text2 = font.render('Player2', True, GRAY)

textRect1 = text1.get_rect()
textRect2 = text2.get_rect()
textRect1.center = (100, 50)
textRect2.center = (SCREEN_WIDTH // 2 + 100, 50)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def draw(self, surface):
        pygame.draw.rect(surface, GREEN, self.rect)
        draw_text(self.text, font, BLUE, surface, self.rect.centerx, self.rect.centery)
        pygame.display.flip()

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
