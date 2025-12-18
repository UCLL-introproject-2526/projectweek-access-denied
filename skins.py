import pygame
from buttons import Button

WIDTH, HEIGHT = 600, 720

def skin(current_skin):
    pygame.event.clear()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    bgS = pygame.image.load("images/main_menu_screen_nologo.png")
    bgS = pygame.transform.scale(bgS, (WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arialblack", 28)

    normal_btn = Button(150, 240, 300, 50, "NORMAL SKIN: ON", font)
    xmas_btn   = Button(150, 320, 300, 50, "XMAS HAT: OFF", font)
    blue_btn   = Button(150, 400, 300, 50, "BLUE SKIN: OFF", font)
    green_btn  = Button(150, 480, 300, 50, "GREEN SKIN: OFF", font)
    purple_btn = Button(150, 560, 300, 50, "PURPLE SKIN: OFF", font)
    white_btn  = Button(150, 640, 300, 50, "WHITE SKIN: OFF", font)
    back_btn = Button(150, 700, 300, 50, "BACK", font)

    skin = current_skin
    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if normal_btn.is_clicked(event):
                skin = "normal"
            
            if xmas_btn.is_clicked(event):
                skin = "normal" if skin == "xmas" else "xmas"

            if blue_btn.is_clicked(event):
                skin = "normal" if skin == "blue" else "blue"

            if green_btn.is_clicked(event):
                skin = "normal" if skin == "green" else "green"

            if purple_btn.is_clicked(event):
                skin = "normal" if skin == "purple" else "purple"

            if white_btn.is_clicked(event):
                skin = "normal" if skin == "white" else "white"

            if back_btn.is_clicked(event):
                return skin

        normal_btn.dynamic_color = (0, 200, 0) if skin == "normal" else (200, 0, 0)
        xmas_btn.dynamic_color = (0, 200, 0) if skin == "xmas" else (200, 0, 0)
        blue_btn.dynamic_color = (0, 200, 0) if skin == "blue" else (200, 0, 0)
        green_btn.dynamic_color = (0, 200, 0) if skin == "green" else (200, 0, 0)
        purple_btn.dynamic_color = (0, 200, 0) if skin == "purple" else (200, 0, 0)
        white_btn.dynamic_color = (0, 200, 0) if skin == "white" else (200, 0, 0)

        xmas_btn.text = f"XMAS HAT: {'ON' if skin == 'xmas' else 'OFF'}"
        normal_btn.text = f"NORMAL SKIN : {'ON' if skin == 'normal' else 'OFF'}"
        blue_btn.text = f"BLUE SKIN : {'ON' if skin == 'blue' else 'OFF'}"
        green_btn.text = f"GREEN SKIN : {'ON' if skin == 'green' else 'OFF'}"
        purple_btn.text = f"PURPLE SKIN : {'ON' if skin == 'purple' else 'OFF'}"
        white_btn.text = f"WHITE SKIN : {'ON' if skin == 'white' else 'OFF'}"

        screen.fill((240, 240, 240))
        screen.blit(bgS, (0, 0))
        title = font.render("SELECT SKIN", True, (255, 255, 255))
        screen.blit(title, (200, 150))

        normal_btn.draw(screen)
        xmas_btn.draw(screen)
        blue_btn.draw(screen)
        green_btn.draw(screen)
        purple_btn.draw(screen)
        white_btn.draw(screen)
        back_btn.draw(screen)

        pygame.display.flip()