import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            print("KEYDOWN detected!", event.key, event.unicode)
            if event.key == pygame.K_m:
                print("M pressed!")

pygame.quit()
