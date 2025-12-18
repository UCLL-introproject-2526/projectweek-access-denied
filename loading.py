import pygame
import random

WIDTH, HEIGHT = 600, 720
def loade():
    pygame.event.clear()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    # loading screen
    screen.fill((255, 255, 255))
    clock = pygame.time.Clock()
    pygame.event.clear()
    
    
    # L25
    L25 = pygame.image.load("images/main_menu_screen_bar_25.png")
    L25 = pygame.transform.scale(L25, (WIDTH, HEIGHT))
    screen.blit(L25, (0, 0))
    pygame.display.flip()
    pygame.time.wait(int(random.uniform(0.2, 0.5) * 1000))

    # L50
    L50 = pygame.image.load("images/main_menu_screen_bar_50.png")
    L50 = pygame.transform.scale(L50, (WIDTH, HEIGHT))
    screen.blit(L50, (0, 0))
    pygame.display.flip()
    pygame.time.wait(int(random.uniform(0.2, 1) * 1000))

    # L75
    L75 = pygame.image.load("images/main_menu_screen_bar_75.png")
    L75 = pygame.transform.scale(L75, (WIDTH, HEIGHT))
    screen.blit(L75, (0, 0))
    pygame.display.flip()
    pygame.time.wait(int(random.uniform(1, 3) * 1000))

    # L100
    L100 = pygame.image.load("images/main_menu_screen_bar_100.png")
    L100 = pygame.transform.scale(L100, (WIDTH, HEIGHT))
    screen.blit(L100, (0, 0))
    pygame.display.flip()
    pygame.time.wait(int(random.uniform(0.1, 0.2) * 1000))

    
    #end loading screen