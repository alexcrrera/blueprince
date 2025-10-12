import pygame
from src import params

class handleBackground:
    """
    Création de la base de l'interface

    """

    def __init__(self, surface: pygame.Surface):
        """Initialisation"""
        self.surface = surface
        self.leftColor = params.BLACK
        self.rightColor = params.WHITE
        self.splitRatio = params.splitRatioScreen  # 33%

    def draw(self):
        """
        Crée le fond de l'interface
        - Gauche 33%: noir
        - Doite 67%: blanc"""
        width, height = self.surface.get_size()
        leftWidth = int(width * self.splitRatio)

        pygame.draw.rect(self.surface, self.leftColor, (0, 0, leftWidth, height))
        pygame.draw.rect(self.surface, self.rightColor, (leftWidth, 0, width - leftWidth, height))