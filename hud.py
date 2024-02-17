import pygame
from settings import *


class HUD:
    """
    Represent the heads-up display (HUD) of the game,
    displaying player health, energy, and experience.

    Attributes:
    - display_surface: A Pygame surface representing
    the display window.
    - font: A Pygame font object for rendering text.
    - health_bar_rect: A Pygame Rect representing the
    bounding rectangle of the health bar.
    - energy_bar_rect: A Pygame Rect representing the
    bounding rectangle of the energy bar.

    Methods:
    - __init__(self): Initializes the HUD with the display
    surface and font.
    - show_bar(self, current, max_amount, bg_rect, color): 
    Displays a bar representing a resource (health or energy).
    - show_exp(self, exp): Displays the player's experience points.
    - display(self, player): Displays the HUD elements including health,
    energy, and experience.
    """
    def __init__(self):
        """
        Initialize the HUD with the display surface and font.
        """
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

    def show_bar(self, current, max_amount, bg_rect, color):
        """
        Display a bar representing a resource (health or energy).

        Parameters:
        - current: Current amount of the resource.
        - max_amount: Maximum amount of the resource.
        - bg_rect: Pygame Rect representing the bounding rectangle of the bar.
        - color: Color of the bar representing the resource.
        """
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        
    def show_exp(self, exp):
        """
        Display the player's experience points.

        Parameters:
        - exp: Integer representing the player's experience points.
        """
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright = (x,y))
        
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20,20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20,20), 3)

    def display(self, player):
        """
        Display the HUD elements including health, energy, and experience.

        Parameters:
        - player: Instance of the Player class representing the player character.
        """
        self.show_bar(player.health, player.stats["health"], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats["energy"], self.energy_bar_rect, ENERGY_COLOR)

        self.show_exp(player.exp)