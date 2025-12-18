import pygame
import random


def load_assets(screen_size=(600, 720)):
    """Load game assets with safe fallbacks and return an assets dict.
    This loader avoids calling convert/convert_alpha so it can be used before a
    display mode is set. Conversion is done later inside `main_game` after
    setting the video mode.
    """
    w, h = screen_size
    assets = {}

    def _load(p, size=None, alpha=True, fallback_color=(100, 100, 100, 255)):
        try:
            img = pygame.image.load(p)
            if size:
                img = pygame.transform.scale(img, size)
            return img
        except (FileNotFoundError, pygame.error) as e:
            print(f"Warning: failed to load {p}: {e}")
            if size is None:
                size = (w, h)
            surf = pygame.Surface(size, pygame.SRCALPHA)
            surf.fill(fallback_color)
            return surf
        
    backgrounds = ["images/sky.png", "images/dungeon.png"]

    assets["background"] = _load(backgrounds[1], (w, h))
    assets["sky_background"] = _load(backgrounds[0], (w, h))

    fig_paths = [
        "images/corridor_right_spiked.png",
        "images/corridor_right.png",
        "images/corridor_left_2.png",
        "images/drie_eilanden_links.png",
        "images/drie_eilanden_rechts.png",
        "images/mini_eilanden_left_2.png",
        "images/mini_eilanden_right_2.png",
        "images/eilanden_right.png",
        "images/eilanden_left.png",
        "images/cube_spike.png",
        "images/cube_spike_left.png",
        "images/cube_spike_right.png",
        "images/cube_spike_right.png",
        "images/six_seven_corridor.png"
    ]
    assets["fig_images"] = [_load(p, (600, 700)) for p in fig_paths]

    # Tubes & balloons
    assets["tube"] = _load("images/straight_tube_texture.png", (600, 700))
    assets["balloon"] = _load("images/balloon.png")
    assets["blue_balloon"] = _load("images/blue_balloon.png", fallback_color=(255,255,255,255))
    assets["green_balloon"] = _load("images/green_balloon.png", fallback_color=(255,255,255,255))
    assets["purple_balloon"] = _load("images/purple_balloon.png", fallback_color=(255,255,255,255))
    assets["white_balloon"] = _load("images/white_balloon.png", fallback_color=(255,255,255,255))
    assets["balloon_prepop"] = _load("images/balloon_prepop.png")
    assets["balloon_pop"] = _load("images/balloon_pop.png")
    assets["death_screen"] = _load("images/death_screen.png", (w, h), alpha=False)

    # optional assets
    try:
        assets["hat"] = pygame.image.load("images/kerstmuts.png")
    except Exception:
        assets["hat"] = None

    assets["game_music"] = "sound/Floating-Dreams.mp3"
    return assets


def main_game(balloon_skin="normal", high_score=0, assets=None, music_on=True, sfx_on=True):
    paused = False
    screen_size = (600, 720)
    center_x = screen_size[0] // 2
    center_y = screen_size[1] // 2
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()

    # Gebruik assets loader als er geen zijn meegegeven
    if assets is None:
        assets = load_assets(screen_size)

    # Na display kan convert / convert_alpha veilig
    for key in ("background", "sky_background", "tube", "balloon", 
                "blue balloon", "green balloon", "purple balloon", "white balloon",
                "balloon_prepop", "balloon_pop", "death_screen"):
        try:
            if key in assets:
                assets[key] = assets[key].convert_alpha()
        except Exception:
            pass

    if assets.get("hat"):
        try:
            assets["hat"] = assets["hat"].convert_alpha()
        except Exception:
            pass

    # --- Kies de juiste balloon skin ---
    balloon_dict = {
        "normal": assets["balloon"],
        "xmas": assets["balloon"],
        "blue": assets["blue_balloon"],
        "green": assets["green_balloon"],
        "purple": assets["purple_balloon"],
        "white": assets["white_balloon"]
    }
    balloon = balloon_dict.get(balloon_skin, assets["balloon"])
    hat = assets.get("hat") if balloon_skin == "xmas" else None

    # --- Overige assets ---
    background = assets["background"]
    sky_background = assets["sky_background"]
    fig_images = assets["fig_images"]
    tube = assets["tube"]
    balloon_prepop = assets["balloon_prepop"]
    balloon_pop = assets["balloon_pop"]
    death_screen = assets["death_screen"]
    game_music = assets.get("game_music", None)

    x, y = 300, 500
    speed_level = 2
    speed = speed_level * 0.8

    # Speel achtergrondmuziek
    if music_on and game_music:
        try:
            pygame.mixer.music.load(game_music)
            pygame.mixer.music.play(-1)
        except Exception:
            pass

    # --- Initial figures ---
    figures = [
        {"image": tube, "x": 0, "y": 0, "type": "tube"},
        {"image": random.choice(fig_images), "x": 0, "y": -700, "type": "spike"}
    ]

    score = 0
    check_score = 10
    debug = False  # toggle met D
    balloon_hitbox_height = 50
    balloon_crop = pygame.Surface((44, balloon_hitbox_height), pygame.SRCALPHA)
    font_hud = pygame.font.Font(None, 60)
    score_text = font_hud.render(f"{score}", True, (255, 255, 255))
    bg_y = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                elif event.key == pygame.K_d:
                    debug = not debug

        screen.fill((255, 255, 255))

        if paused:
            # --- Pauze overlay ---
            screen.blit(background, (0, bg_y))
            screen.blit(background, (0, bg_y - screen_size[1]))
            for fig in figures:
                screen.blit(fig["image"], (fig["x"], fig["y"]))
            screen.blit(balloon, (x, y))
            if hat:
                screen.blit(hat, (x + 3, y - 30))
            screen.blit(score_text, (287, 20))
            font_pause = pygame.font.Font(None, 80)
            text = font_pause.render("PAUSED", True, (255, 255, 255))
            screen.blit(text, (center_x - 110, center_y - 40))
            pygame.display.flip()
            clock.tick(60)
            continue

        # --- Scroll background & sky transition ---
        if "_sky_state" not in assets:
            assets["_sky_state"] = {
                "threshold": 1,
                "transitioning": False,
                "sky_static": False,
                "sky_y": -screen_size[1],
            }
        sky = assets["_sky_state"]

        if score >= sky["threshold"] and not sky["transitioning"] and not sky["sky_static"]:
            sky["transitioning"] = True
            sky["sky_y"] = -screen_size[1]

        if not sky["transitioning"] and not sky["sky_static"]:
            bg_y += speed_level - 1
            if bg_y >= screen_size[1]:
                bg_y = 0
            screen.blit(background, (0, bg_y))
            screen.blit(background, (0, bg_y - screen_size[1]))
        elif sky["transitioning"]:
            bg_y += speed_level - 1
            if bg_y >= screen_size[1]:
                bg_y = 0
            screen.blit(background, (0, bg_y))
            screen.blit(background, (0, bg_y - screen_size[1]))
            sky["sky_y"] += speed_level
            if sky["sky_y"] >= 0:
                sky["sky_y"] = 0
                sky["transitioning"] = False
                sky["sky_static"] = True
            screen.blit(sky_background, (0, int(sky["sky_y"])))
        else:
            screen.blit(sky_background, (0, 0))

        # --- Figures bewegen en tekenen ---
        for fig in list(figures):
            fig["y"] += speed_level

            balloon_crop.blit(balloon, (0, 0), (0, 0, 44, balloon_hitbox_height))
            balloon_mask = pygame.mask.from_surface(balloon_crop)
            fig_mask = pygame.mask.from_surface(fig["image"])
            offset = (fig["x"] - x, fig["y"] - y)

            # spawn nieuwe spike
            if fig["type"] == "spike" and fig["y"] > 0:
                if not any(f["type"] == "spike" and f["y"] < 0 for f in figures):
                    figures.append({
                        "image": random.choice(fig_images),
                        "x": 0,
                        "y": -695,
                        "type": "spike"
                    })

            # tube verwijderen
            if fig["type"] == "tube" and fig["y"] > 720:
                figures.remove(fig)
                continue

            # spike verwijderen en score updaten
            if fig["type"] == "spike" and fig["y"] > 720:
                figures.remove(fig)
                score += 1

            # balloon grenzen
            if x > screen_size[0] - balloon.get_width():
                x = screen_size[0] - balloon.get_width()
            if x < 0:
                x = 0

            # speed update
            speed_level += 0.0002
            speed = speed_level * 0.8

            # collision
            if balloon_mask.overlap(fig_mask, offset):
                if sfx_on:
                    try:
                        pygame.mixer.Sound("sound/balloon-pop.wav").play()
                    except Exception:
                        pass
                try:
                    pygame.mixer.music.stop()
                except Exception:
                    pass
                speed_level = 0
                speed = 0

                # --- prepop en pop tonen ---
                screen.blit(background, (0, bg_y))
                screen.blit(background, (0, bg_y - screen_size[1]))
                screen.blit(balloon_prepop, (x, y))
                for f in figures:
                    screen.blit(f["image"], (f["x"], f["y"]))
                pygame.display.flip()
                pygame.time.wait(25)

                screen.blit(background, (0, bg_y))
                screen.blit(background, (0, bg_y - screen_size[1]))
                screen.blit(balloon_pop, (x, y))
                for f in figures:
                    screen.blit(f["image"], (f["x"], f["y"]))
                pygame.display.flip()
                pygame.time.wait(1000)

                screen.blit(death_screen, (0, 0))
                pygame.display.flip()
                pygame.time.wait(2000)

                if score > high_score:
                    high_score = score
                return score, high_score

            # draw fig
            screen.blit(fig["image"], (fig["x"], fig["y"]))

            if debug:
                pygame.draw.rect(screen, (0, 255, 0), (fig["x"], fig["y"], 10, 10), 1)
                pygame.draw.rect(screen, (255, 0, 0), (fig["x"], fig["y"], fig["image"].get_width(), fig["image"].get_height()), 1)
                pygame.draw.rect(screen, (0, 0, 255), (x, y, balloon.get_width(), balloon.get_height()), 1)

        # --- HUD ---
        score_text = font_hud.render(f"{score}", True, (255, 255, 255))
        screen.blit(score_text, (287, 20))

        # Balloon movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            x -= speed
        if keys[pygame.K_RIGHT]:
            x += speed

        # Draw balloon en eventueel hat
        if hat:
            screen.blit(balloon, (x, y))
            screen.blit(hat, (x + 3, y - 30))
        else:
            screen.blit(balloon, (x, y))

        pygame.display.flip()
        clock.tick(60)

    try:
        pygame.mixer.music.stop()
    except Exception:
        pass
    if score > high_score:
        high_score = score
    return score, high_score


