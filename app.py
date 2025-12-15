def main(): 
    import pygame


    def create_main_surface():
        pygame.init() #initialize Pygame
        screen_size = (1024, 768) # Tuple representing width and height in pixels
        screen = pygame.display.set_mode(screen_size)
        return screen

    screen = create_main_surface() # Create window with given size
    balloon = pygame.image.load("ballon.png")
    balloon = pygame.transform.scale(balloon, (100, 150))  # breedte, hoogte


    
    running = True
    while running:
        for event in pygame.event.get(): # om het spel af te sluiten
            if event.type == pygame.QUIT:# dit ook
                running = False # dit ook
        screen.fill((50, 100, 180)) # de achtergrond een kleur geven
        screen.blit(balloon, (450, 500)) # de afbeelding op het scherm zetten
        pygame.display.flip() # ververst het scherm
    pygame.quit() # ook nog om het spel af te sluiten

main()