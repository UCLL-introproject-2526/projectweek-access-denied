import pygame
import sys
from buttons import Button

pygame.init()

# ---------------- WINDOW ----------------
WIDTH, HEIGHT = 600, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Balloon Game")

clock = pygame.time.Clock()

# ---------------- FONTS ----------------
title_font = pygame.font.SysFont("arialblack", 50)
button_font = pygame.font.SysFont("arialblack", 30)

# ---------------- COLORS ----------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# ---------------- BACKGROUNDS ----------------
MENU_BG = pygame.image.load("achtergrond_1.jpg").convert()
MENU_BG = pygame.transform.scale(MENU_BG, (WIDTH, HEIGHT))

GAME_BG = pygame.image.load("achtergrond_1.jpg").convert()
GAME_BG = pygame.transform.scale(GAME_BG, (WIDTH, HEIGHT))

# ---------------- TEXT ----------------
def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# ---------------- BUTTONS ----------------
start_button = Button(150, 300, 300, 60, "START", button_font)
quit_button = Button(150, 380, 300, 60, "QUIT", button_font)

resume_button = Button(150, 300, 300, 60, "RESUME", button_font)
pause_quit_button = Button(150, 380, 300, 60, "QUIT", button_font)

restart_button = Button(150, 300, 300, 60, "RESTART", button_font)
gameover_quit_button = Button(150, 380, 300, 60, "QUIT", button_font)

# ---------------- GAME STATES ----------------
MENU = 0
GAME = 1
PAUSE = 2
GAME_OVER = 3

game_state = MENU

# ---------------- MAIN LOOP ----------------
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # -------- MENU --------
        if game_state == MENU:
            if start_button.is_clicked(event):
                game_state = GAME
            elif quit_button.is_clicked(event):
                running = False

        # -------- GAME --------
        elif game_state == GAME:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = PAUSE

            # ⚠️ SIMULATIE: druk op D = dood
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    game_state = GAME_OVER

        # -------- PAUSE --------
        elif game_state == PAUSE:
            if resume_button.is_clicked(event):
                game_state = GAME
            elif pause_quit_button.is_clicked(event):
                game_state = MENU

        # -------- GAME OVER --------
        elif game_state == GAME_OVER:
            if restart_button.is_clicked(event):
                game_state = GAME
            elif gameover_quit_button.is_clicked(event):
                game_state = MENU

    # ---------------- DRAW ----------------
    if game_state == MENU:
        screen.blit(MENU_BG, (0, 0))
        draw_text("BALLOON GAME", title_font, BLACK, 100, 180)
        start_button.draw(screen)
        quit_button.draw(screen)

    elif game_state == GAME:
        screen.blit(GAME_BG, (0, 0))
        draw_text("GAME RUNNING", title_font, BLACK, 120, 300)
        draw_text("ESC = pause | D = game over", button_font, BLACK, 80, 360)

    elif game_state == PAUSE:
        screen.blit(GAME_BG, (0, 0))
        draw_text("PAUSED", title_font, BLACK, 200, 180)
        resume_button.draw(screen)
        pause_quit_button.draw(screen)

    elif game_state == GAME_OVER:
        screen.blit(MENU_BG, (0, 0))
        draw_text("GAME OVER", title_font, (200, 0, 0), 160, 180)
        restart_button.draw(screen)
        gameover_quit_button.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
