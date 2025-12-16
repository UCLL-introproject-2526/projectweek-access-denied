# game.py
import pygame
from pygame import mixer

WIDTH, HEIGHT = 600, 720

def main_game():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    background = pygame.image.load("images/achtergrond 1.jpg").convert()

    mixer.music.load("sound/Floating-Dreams.mp3")
    mixer.music.play(-1)

    balloon = pygame.Surface((40, 60), pygame.SRCALPHA)
    pygame.draw.ellipse(balloon, (255, 0, 0), balloon.get_rect())

    x, y = WIDTH // 2, HEIGHT - 150
    speed = 4

    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mixer.music.stop()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                mixer.music.stop()
                return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            x -= speed
        if keys[pygame.K_RIGHT]:
            x += speed

        x = max(0, min(WIDTH - balloon.get_width(), x))

        screen.blit(background, (0, 0))
        screen.blit(balloon, (x, y))
        pygame.display.flip()
