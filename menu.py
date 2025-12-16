# menu.py
import pygame
from buttons import Button

WIDTH, HEIGHT = 600, 720
bg = pygame.image.load("images/achtergrond 1.png")

def menu():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    title_font = pygame.font.SysFont("arialblack", 50)
    button_font = pygame.font.SysFont("arialblack", 30)

    start_button = Button(150, 300, 300, 60, "START", button_font)
    quit_button = Button(150, 380, 300, 60, "QUIT", button_font)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if start_button.is_clicked(event):
                return "play"
            if quit_button.is_clicked(event):
                return "quit"

        screen.fill((255, 255, 255))
        screen.blit(bg, (0, 0))
        title = title_font.render("BALLOON GAME", True, (0, 0, 0))
        screen.blit(title, (100, 180))
        start_button.draw(screen)
        quit_button.draw(screen)
        pygame.display.flip()
        clock.tick(60)
