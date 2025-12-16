import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 600, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Balloon Game - Menu")

clock = pygame.time.Clock()
font = pygame.font.SysFont("arialblack", 50)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def draw_text(text, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def menu():
    running = True

    while running:
        screen.fill(WHITE)

        draw_text("BALLOON GAME", BLACK, 100, 150)
        draw_text("START", BLACK, 220, 300)
        draw_text("QUIT", BLACK, 240, 380)

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        # START knop
        if 220 < mouse_pos[0] < 380 and 300 < mouse_pos[1] < 350:
            if mouse_click[0]:
                return "start"

        # QUIT knop
        if 240 < mouse_pos[0] < 360 and 380 < mouse_pos[1] < 430:
            if mouse_click[0]:
                pygame.quit()
                sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(60)
menu()