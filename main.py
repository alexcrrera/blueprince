import pygame
import sys
import os
import time

# Constants
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 60
BG_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)
FONT_SIZE = 30
PADDING = 20
SMALL_FONT_SIZE = 10


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)
        pygame.display.set_caption("Blue Prince Emulation")
        self.clock = pygame.time.Clock()
        self.running = True

        # Load fonts (must be in the same folder)
        self.default_font = pygame.font.Font("assets/fonts/Helvetica.ttf", FONT_SIZE)  # general text

        self.special_font = pygame.font.Font("assets/fonts/damnarc.ttf", FONT_SIZE + 10)  # specific text
        self.small_font = pygame.font.Font("assets/fonts/Helvetica.ttf", SMALL_FONT_SIZE)  # smaller text
        # Placeholder texts
        self.left_text = "Left info"
        self.right_text = "Right info"
        self.special_text = "Day One"


    def draw_text(self, text, position, font=None, color=TEXT_COLOR):
        """Draw text with optional font and color."""
        font = font or self.default_font
        rendered_text = font.render(text, True, color)
        self.screen.blit(rendered_text, position)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        # Placeholder for updating game logic
        pass

    def draw(self):
        self.screen.fill(BG_COLOR)
        # Bottom-left
        self.draw_text(self.left_text, (PADDING, SCREEN_HEIGHT - FONT_SIZE - PADDING))
        # Bottom-right
        right_pos = (SCREEN_WIDTH - PADDING - self.default_font.size(self.right_text)[0], SCREEN_HEIGHT - FONT_SIZE - PADDING)
        self.draw_text(self.right_text, right_pos)
        # Example of special text in a custom font at top-left
        self.draw_text(self.special_text, (PADDING, PADDING), font=self.special_font, color=(255, 200, 0))
        fps_text = f"FPS: {int(self.clock.get_fps())}"
        self.draw_text(fps_text, (SCREEN_WIDTH//2 - PADDING -  self.small_font.size(fps_text)[0], SCREEN_HEIGHT - PADDING),font=self.small_font)

        pygame.display.flip()





    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
       

            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    time.sleep(1)
    sys.exit()
