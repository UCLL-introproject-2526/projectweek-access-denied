import pygame

pygame.init()
screen_size = (600, 720)
screen = pygame.display.set_mode(screen_size)
background = pygame.image.load("images/achtergrond 1.jpg").convert()
background = pygame.transform.scale(background, (600, 720))
clock = pygame.time.Clock()

#afbeeldingen zijn gemaakt met draw io de breete is 9 vakken en op de uiteinden 3 vakken
fig1 = pygame.image.load("images/spike_left.png") # dit maakt de variable
fig1 = pygame.transform.scale(fig1, (600, 700)) # dit bepaald de schaal

fig2 = pygame.image.load("images/spike_right.png") # dit maakt de variable
fig2 = pygame.transform.scale(fig2, (600, 700)) # dit bepaald de schaal

balloon = pygame.image.load("images/red-balloon transparant.png")
balloon = pygame.transform.scale(balloon, (44, 100))  # breedte, hoogte
x, y = 450, 500 # begin positie

figures = [
    {"image": fig1, "x": 0, "y": 10}, # centreren doe je door (1024-500)/2    ;;//;; de 500 is de afbeelding grote
    {"image": fig2, "x": 0, "y": -685} # start boven fig1
]
speed = 1.5 # de snelheid van de beweging aanpassen
SPeed = 3
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255,255,255))  # achtergrond zwart
    screen.blit(background, (0, 0))

    for fig in figures:
        fig["y"] += SPeed # dit zorgt dat het naar beneden beweegd

        # opnieuw bovenaan als onderkant scherm bereikt
        if fig["y"] > 720:
            fig["y"] = -665  # hoogte van de afbeelding dit moet iets kleiner zijn om gaten te voorkomen tussen de twee

        if x > 920: # de rechter kant limiteren voor de beweging van de ballon
            x = 920
        if x < 10: # de linker kant limiteren voor de beweging van de ballon
            x = 10
        keys = pygame.key.get_pressed() # lijkt op een dict maar werkt betje anders
        if keys[pygame.K_LEFT]: # K_LEFT is voor pijltje links
            x -= speed
        if keys[pygame.K_RIGHT]: # K_RIGHT is voor pijltje rechts
            x += speed
        screen.blit(fig["image"], (fig["x"], fig["y"])) # dit tekend je afbeeldingen
        screen.blit(balloon, (x, y)) # de afbeelding op het scherm zetten

    pygame.display.flip() # dit laat wat je hebt gevraagd
    clock.tick(60)  # 60 FPS dit zorgt er voor dat er geen extra probleemen zijn door een stabiele frame rate

pygame.quit()
