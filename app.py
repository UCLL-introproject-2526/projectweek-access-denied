# app.py
import pygame
from menu import menu
from game import main_game

def main():
    pygame.init()
    pygame.mixer.init()

    while True:
        choice = menu()
        if choice == "play":
            main_game()
        elif choice == "quit":
            break

    pygame.quit()

if __name__ == "__main__":
    main()

