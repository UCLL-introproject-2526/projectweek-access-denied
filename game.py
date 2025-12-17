import pygame
import random

def main_game(balloon_skin="normal", high_score=0):
    screen_size = (600, 720)
    center_x = screen_size[0] // 2
    center_y = screen_size[1] // 2
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()

    background = pygame.image.load("images/dungeon.png").convert()
    background = pygame.transform.scale(background, (600, 720))

    # Load images
    fig1 = pygame.image.load("images/corridor_right_spiked.png").convert_alpha()
    fig1 = pygame.transform.scale(fig1, (600, 700))

    fig2 = pygame.image.load("images/corridor_right.png").convert_alpha()
    fig2 = pygame.transform.scale(fig2, (600, 700))

    fig3 = pygame.image.load("images/corridor_left_2.png").convert_alpha()
    fig3 = pygame.transform.scale(fig3, (600, 700))

    fig4 = pygame.image.load("images/drie_eilanden_links.png").convert_alpha()
    fig4 = pygame.transform.scale(fig4, (600, 700))

    fig5 = pygame.image.load("images/drie_eilanden_rechts.png").convert_alpha()
    fig5 = pygame.transform.scale(fig5, (600, 700))

    fig6 = pygame.image.load("images/mini_eilanden_left_2.png").convert_alpha()
    fig6 = pygame.transform.scale(fig6, (600, 700))

    fig7 = pygame.image.load("images/mini_eilanden_right_2.png").convert_alpha()
    fig7 = pygame.transform.scale(fig7, (600, 700))

    fig8 = pygame.image.load("images/eilanden_right.png").convert_alpha()
    fig8 = pygame.transform.scale(fig8, (600, 700))

    fig9 = pygame.image.load("images/eilanden_left.png").convert_alpha()
    fig9 = pygame.transform.scale(fig9, (600, 700))

    fig10 = pygame.image.load("images/cube_spike.png").convert_alpha()
    fig10 = pygame.transform.scale(fig10, (600, 700))

    fig11 = pygame.image.load("images/cube_spike_left.png").convert_alpha()
    fig11 = pygame.transform.scale(fig11, (600, 700))

    fig12 = pygame.image.load("images/cube_spike_right.png").convert_alpha()
    fig12 = pygame.transform.scale(fig12, (600, 700))

    fig13 = pygame.image.load("images/cube_spike_right.png").convert_alpha()
    fig13 = pygame.transform.scale(fig13, (600, 700))

    tube = pygame.image.load("images/straight_tube_texture.png").convert_alpha()
    tube = pygame.transform.scale(tube, (600, 700))

    if balloon_skin == "xmas":
        balloon = pygame.image.load("images/balloon.png").convert_alpha()
        hat = pygame.image.load("images/kerstmuts.png").convert_alpha()
    else:
        balloon = pygame.image.load("images/balloon.png").convert_alpha()
        hat = None

    balloon_prepop = pygame.image.load("images/balloon_prepop.png").convert_alpha()
    balloon_pop = pygame.image.load("images/balloon_pop.png").convert_alpha()
    death_screen = pygame.image.load("images/death_screen.png")
    death_screen = pygame.transform.scale(death_screen, (600, 720))

    x, y = 300, 500
    speed_level = 2
    speed = speed_level * 0.8

    game_music = "sound/Floating-Dreams.mp3"
    pop_sound = "sound/balloon_pop.wav"

    # Background music
    try:
        pygame.mixer.music.load(game_music)
        pygame.mixer.music.play(-1)
    except Exception:
        pass

    # --- INITIAL FIGURES ---
    figures = [
        {"image": tube, "x": 0, "y": 0, "type": "tube"},
        {"image": random.choice([fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10, fig11, fig12, fig13]), "x": 0, "y": -700, "type": "spike"}
    ]

    score = 0
    check_score = 10

    # background offset
    bg_y = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))

        # --- Scroll background ---
        bg_y += speed_level - 1
        if bg_y >= screen_size[1]:
            bg_y = 0
        screen.blit(background, (0, bg_y))
        screen.blit(background, (0, bg_y - screen_size[1]))

        # --- MOVE AND DRAW FIGURES ---
        for fig in list(figures):
            fig["y"] += speed_level

            # Balloon hitbox
            balloon_hitbox_height = 50
            balloon_crop = pygame.Surface((44, balloon_hitbox_height), pygame.SRCALPHA)
            balloon_crop.blit(balloon, (0, 0), (0, 0, 44, balloon_hitbox_height))
            balloon_mask = pygame.mask.from_surface(balloon_crop)

            fig_mask = pygame.mask.from_surface(fig["image"])
            offset = (fig["x"] - x, fig["y"] - y)

            # --- Spawn next spike early ---
            if fig["type"] == "spike" and fig["y"] > 0:
                if not any(f["type"] == "spike" and f["y"] < 0 for f in figures):
                    figures.append({
                        "image": random.choice([fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10, fig11, fig12, fig13]),
                        "x": 0,
                        "y": -695,
                        "type": "spike"
                    })

            # --- Remove tube once it leaves ---
            if fig["type"] == "tube" and fig["y"] > 720:
                figures.remove(fig)
                continue

            # --- Remove spikes once they leave ---
            if fig["type"] == "spike" and fig["y"] > 720:
                figures.remove(fig)
                score += 1

            # Balloon boundaries
            if x > screen_size[0] - balloon.get_width():
                x = screen_size[0] - balloon.get_width()
            if x < 0:
                x = 0

            # update speed
            speed_level += 0.0001
            speed = speed_level * 0.8

            # Collision check
            if balloon_mask.overlap(fig_mask, offset):
                try:
                    pygame.mixer.Sound(pop_sound).play()
                except Exception:
                    pass
                pygame.mixer.music.stop()
                speed_level = 0
                speed = 0

                # --- Show balloon prepop ---
                screen.blit(background, (0, bg_y))
                screen.blit(background, (0, bg_y - screen_size[1]))
                screen.blit(balloon_prepop, (x, y))
                for f in figures:
                    screen.blit(f["image"], (f["x"], f["y"]))
                pygame.display.flip()
                pygame.time.wait(25)

                # --- Show balloon pop ---
                screen.blit(background, (0, bg_y))
                screen.blit(background, (0, bg_y - screen_size[1]))
                screen.blit(balloon_pop, (x, y))
                for f in figures:
                    screen.blit(f["image"], (f["x"], f["y"]))
                pygame.display.flip()
                pygame.time.wait(1000)

                # --- Show death screen ---
                screen.blit(death_screen, (0, 0))
                pygame.display.flip()
                pygame.time.wait(2000)

                if score > high_score:
                    high_score = score
                return score, high_score

            # Draw obstacle
            screen.blit(fig["image"], (fig["x"], fig["y"]))

        # --- HUD ---
        font_hud = pygame.font.Font(None, 60)
        score_text = font_hud.render(f"{score}", True, (255, 255, 255))
        screen.blit(score_text, (287, 20))

        # Balloon movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            x -= speed
        if keys[pygame.K_RIGHT]:
            x += speed

        # Draw balloon (with optional hat)
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
