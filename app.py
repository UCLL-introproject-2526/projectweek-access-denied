import pygame

def main(): 


    def create_main_surface():
        #initialize Pygame
        pygame.init()


        # Tuple representing width and height in pixels
        screen_size = (1024, 768)
        return screen_size

    screen_size = create_main_surface()
    # Create window with given size
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Bloon Crackers")
    # Create window with given size
    while True:
        screen.fill((80, 150, 200))  # fills with blue
        pygame.display.flip()
        pygame.event.pump()
main()


