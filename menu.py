import pygame, random
from buttons import Button
from settings import settings

# ----------------------------------
# INIT
# ----------------------------------
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

WIDTH, HEIGHT = 600, 720


def load_balloon_images():
    balloon_red = pygame.image.load("images/balloon_red.png").convert_alpha()
    balloon_blue = pygame.image.load("images/balloon_blue.png").convert_alpha()
    balloon_green = pygame.image.load("images/balloon_green.png").convert_alpha()
    balloon_purple = pygame.image.load("images/balloon_purple.png").convert_alpha()
    balloon_white = pygame.image.load("images/balloon_white.png").convert_alpha()

    balloons = [balloon_red, balloon_blue, balloon_green, balloon_purple, balloon_white]
    balloons = [pygame.transform.scale(b, (44, 100)) for b in balloons]

    return balloons


def menu(score=0, high_score=0):
    pygame.event.clear()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Balloon Game")

    clock = pygame.time.Clock()

    # ----------------------------------
    # MUSIC
    # ----------------------------------
    pygame.mixer.music.load("sound/menu_music.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)

    # ----------------------------------
    # ASSETS
    # ----------------------------------
    bgM = pygame.image.load("images/main_menu_screen.png")
    bgM = pygame.transform.scale(bgM, (WIDTH, HEIGHT))

    font = pygame.font.SysFont("terminal", 60)
    font_settings = pygame.font.SysFont("terminal", 30)
    font_score = pygame.font.SysFont("terminal", 40)

    balloons = load_balloon_images()

    # ----------------------------------
    # BALLOON SYSTEM
    # ----------------------------------
    active_balloons = []
    spawn_interval = 2000
    last_spawn_time = pygame.time.get_ticks()

    # ----------------------------------
    # BUTTONS
    # ----------------------------------
    play_btn = Button(
        150, 425, 300, 50, "PLAY", font,
        base_color=(240, 180, 0),
        text_color=(255, 255, 255),
        shadow_color=(30, 30, 30),
        text_shadow_color=(0, 0, 0)
    )

    quit_btn = Button(
        150, 500, 300, 50, "QUIT", font,
        base_color=(200, 200, 200),
        text_color=(0, 0, 0),
        shadow_color=(30, 30, 30),
        text_shadow_color=(200, 200, 200)
    )

    settings_icon = pygame.image.load("images/gear_icon.png").convert_alpha()
    settings_btn = Button(10, 670, 40, 40, "", font_settings, image=settings_icon)

    question_icon = pygame.image.load("images/question.png").convert_alpha()
    question_icon = pygame.transform.scale(question_icon, (40, 40))
    how_btn = Button(WIDTH - 50, HEIGHT - 50, 40, 40, "", font, image=question_icon)

    try:
        trophy_icon = pygame.image.load("images/trophy_icon.png").convert_alpha()
        trophy_icon = pygame.transform.scale(trophy_icon, (40, 40))
    except:
        trophy_icon = None

    # ----------------------------------
    # LOOP
    # ----------------------------------
    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                return "quit"

            if play_btn.is_clicked(event):
                pygame.mixer.music.stop()
                return "play"

            if settings_btn.is_clicked(event):
                pygame.mixer.music.stop()
                return "settings"

            if how_btn.is_clicked(event):
                pygame.mixer.music.stop()
                return "how"

            if quit_btn.is_clicked(event):
                pygame.mixer.music.stop()
                return "quit"

        screen.blit(bgM, (0, 0))

        # ----------------------------------
        # SCORES
        # ----------------------------------
        try:
            with open("high_score.txt", "r") as f:
                high_score = int(f.read())
        except:
            high_score = 0

        try:
            with open("last_score.txt", "r") as f:
                score = int(f.read())
        except:
            score = 0

        # ----------------------------------
        # BALLOONS
        # ----------------------------------
        now = pygame.time.get_ticks()
        if now - last_spawn_time >= spawn_interval:
            last_spawn_time = now
            img = random.choice(balloons)
            x = random.randint(20, WIDTH - 60)
            active_balloons.append({"img": img, "x": x, "y": HEIGHT})

        for balloon in active_balloons[:]:
            balloon["y"] -= 2
            screen.blit(balloon["img"], (balloon["x"], balloon["y"]))
            if balloon["y"] < -120:
                active_balloons.remove(balloon)

        # ----------------------------------
        # SCORE PANEL
        # ----------------------------------
        panel_rect = pygame.Rect((WIDTH - 350) // 2, 580, 350, 120)
        panel = pygame.Surface(panel_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(panel, (0, 0, 0, 120), panel.get_rect(), border_radius=12)
        screen.blit(panel, panel_rect.topleft)

        if score:
            txt = font_score.render(f"Last Score: {score}", True, (255, 255, 255))
            screen.blit(txt, txt.get_rect(center=(panel_rect.centerx, panel_rect.top + 33)))

        hs = font_score.render(f"High Score: {high_score}", True, (240, 180, 0))
        hs_rect = hs.get_rect(center=(panel_rect.centerx, panel_rect.top + 83))
        screen.blit(hs, hs_rect)

        if trophy_icon:
            trophy_rect = trophy_icon.get_rect(midright=(hs_rect.left - 10, hs_rect.centery))
            screen.blit(trophy_icon, trophy_rect)

        # ----------------------------------
        # DRAW BUTTONS
        # ----------------------------------
        play_btn.draw(screen)
        quit_btn.draw(screen)
        settings_btn.draw(screen)
        how_btn.draw(screen)

        pygame.display.flip()
