import pygame
from buttons import Button

WIDTH, HEIGHT = 600, 720

def settings(music_on, sfx_on):
    pygame.event.clear()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    bgS = pygame.image.load("images/main_menu_screen_nologo.png")
    bgS = pygame.transform.scale(bgS, (WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arialblack", 28)

    
    music_btn = Button(150, 320, 300, 50, "MUSIC: ON", font)
    sfx_btn   = Button(150, 400, 300, 50, "SFX: ON", font)
    back_btn = Button(150, 560, 300, 50, "BACK", font)

    
    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            
            
            if music_btn.is_clicked(event):
                music_on = not music_on
                

            if sfx_btn.is_clicked(event):
                sfx_on = not sfx_on


            if back_btn.is_clicked(event):
                return music_on, sfx_on

            
        
        music_btn.dynamic_color = (0, 200, 0) if music_on else (200, 0, 0)
        sfx_btn.dynamic_color   = (0, 200, 0) if sfx_on else (200, 0, 0)

        
        music_btn.text = f"MUSIC: {'ON' if music_on else 'OFF'}"
        sfx_btn.text   = f"SFX: {'ON' if sfx_on else 'OFF'}"

        screen.fill((240, 240, 240))
        screen.blit(bgS, (0, 0))
        title = font.render("SETTINGS", True, (255, 255, 255))
        screen.blit(title, (210, 150))

        
        music_btn.draw(screen)
        sfx_btn.draw(screen)
        back_btn.draw(screen)

        pygame.display.flip()

