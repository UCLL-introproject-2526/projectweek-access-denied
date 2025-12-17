import pygame
from menu import menu
from game import main_game
from settings import settings

def main():
    pygame.init()

    balloon_skin = "normal"

    while True:
        choice = menu()

        if choice == "play":
            main_game(balloon_skin)

        elif choice == "settings":
            balloon_skin = settings(balloon_skin)

        elif choice == "quit":
            break

    pygame.quit()

if __name__ == "__main__":
    main()

    # test
