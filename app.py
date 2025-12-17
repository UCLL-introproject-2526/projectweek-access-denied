import pygame
from menu import menu
from game import main_game
from settings import settings

def main():
    pygame.init()

    balloon_skin = "normal"
    high_score = 0
    last_score = None

    while True:
        # geef laatste score en high score mee aan menu
        choice = menu(score=last_score, high_score=high_score)

        if choice == "play":
            last_score, high_score = main_game(balloon_skin)

        elif choice == "settings":
            balloon_skin = settings(balloon_skin)

        elif choice == "quit":
            break

    pygame.quit()

if __name__ == "__main__":
    main()
