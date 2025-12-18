import pygame
from buttons import Button

WIDTH, HEIGHT = 600, 720

def menu(score=0, high_score=0):
    pygame.event.clear()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    bgM = pygame.image.load("images/main_menu_screen.png")
    bgM = pygame.transform.scale(bgM, (WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("terminal", 60)
    font_settings = pygame.font.SysFont("terminal", 30)
    font_score = pygame.font.SysFont("terminal", 40)

    # Buttons
    play_btn = Button(
        150, 425, 300, 50, "PLAY", font,
        base_color=(240, 180, 0),
        text_color=(255, 255, 255),
        shadow_color=(30, 30, 30),
        text_shadow_color=(0, 0, 0)
    )

    # Settings button as image (gear icon)
    settings_icon = pygame.image.load("images/gear_icon.png").convert_alpha()
    settings_btn = Button(
        10, 670, 40, 40, "", font_settings,
        image=settings_icon
    )

    quit_btn = Button(
        150, 500, 300, 50, "QUIT", font,
        base_color=(200, 200, 200),
        text_color=(0, 0, 0),
        shadow_color=(30, 30, 30),
        text_shadow_color=(200, 200, 200)
    )

    # Optional trophy icon for high score
    try:
        trophy_icon = pygame.image.load("images/trophy_icon.png").convert_alpha()
        trophy_icon = pygame.transform.scale(trophy_icon, (40, 40))
    except Exception:
        trophy_icon = None

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if play_btn.is_clicked(event):
                return "play"

            if settings_btn.is_clicked(event):
                return "settings"

            if quit_btn.is_clicked(event):
                return "quit"

        screen.fill((240, 240, 240))
        screen.blit(bgM, (0, 0))

        # Read high score from file
        try:
            with open("high_score.txt", "r") as f:
                high_score = int(f.read())
        except Exception:
            high_score = 0

        try:
            with open("last_score.txt", "r") as f:
                score = int(f.read())
        except Exception:
            score = 0

        # --- Centered Score Panel ---
        panel_width, panel_height = 350, 120
        panel_x = (WIDTH - panel_width) // 2   # center horizontally
        panel_y = 580
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)

        panel_surface = pygame.Surface(panel_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(panel_surface, (0, 0, 0, 120), panel_surface.get_rect(), border_radius=12)
        screen.blit(panel_surface, panel_rect.topleft)

        # --- Last score (centered inside panel) ---
        if score:
            score_text = font_score.render(f"Last Score: {score}", True, (255, 255, 255))
            shadow = font_score.render(f"Last Score: {score}", True, (0, 0, 0))
            score_rect = score_text.get_rect(center=(panel_rect.centerx, panel_rect.top + 33))
            shadow_rect = shadow.get_rect(center=(panel_rect.centerx, panel_rect.top + 35))
            screen.blit(shadow, shadow_rect)
            screen.blit(score_text, score_rect)

        # --- High score (centered inside panel) ---
        hs_text = font_score.render(f"High Score: {high_score}", True, (240, 180, 0))  # gold
        shadow = font_score.render(f"High Score: {high_score}", True, (0, 0, 0))
        hs_text_rect = hs_text.get_rect(center=(panel_rect.centerx, panel_rect.top + 83))
        hs_shadow_rect = shadow.get_rect(center=(panel_rect.centerx, panel_rect.top + 85))
        screen.blit(shadow, hs_shadow_rect)
        screen.blit(hs_text, hs_text_rect)

        # Trophy icon next to high score (relative to text position)
        if trophy_icon:
            trophy_rect = trophy_icon.get_rect()
            trophy_rect.midright = (hs_text_rect.left - 10, hs_text_rect.centery)
            screen.blit(trophy_icon, trophy_rect)

        # Draw buttons
        play_btn.draw(screen)
        settings_btn.draw(screen)
        quit_btn.draw(screen)

        pygame.display.flip()
