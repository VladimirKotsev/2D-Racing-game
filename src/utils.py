import pygame
from constants import *

icon = pygame.image.load(WINDOW_ICON_PATH)
game_font = pygame.font.Font('freesansbold.ttf', 32)
menu_font = pygame.font.Font('freesansbold.ttf', 64)
text1 = game_font.render('Player1', True, GRAY)
text2 = game_font.render('Player2', True, GRAY)

textRect1 = text1.get_rect()
textRect2 = text2.get_rect()
textRect1.center = (100, 50)
textRect2.center = (SCREEN_WIDTH // 2 + 100, 50)


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


class Button:
    def __init__(self, x, y, width, height, text, image_path=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.image = None
        self.hover_image = None

        if image_path:
            # Load the normal and hover images
            try:
                # Load and scale the original image
                original_image = pygame.image.load(image_path)
                self.image = pygame.transform.scale(original_image, (width, height))

                # Create a slightly brighter version for hover effect
                hover_image = original_image.copy()
                hover_surface = pygame.Surface((width, height), pygame.SRCALPHA)
                hover_surface.fill((255, 255, 255, 50))  # Semi-transparent white
                hover_image.blit(hover_surface, (0, 0))
                self.hover_image = pygame.transform.scale(hover_image, (width, height))
            except pygame.error:
                print(f"Could not load button image: {image_path}")
                self.image = None
                self.hover_image = None

        self.is_hovered = False

    def draw(self, surface):
        if self.image:
            # Draw the appropriate image based on hover state
            current_image = self.hover_image if self.is_hovered else self.image
            surface.blit(current_image, self.rect)

            # Draw text on top of the image if needed
            if self.text:
                draw_text(self.text, menu_font, BLUE, surface,
                          self.rect.centerx, self.rect.centery)
        else:
            # Fallback to original rectangle drawing if image loading failed
            pygame.draw.rect(surface, GREEN, self.rect)
            if self.text:
                draw_text(self.text, menu_font, BLUE, surface,
                          self.rect.centerx, self.rect.centery)

        pygame.display.flip()

    def update(self, mouse_pos):
        # Update hover state
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)