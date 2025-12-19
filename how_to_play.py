import pygame
from buttons import Button

WIDTH, HEIGHT = 600, 720

def how_to_play():
    pygame.event.clear()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # achtergrond = dezelfde als settings
    bg = pygame.image.load("images/main_menu_screen_nologo.png")
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

    # how to play image
    how_img = pygame.image.load("images/how_to_play.png")
    how_img = pygame.transform.scale(how_img, (WIDTH, HEIGHT))

    font = pygame.font.SysFont("arialblack", 15)
    
    x_icon = pygame.image.load("images/x.png").convert_alpha()
    x_icon = pygame.transform.scale(x_icon, (40, 40))
    back_btn = Button(
        10, 10, 40, 40, "", font,
        image=x_icon
    )


    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if back_btn.is_clicked(event):
                return

        screen.blit(bg, (0, 0))
        screen.blit(how_img, (0, 0))
        back_btn.draw(screen)

        pygame.display.flip()
