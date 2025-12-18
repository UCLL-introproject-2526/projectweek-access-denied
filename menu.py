import pygame
from buttons import Button

WIDTH, HEIGHT = 600, 720

def menu(score=0, high_score=0):
    pygame.event.clear()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    bgM = pygame.image.load("images/main_menu_screen.png")
    bgM = pygame.transform.scale(bgM, (WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arialblack", 30)
    font_settings = pygame.font.SysFont("arialblack", 10)
    font_how = pygame.font.SysFont("arialblack", 10)

    play_btn = Button(150, 425, 300, 50, "PLAY", font)
    settings_btn = Button(10, 10, 100, 20, "SETTINGS", font_settings)
    quit_btn = Button(150, 500, 300, 50, "QUIT", font)
    how_btn = Button(500, 10, 100, 20, "HOW TO PLAY", font_how)

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if play_btn.is_clicked(event):
                return "play"

            if settings_btn.is_clicked(event):
                return "settings"

            if quit_btn.is_clicked(event):
                return "quit"
            
            if how_btn.is_clicked(event):
                return "how"

        screen.fill((240, 240, 240))
        screen.blit(bgM, (0, 0))

        #  Lees high score hier telkens opnieuw uit bestand
        try:
            with open("high_score.txt", "r") as f:
                high_score = int(f.read())
        except Exception:
            high_score = 0

        # toon laatste score en high score

        if score:
            score_text = font.render(f"Last Score: {score}", True, (0, 0, 0))
            screen.blit(score_text, (190, 550))
        hs_text = font.render(f"High Score: {high_score}", True, (0, 0, 0))
        screen.blit(hs_text, (190, 600))

        play_btn.draw(screen)
        settings_btn.draw(screen)
        quit_btn.draw(screen)
        how_btn.draw(screen)


        pygame.display.flip()
