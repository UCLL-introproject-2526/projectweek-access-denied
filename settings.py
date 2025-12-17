import pygame
from buttons import Button

WIDTH, HEIGHT = 600, 720

def settings(current_skin):
    pygame.event.clear()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    bgS = pygame.image.load("images/main_menu_screen_nologo.png")
    bgS = pygame.transform.scale(bgS, (WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arialblack", 28)

    xmas_btn = Button(150, 240, 300, 50, "CHRISTMAS HAT", font)
    back_btn = Button(150, 560, 300, 50, "BACK", font)

    skin = current_skin
    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if xmas_btn.is_clicked(event):
                skin = "default" if skin == "xmas" else "xmas"

            if back_btn.is_clicked(event):
                return skin
            
        xmas_btn.dynamic_color = (0, 200, 0) if skin == "xmas" else (200, 0, 0)

        screen.fill((240, 240, 240))
        screen.blit(bgS, (0, 0))
        title = font.render("SETTINGS", True, (255, 255, 255))
        screen.blit(title, (210, 150))

        xmas_btn.draw(screen)
        back_btn.draw(screen)

        pygame.display.flip()

