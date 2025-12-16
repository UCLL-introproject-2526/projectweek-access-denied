import pygame
import math

pygame.init()

# res and caption of game window
screen = pygame.display.set_mode((560, 720))
pygame.display.set_caption("Menu")

# background image
BG = pygame.image.load("images/8666420.jpg")
BG = pygame.transform.scale(BG, (560, 720))

# balloon goes up
def render_frame(surface, y):
    surface.blit(balloon, (280 - balloon.get_width()//2, int(y) - balloon.get_height()//2))

clock = pygame.time.Clock()

target_y = 250 # where balloon needs to stop
balloon = pygame.image.load("images/red-balloon.png").convert_alpha()
balloon.set_colorkey((255, 255, 255))

# game variables
game_paused = False


# define fonts
font = pygame.font.SysFont("arialblack", 40)

# define colors
text_col = (0,0,0)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# function to complete actions while game is running
def main_menu():
    game_paused = False

    pause_overlay = pygame.Surface((560, 720), pygame.SRCALPHA)
    pause_overlay.fill((0, 0, 0, 150))

    y = 750
    state = "rising"
    float_time = 0

    running = True
    while running:
        clock.tick(60)

        # background
        screen.blit(BG, (0,0))

        # events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_paused = not game_paused
            if event.type == pygame.QUIT:
                running = False

        # updates (only when not paused)
        if not game_paused:
            if state == "rising":
                y -= 3
                if y <= target_y:
                    y = target_y
                    state = "floating"
            elif state == "floating":
                float_time += 0.05
                y = target_y + math.sin(float_time) * 10
        
        # draw balloon
        render_frame(screen, y)

        # pause overlay
        if game_paused:
            screen.blit(pause_overlay, (0, 0))
            draw_text("PAUSED", font, (255,255,255), 200, 300)
        else:
            draw_text("Press ESC to pause", font, text_col, 67, 600)

        pygame.display.flip()

        render_frame(screen, y)
    pygame.quit()

main_menu()
