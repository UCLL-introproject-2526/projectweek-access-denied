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

# Load images with transparency support
fig1 = pygame.image.load("images/spike_left.webp").convert_alpha()
fig1 = pygame.transform.scale(fig1, (600, 700))

fig2 = pygame.image.load("images/spike_right.webp").convert_alpha()
fig2 = pygame.transform.scale(fig2, (600, 700))

tube = pygame.image.load("images/straight_tube.webp").convert_alpha()
tube = pygame.transform.scale(tube, (600, 700))

balloon = pygame.image.load("images/ballon.jpg").convert_alpha()
balloon = pygame.transform.scale(balloon, (44, 100))
x, y = 300, 500  # start position

# Options for obstacles
options = [
    {"image": fig1, "x": 0, "y": -700},
    {"image": fig2, "x": 0, "y": -700}
]

# Start with one obstacle (tube in the middle)
figures = [
    {"image": tube, "x": center_x - 22, "y": y}
]

speed = 3          # balloon movement speed
speed_level = 5    # obstacle speed

pygame.mixer.music.load("sound/Floating-Dreams.mp3")
pygame.mixer.music.play(-1)  # loop background music

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))

    for fig in figures:
        fig["y"] += speed_level  # move obstacle down

        # Balloon hitbox (top half only)
        balloon_hitbox_height = 50
        balloon_crop = pygame.Surface((44, balloon_hitbox_height), pygame.SRCALPHA)
        balloon_crop.blit(balloon, (0, 0), (0, 0, 44, balloon_hitbox_height))
        balloon_mask = pygame.mask.from_surface(balloon_crop)

        fig_mask = pygame.mask.from_surface(fig["image"])
        offset = (fig["x"] - x, fig["y"] - y)

        # Respawn obstacle when it leaves screen
        if fig["y"] > 720:
            new = random.choice(options)  # pick random spike
            fig["image"] = new["image"]
            fig["x"] = new["x"]
            fig["y"] = new["y"]  # start above the screen

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

        # Balloon movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            x -= speed
        if keys[pygame.K_RIGHT]:
            x += speed

        # Draw everything
        screen.blit(fig["image"], (fig["x"], fig["y"]))
        screen.blit(balloon, (x, y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
