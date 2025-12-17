# menu.py
import pygame
from buttons import Button

WIDTH, HEIGHT = 600, 720

def menu():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    bg = pygame.image.load("images/main_menu_screen.png").convert()
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    button_font = pygame.font.SysFont("arialblack", 30)
    settings_button_font = pygame.font.SysFont("arialblack", 10)

    start_button = Button(150, 500, 300, 60, "START", button_font)
    quit_button = Button(150, 580, 300, 60, "QUIT", button_font)
    settings_button = Button(10, 10, 100, 20, "SETTINGS", settings_button_font)

    while True:

        for event in pygame.event.get():
            if quit_button.is_clicked(event):
                return "quit"
            if start_button.is_clicked(event):
                return "play"
            if event.type == pygame.QUIT:
                return "quit"
            if settings_button.is_clicked(event):
                return "settings"

        screen.fill((255, 255, 255))
        screen.blit(bg, (0, 0))
        start_button.draw(screen)
        quit_button.draw(screen)
        settings_button.draw(screen)
        clock.tick(60)
        pygame.display.flip()
