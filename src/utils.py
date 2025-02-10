import pygame
from constants import *

icon = pygame.image.load(WINDOW_ICON_PATH)
game_font = pygame.font.Font('freesansbold.ttf', 32)
menu_font = pygame.font.Font('freesansbold.ttf', 144)
text1 = game_font.render('Player1', True, GRAY)
text2 = game_font.render('Player2', True, GRAY)

textRect1 = text1.get_rect()
textRect2 = text2.get_rect()
textRect1.center = (100, 50)
textRect2.center = (SCREEN_WIDTH // 2 + 100, 50)

def draw_text(text, font, color, surface, x, y):
    """Draw text on screen."""
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def draw_rounded_rect(surface, rect, color, corner_radius):
    """Draw a rectangle with rounded corners"""
    if corner_radius < 0:
        corner_radius = 0

    rect_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)

    pygame.draw.rect(rect_surface, color, (0, 0, rect.width, rect.height), border_radius=corner_radius)
    surface.blit(rect_surface, rect)
    return rect_surface


class Button:
    """Represent a clickable button."""

    def __init__(self, x, y, width, height):
        """Create a new instance of button."""
        self.rect = pygame.Rect(x, y, width, height)
        self.corner_radius = BUTTON_BORDER_RADIUS

        original_image = pygame.image.load(BUTTON_IMAGE_PATH)
        base_surface = pygame.Surface((width, height), pygame.SRCALPHA)

        mask_surface = draw_rounded_rect(base_surface, pygame.Rect(0, 0, width, height),
                                         WHITE, self.corner_radius)

        scaled_image = pygame.transform.scale(original_image, (width, height))

        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.blit(scaled_image, (0, 0))

        self.image.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

        hover_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        draw_rounded_rect(hover_surface, pygame.Rect(0, 0, width, height),
                          WHITE_TRANSPARENT, self.corner_radius)

        self.hover_image = self.image.copy()
        self.hover_image.blit(hover_surface, (0, 0))

        self.is_hovered = False

    def draw(self, surface):
        """Draw button on screen."""
        current_image = self.hover_image if self.is_hovered else self.image
        surface.blit(current_image, self.rect)

        pygame.display.flip()

    def update(self, mouse_pos):
        """Update button if mouse on hover."""
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos):
        """Return if button is clicked."""
        return self.rect.collidepoint(mouse_pos)
