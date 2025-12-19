import pygame
import random

# Beter werkt deze shit




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
        "images/saw1_right.png",
        "images/saw1_left.png",
        "images/spike_bal.png",
        "images/crates_mix.png",
        "images/crates1_left.png",
        "images/crates1_right.png",
        "images/mini_tube_spike_left.png",
        "images/mini_tube_spike_right.png",
        "images/cube_spike_left_crates_left.png",
        "images/cube_spike_left_crates_right.png",
        "images/hourglass_cubes_left.png",
        "images/hourglass_cubes_right.png",
        "images/spike_room_left.png",
        "images/spike_room_right.png",
        "images/tree_left.png",
        "images/tree_right.png",
        "images/tree_saw_left.png",
        "images/tree_saw_right.png",
        "images/tree.png",
    ]

    assets["fig_images"] = [_load(p, (600, 700)) for p in fig_paths]
    assets["tube"] = _load("images/straight_tube_texture.png", (600, 700))
    assets["balloon"] = _load("images/balloon_red.png")
    assets["balloon_prepop"] = _load("images/balloon_prepop.png")
    assets["balloon_pop"] = _load("images/balloon_pop.png")
    assets["heart"] = _load("images/heart.png", (35, 35))
    assets["death_screen"] = _load("images/death_screen.png", (600, 720), alpha=False)
    assets["hat"] = _load("images/kerstmuts.png", (40, 30))
    # optional assets
    try:
        assets["hat"] = pygame.image.load("images/kerstmuts.png")
    except Exception:
        assets["hat"] = None

    assets["game_music"] = "sound/Floating-Dreams.mp3"
    return assets


def main_game(balloon_skin="normal", assets=None, music_on=True, sfx_on=True):
    # Damage / flicker system
    damage_timer = 0
    damage_duration = 2000  # 2 seconden in ms
    flicker_interval = 150  # hoe snel hij flikkert

    paused = False
    screen_size = (600, 720)
    center_x = screen_size[0] // 2
    center_y = screen_size[1] // 2
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    last_heart_spawn = pygame.time.get_ticks()
    heart_spawn_delay = 20000  # 20 seconden


    try:
        with open("high_score.txt", "r") as f:
            high_score = int(f.read())
    except Exception:
            high_score = 0

    # Custom event that fires every 1000 ms (1 second)
    SCORE_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SCORE_EVENT, 20)


    # Use provided assets or load them now (loader avoids convert calls)
    if assets is None:
        assets = load_assets(screen_size)

    # After creating a display, we can call convert/convert_alpha safely for speed
    try:
        assets["background"] = assets["background"].convert()
    except Exception:
        pass

    for i, img in enumerate(assets["fig_images"]):
        try:
            assets["fig_images"][i] = img.convert_alpha()
        except Exception:
            pass

    try:
        assets["tube"] = assets["tube"].convert_alpha()
    except Exception:
        pass

    try:
        assets["balloon"] = assets["balloon"].convert_alpha()
    except Exception:
        pass

    try:
        assets["heart"] = assets["heart"].convert_alpha()
    except Exception:
        pass


    for key in ("balloon_prepop", "balloon_pop", "death_screen"):
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

    }
    balloon = balloon_dict.get(balloon_skin, assets["balloon"])
    hat = assets.get("hat") if balloon_skin == "xmas" else None

    # --- Overige assets ---
    background = assets["background"]
    fig_images = assets["fig_images"]
    tube = assets["tube"]
    balloon = assets["balloon"]
    heart_img = assets["heart"]
    balloon_prepop = assets["balloon_prepop"]
    balloon_pop = assets["balloon_pop"]
    death_screen = assets["death_screen"]
    hat = assets.get("hat") if balloon_skin == "xmas" else None
    game_music = assets.get("game_music", None)

    x, y = 300, 500
    speed_level = 3
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
        {"image": random.choice(fig_images), "x": 0, "y": -695, "type": "spike"}
    ]

    score = 0
    check_score = 10

    # --- LIVES ---
    max_lives = 3
    lives = 2
    level = 1
    last_hit_time = 0
    hit_invincibility_duration = 2000  # ms = 2 seconde
    invincible = False
    if not invincible:
        original_speed = speed_level


    font_popup = pygame.font.SysFont("terminal", 40)
    score_popup_text = None
    score_popup_pos = (0, 0)
    score_popup_start = 0
    score_popup_duration = 1000  # 1 seconde




    # UI & debug state
    debug = False  # toggle with D key
    balloon_hitbox_height = 50
    balloon_crop = pygame.Surface((44, balloon_hitbox_height), pygame.SRCALPHA)
    font_hud = pygame.font.SysFont("terminal", 60)
    font_gameover = pygame.font.SysFont("terminal", 60)
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
            if event.type == SCORE_EVENT and not paused:
                score += 1

        screen.fill((255, 255, 255))

        if paused:
            # --- Pauze overlay ---
            screen.blit(background, (0, bg_y))
            screen.blit(background, (0, bg_y - screen_size[1]))
            for fig in figures:
                screen.blit(fig["image"], (fig["x"], fig["y"]))
            screen.blit(balloon, (x, y))
            screen.blit(score_text, (260, 20))

            font_pause = pygame.font.Font(None, 80)
            text = font_pause.render("PAUSED", True, (255, 255, 255))
            screen.blit(text, (center_x - 110, center_y - 40))
            pygame.display.flip()
            clock.tick(60)
            continue

        # --- Scroll dungeon background ---
        bg_y += speed_level - 1
        if bg_y >= screen_size[1]:
            bg_y = 0
        screen.blit(background, (0, bg_y))
        screen.blit(background, (0, bg_y - screen_size[1]))



        # --- Figures bewegen en tekenen ---
        for fig in list(figures):
            fig["y"] += speed_level

            balloon_hitbox_height = 50
            balloon_crop = pygame.Surface((44, balloon_hitbox_height), pygame.SRCALPHA)
            balloon_crop.blit(balloon, (0, 0), (0, 0, 44, balloon_hitbox_height))
            balloon_mask = pygame.mask.from_surface(balloon_crop)
            fig_mask = pygame.mask.from_surface(fig["image"])
            offset = (fig["x"] - x, fig["y"] - y)

            if fig["type"] == "spike" and fig["y"] > 0:
                if not any(f["type"] == "spike" and f["y"] < 0 for f in figures):
                    figures.append({
                        "image": random.choice(fig_images),
                        "x": 0,
                        "y": -695,
                        "type": "spike"
                    })
            
            if fig["type"] == "heart" and fig["y"] > 720:
                figures.remove(fig)
                continue


            if fig["type"] == "tube" and fig["y"] > 720:
                figures.remove(fig)
                continue

            if fig["type"] == "spike" and fig["y"] > 720:
                figures.remove(fig)

                if score % 10 == 0:
                    level += 1

            
            current_time = pygame.time.get_ticks()

            if level >= 2 and current_time - last_heart_spawn >= heart_spawn_delay:
                figures.append({
                    "image": heart_img,
                    "x": random.randint(200, 400),
                    "y": -40,
                    "type": "heart"
                })
                last_heart_spawn = current_time


            # Balloon boundaries
            if x > screen_size[0] - balloon.get_width():
                x = screen_size[0] - balloon.get_width()
            if x < 0:
                x = 0



            speed_level += 0.0002
            speed = speed_level * 0.8

            # --- HARTJES OPPAKKEN ---
            if fig["type"] == "heart":
                heart_mask = pygame.mask.from_surface(fig["image"])
                if balloon_mask.overlap(heart_mask, offset):
                    if lives < max_lives:
                        lives += 1
                    else:
                        score += 250
                        score_popup_text = font_popup.render("+250", True, (0, 180, 0))
                        score_popup_pos = (x + 30, y - 20)
                        score_popup_start = pygame.time.get_ticks()

                    figures.remove(fig)
                    continue  # meteen verder met de volgende figuur

            # --- GEVAARLIJKE OBSTAKELS ---
            elif fig["type"] == "spike" and balloon_mask.overlap(fig_mask, offset) and not invincible:

                current_time = pygame.time.get_ticks()
                if current_time - last_hit_time >= hit_invincibility_duration:
                    last_hit_time = current_time
                    lives -= 1
                    damage_timer = pygame.time.get_ticks()

                    if lives > 0:
                            # Slow down speed during invincibility
                        original_speed = speed_level
                        speed_level = max(1, speed_level // 2)  # halve speed
                        invincible = True

                        # Play SFX
                        if sfx_on:
                            try:
                                pygame.mixer.Sound("sound/balloon-inflation.wav").play()
                            except Exception:
                                pass
            # Restore speed after invincibility ends
            if invincible and pygame.time.get_ticks() - last_hit_time >= hit_invincibility_duration:
                speed_level = original_speed
                invincible = False
            # --- DEATH CHECK PAS HIER ---
            if lives <= 0:
                # toon prepop en pop
                if sfx_on:
                    try:
                        pygame.mixer.Sound("sound/balloon-pop.wav").play()
                    except Exception:
                        pass
                pygame.mixer.music.stop()
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

                # death screen
                screen.blit(death_screen, (0, 0))

                score_text = font_gameover.render(f"Score: {score}", True, (255, 255, 255))
                score_rect = score_text.get_rect(center=(screen_size[0] // 2, 500))
                screen.blit(score_text, score_rect)

                pygame.display.flip()
                pygame.time.wait(2000)

                # update last score
                with open("last_score.txt", "w") as f:
                    f.write(str(score))

                # update high score
                if score > high_score:
                    high_score = score
                    with open("high_score.txt", "w") as f:
                        f.write(str(high_score))
                return

            # draw fig
            screen.blit(fig["image"], (fig["x"], fig["y"]))

            # --- DEBUG OVERLAY ---
            if debug:
                try:
                    pygame.draw.rect(screen, (0, 255, 0), (fig["x"], fig["y"], 10, 10), 1)
                    pygame.draw.rect(screen, (255, 0, 0),
                                    (fig["x"], fig["y"], fig["image"].get_width(), fig["image"].get_height()), 1)
                    pygame.draw.rect(screen, (0, 0, 255),
                                    (x, y, balloon.get_width(), balloon.get_height()), 1)
                    font_dbg = pygame.font.Font(None, 20)
                    label = font_dbg.render(fig.get("type", ""), True, (255, 255, 255))
                    screen.blit(label, (fig["x"] + 12, fig["y"] + 2))
                except Exception:
                    pass

        # --- HUD ---
        score_text = font_hud.render(f"{score}", True, (255, 255, 255))
        screen.blit(score_text, (20, 20))

        # --- DRAW LIVES ---
        for i in range(lives):
            screen.blit(heart_img, (screen_size[0] - (i + 1) * 35 - 10, 10))



        # Balloon movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            x -= speed
        if keys[pygame.K_RIGHT]:
            x += speed

        # Flikker
        current_time = pygame.time.get_ticks()
        is_damaged = current_time - damage_timer < damage_duration

        draw_balloon = True
        if is_damaged:
            if (current_time // flicker_interval) % 2 == 0:
                draw_balloon = False

        # Draw balloon (with optional hat)
        if draw_balloon:
            if hat:
                screen.blit(balloon, (x, y))
                screen.blit(hat, (x + 3, y - 30))
            else:
                screen.blit(balloon, (x, y))

        # --- SCORE POPUP (+250) ---
        if score_popup_text:
            if pygame.time.get_ticks() - score_popup_start < score_popup_duration:
                screen.blit(score_popup_text, score_popup_pos)
            else:
                score_popup_text = None


        pygame.display.flip()
        clock.tick(60)