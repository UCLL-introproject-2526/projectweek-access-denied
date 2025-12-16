import pygame
import math
from buttons import Button

pygame.init()

# window
WIDTH, HEIGHT = 600, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Balloon Game")

clock = pygame.time.Clock()

# background
MENU_BG = pygame.image.load('achtergrond_1.jpg').convert()
MENU_BG = pygame.transform.scale(MENU_BG, (WIDTH, HEIGHT))
BG = pygame.image.load('achtergrond_1.jpg')
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

# balloon
balloon = pygame.image.load("red-balloon_transparant.png").convert_alpha()
balloon = pygame.transform.scale(balloon, (100, 218))

# spike
spike_img = pygame.image.load("spike.png").convert_alpha()
spike_img = pygame.transform.scale(spike_img, (40, 40))
spike_img = pygame.transform.rotate(spike_img, 180)

# font
font = pygame.font.SysFont("arialblack", 40)

def draw_text(text, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# ----------------------------------
# BUTTONS
# ----------------------------------
start_button = Button(150, 250, 300, 60, "START", small_font)
quit_button = Button(150, 340, 300, 60, "QUIT", small_font)

resume_button = Button(150, 260, 300, 60, "RESUME", small_font)
pause_quit_button = Button(150, 340, 300, 60, "QUIT", small_font)

restart_button = Button(150, 260, 300, 60, "RESTART", small_font)
gameover_quit_button = Button(150, 340, 300, 60, "QUIT", small_font)

# ----------------------------------
# GAME STATES
# ----------------------------------
MENU = 0
GAME = 1
PAUSE = 2
GAME_OVER = 3

game_state = MENU


# spikes setup
spikes = []
start_x = 180
spike_y = 350
for i in range(4):
    rect = spike_img.get_rect(topleft=(start_x + i * 40, spike_y))
    spikes.append(rect)

def main_game():
    # balloon position
    x = WIDTH // 2
    y = 750
    speed_x = 5

    target_y = 250
    state = "rising"
    float_time = 0

    obstacle_rect = pygame.Rect(200, 300, 160, 10)

    game_paused = False
    game_over = False
    running = True

    pause_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pause_overlay.fill((0, 0, 0, 150))

    while running:
        clock.tick(60)
        screen.blit(BG, (0, 0))

        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_paused = not game_paused
            
            # ---------------- MENU ----------------
        if game_state == MENU and event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.is_clicked(event):
                game_state = GAME
            elif quit_button.is_clicked(event):
                running = False

        keys = pygame.key.get_pressed()

        if not game_paused and not game_over:
            # horizontal movement
            if keys[pygame.K_LEFT]:
                x -= speed_x
            if keys[pygame.K_RIGHT]:
                x += speed_x

            # keep balloon on screen
            x = max(balloon.get_width() // 2, min(WIDTH - balloon.get_width() // 2, x))

            # vertical movement
            if state == "rising":
                y -= 3
                if y <= target_y:
                    y = target_y
                    state = "floating"
            elif state == "floating":
                float_time += 0.05
                y = target_y + math.sin(float_time) * 10

        balloon_rect = balloon.get_rect(center=(x, int(y)))

        # kleinere hitbox (alleen ballon, niet koord)
        hitbox = balloon_rect.copy()
        hitbox.width = int(balloon_rect.width * 0.8)
        hitbox.height = int(balloon_rect.height * 0.2)

        hitbox.centerx = balloon_rect.centerx
        hitbox.top = balloon_rect.top

        # draw spikes
        for rect in spikes:
            screen.blit(spike_img, rect)
            if hitbox.colliderect(rect):
                game_over = True

        # obstacle
        pygame.draw.rect(screen, (82, 82, 82), obstacle_rect)
        if hitbox.colliderect(obstacle_rect):
            game_over = True
        
        pygame.draw.rect(screen, (255, 0, 0), hitbox, 2)

        # draw balloon
        screen.blit(balloon, balloon_rect)

        # UI
        if game_over:
            draw_text("GAME OVER", (255, 0, 0), 150, 100)

        if game_paused:
            screen.blit(pause_overlay, (0, 0))
            draw_text("PAUSED", (255, 255, 255), 200, 300)
        else:
            draw_text("ESC = pause | ← → bewegen", (0, 0, 0), 60, 660)

        pygame.display.flip()

    pygame.quit()

main_game()
