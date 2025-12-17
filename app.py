import pygame
import random

pygame.init()

screen_size = (600, 720)
center_x = screen_size[0] // 2
center_y = screen_size[1] // 2
screen = pygame.display.set_mode(screen_size)
background = pygame.image.load("images/sky.jpg").convert()
background = pygame.transform.scale(background, (600, 720))
clock = pygame.time.Clock()

# Load images
fig1 = pygame.image.load("images/spike_left.webp").convert_alpha()
fig1 = pygame.transform.scale(fig1, (600, 700))

fig2 = pygame.image.load("images/spike_right.webp").convert_alpha()
fig2 = pygame.transform.scale(fig2, (600, 700))

tube = pygame.image.load("images/straight_tube.webp").convert_alpha()
tube = pygame.transform.scale(tube, (600, 700))

balloon = pygame.image.load("images/ballon.jpg").convert_alpha()
balloon = pygame.transform.scale(balloon, (44, 100))
x, y = 300, 500

speed = 1.6
speed_level = 2

pygame.mixer.music.load("sound/Floating-Dreams.mp3")
pygame.mixer.music.play(-1)

# --- INITIAL FIGURES ---
# Tube at start + one spike above it
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
    for fig in list(figures):  # copy to allow removal
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
            # Check if we already have a "next" spike queued
            if not any(f["type"] == "spike" and f["y"] < 0 for f in figures):
                figures.append({
                    "image": random.choice([fig1, fig2]),
                    "x": 0,
                    "y": -700,
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
            if score >= 30:
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
            screen.fill((200, 25, 25))
            pygame.mixer.music.stop()
            font = pygame.font.Font(None, 74)
            text = font.render("Game Over", True, (0, 0, 0))
            screen.blit(text, (center_x - 100, center_y))
            pygame.display.flip()
            pygame.time.delay(2000)
            running = False

        # Draw
        screen.blit(fig["image"], (fig["x"], fig["y"]))

        font = pygame.font.Font(None, 80)  # smaller font for score

        # inside the main loop, after drawing everything:
        score_text = font.render(f"{score}", True, (0, 0, 0))
        screen.blit(score_text, (285, 10))  # top-left corner

        # --- Increase speed every 10 points ---
        




    # Balloon movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= speed
    if keys[pygame.K_RIGHT]:
        x += speed

    screen.blit(balloon, (x, y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
