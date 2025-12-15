def main(): 
    import pygame


    def create_main_surface():
        #initialize Pygame
        pygame.init()


        # Tuple representing width and height in pixels
        screen_size = (1024, 768)
        return screen_size

    screen_size = create_main_surface()
    # Create window with given size
    while True:
        pygame.display.set_mode(screen_size)

main()