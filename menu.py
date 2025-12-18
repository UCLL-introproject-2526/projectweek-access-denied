import pygame
from buttons import Button

WIDTH, HEIGHT = 600, 720

def menu(score=0, high_score=0):
    pygame.event.clear()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    bgM = pygame.image.load("images/main_menu_screen.png")
    bgM = pygame.transform.scale(bgM, (WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    #fonts
    font = pygame.font.SysFont("arialblack", 30)
    font_settings = pygame.font.SysFont("arialblack", 15)

    #buttons
    play_btn = Button(150, 425, 300, 50, "PLAY", font, (200, 50, 50))
    settings_btn = Button(10, 10, 120, 30, "SETTINGS", font_settings,(50, 150, 250))
    skins_btn = Button(470, 10, 120, 30, "SKINS", font_settings, (100, 250, 100))
    quit_btn = Button(150, 500, 300, 50, "QUIT", font,(200,200,50))


    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if play_btn.is_clicked(event):
                return "play"

            if settings_btn.is_clicked(event):
                return "settings"
            
            if skins_btn.is_clicked(event):
                return "skins"

            if quit_btn.is_clicked(event):
                return "quit"

        screen.fill((240, 240, 240))
        screen.blit(bgM, (0, 0))

        # toon laatste score en high score
        if score is not None:
            score_text = font.render(f"Last Score: {score}", True, (0, 0, 0))
            screen.blit(score_text, (190, 550))
        hs_text = font.render(f"High Score: {high_score}", True, (0, 0, 0))
        screen.blit(hs_text, (190, 600))

        play_btn.draw(screen)
        settings_btn.draw(screen)
        skins_btn.draw(screen) 
        quit_btn.draw(screen)

        pygame.display.flip()
