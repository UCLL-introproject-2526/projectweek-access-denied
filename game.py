import pygame
import random

def main_game(balloon_skin="normal", high_score=0):
    screen_size = (600, 720)
    center_x = screen_size[0] // 2
    center_y = screen_size[1] // 2
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()

    background = pygame.image.load("images/sky.jpg").convert()
    background = pygame.transform.scale(background, (600, 720))

    # Load images
    fig1 = pygame.image.load("images/spike_left.png").convert_alpha()
    fig1 = pygame.transform.scale(fig1, (600, 700))

    fig2 = pygame.image.load("images/spike_right.png").convert_alpha()
    fig2 = pygame.transform.scale(fig2, (600, 700))

    tube = pygame.image.load("images/straight_tube.png").convert_alpha()
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
    speed = 1.6
    speed_level = 2


    death = 0
    prepop = 0 

    # Background music (optional)
    try:
        pygame.mixer.music.load("sound/Floating-Dreams.mp3")
        pygame.mixer.music.play(-1)
    except Exception:
        pass

    # --- INITIAL FIGURES ---
    figures = [
        {"image": tube, "x": 0, "y": 0, "type": "tube"},
        {"image": random.choice([fig1, fig2]), "x": 0, "y": -700, "type": "spike"}
    ]

    score = 0
    check_score = 10

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        screen.blit(background, (0, 0))

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
                        "image": random.choice([fig1, fig2]),
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
                if score < 30:
                    if score >= check_score:
                        speed_level += 1
                        speed += 0.8
                        check_score += 10
                else:
                    if score >= check_score:
                        speed_level += 1
                        speed += 0.8
                        check_score += 20
                continue

            # Balloon boundaries
            if x > screen_size[0] - balloon.get_width():
                x = screen_size[0] - balloon.get_width()
            if x < 0:
                x = 0

            # Collision check
            if balloon_mask.overlap(fig_mask, offset):
                pygame.mixer.music.stop()
                speed_level = 0
                speed = 0

                # --- Show balloon prepop ---
                screen.blit(background, (0, 0))
                screen.blit(balloon_prepop, (x, y))
                for fig in figures:
                    screen.blit(fig["image"], (fig["x"], fig["y"]))
                pygame.display.flip()
                pygame.time.wait(25)

                # --- Show balloon pop ---
                screen.blit(background, (0, 0))
                screen.blit(balloon_pop, (x, y))
                for fig in figures:
                    screen.blit(fig["image"], (fig["x"], fig["y"]))
                pygame.display.flip()
                pygame.time.wait(1000)

                # --- Show death screen ---
                screen.blit(death_screen, (0, 0))
                pygame.display.flip()
                pygame.time.wait(2000)

                # after sequence, just pass control back to loop end
                pass

                

                # Update high score before returning
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

    # If window closed during loop, finalize and return
    try:
        pygame.mixer.music.stop()
    except Exception:
        pass
    if score > high_score:
        high_score = score
    return score, high_score
