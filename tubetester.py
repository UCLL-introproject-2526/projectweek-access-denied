import pygame
import random
import sys

pygame.init()

# Scherm instellen
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wrench Levels")

# Kleuren
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (200, 0, 0)

# Basisvormen (vereenvoudigd als rechthoeken en polygonen)
def draw_wrench(x, y, with_teeth=False):
    # Hexagon (moer)
    hexagon = [(x, y), (x+40, y), (x+60, y+20),
               (x+40, y+40), (x, y+40), (x-20, y+20)]
    pygame.draw.polygon(screen, BLACK, hexagon, 2)

    # Wrench body
    pygame.draw.rect(screen, BLACK, (x-80, y+10, 60, 20), 2)

    # Tanden (dodelijk)
    if with_teeth:
        for i in range(5):
            pygame.draw.polygon(screen, RED, [
                (x+60+i*10, y+20),
                (x+65+i*10, y+10),
                (x+70+i*10, y+20)
            ])

# Game loop
clock = pygame.time.Clock()
running = True

# Startpositie
wrenches = [(WIDTH//2, HEIGHT//2, False)]

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Willekeurig een nieuwe wrench toevoegen
    if random.random() < 0.01:  # kans per frame
        with_teeth = random.choice([True, False])
        wrenches.append((WIDTH//2, HEIGHT//2 - len(wrenches)*60, with_teeth))

    # Teken alle wrenches
    for wx, wy, teeth in wrenches:
        draw_wrench(wx, wy, with_teeth=teeth)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
