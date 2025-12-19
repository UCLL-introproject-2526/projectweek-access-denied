import pygame
from loading import loade
from menu import menu
from game import main_game, load_assets
from settings import settings
from how_to_play import how_to_play

def main():
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("🎈Bloon Crackers🎈")

    music_on = True
    sfx_on = True

    balloon_skin = "normal"
    high_score = 0

    # Load assets once and reuse them (safe loader)
    screen_size = (600, 720)
    assets = load_assets(screen_size)
    loade()
    while True:
        # geef laatste score en high score mee aan menu
        choice = menu(music_on, high_score=high_score)

        if choice == "play":
            pygame.mixer.music.stop()
            main_game(balloon_skin, assets, music_on, sfx_on)

        elif choice == "settings":
            current_skin, music_on, sfx_on = settings(balloon_skin, music_on, sfx_on)

        #elif choice == "skins":
        #   balloon_skin = skin(balloon_skin)
            
        elif choice == "quit":
            break
        
        elif choice == "how":
            how_to_play()

    pygame.quit()

if __name__ == "__main__":
    main()