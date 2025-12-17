import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 720

BALLOON_SPEED = 0.1
OBSTACLE_SPEED = 0.1

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Dikke Nantoe Teger")

font = pygame.font.Font(None, 40)

BG = pygame.image.load("images/background.png").convert_alpha()

balloon = pygame.image.load("images/balloon.png").convert_alpha()
balloon_rect = balloon.get_rect()
balloon_rect.midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 10)
balloon_x = float(balloon_rect.x)

balloon_prepop = pygame.image.load("images/balloon_prepop.png")
balloon_prepop_rect = balloon_prepop.get_rect()
balloon_prepop_rect.midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 10)
balloon_prepop_x = float(balloon_prepop_rect.x)

balloon_pop = pygame.image.load("images/balloon_pop.png")
balloon_pop_rect = balloon_pop.get_rect()
balloon_pop_rect.midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 10)
balloon_pop_x = float(balloon_pop_rect.x)

spikes_locations = [100, 400]
spikes = pygame.image.load("images/spikes.png")
spike_rect = spikes.get_rect()
spike_rect.midtop = (random.choice(spikes_locations), 0)
spike_y = float(spike_rect.y)
spike_x = float(spike_rect.x)

# obstacle_locations = [100, 500]
# obstacle_rect = pygame.Rect(random.choice(obstacle_locations),50, 90, 25)
# obstacle_y = float(obstacle_rect.y)
# obstacle_x = float(obstacle_rect.x)

death_screen = pygame.image.load("images/death_screen.png")
death_screen = pygame.transform.scale(death_screen,(600, 720))

death_shown = 0
BG = ((0,0,0))

text_col = (0,0,0)
def draw_text(text, font, text_col, x, y):
    text_msg = font.render(text, True, text_col)
    screen.blit(text_msg, (x, y))

running = True
while running:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    

    screen.fill((0,0,0))

    col = (0, 255, 0)
    if not balloon_rect.colliderect(spike_rect):
        spike_y += OBSTACLE_SPEED

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            balloon_x -= BALLOON_SPEED
        if keys[pygame.K_RIGHT]:
            balloon_x += BALLOON_SPEED

        
        if balloon_x < 0:
            balloon_x = 0
        if balloon_x > SCREEN_WIDTH - balloon_rect.width:
            balloon_x = SCREEN_WIDTH - balloon_rect.width

        balloon_rect.x = int(balloon_x)
        balloon_prepop_rect.x = int(balloon_prepop_x)
        balloon_pop_rect.x = int(balloon_pop_x)
        spike_rect.y = int(spike_y)
        spike_rect.x = int(spike_x)
        
        
        # pygame.draw.rect(screen,(0,0,255), obstacle_rect)
        screen.blit(spikes, spike_rect)
        screen.blit(balloon, balloon_rect)
        
        pygame.display.flip()
    
    if balloon_rect.colliderect(spike_rect):
        BALLOON_SPEED = 0
        # obstacle_rect = pygame.Rect(obstacle_rect.x,obstacle_rect.y, 90, 25)
        # pygame.draw.rect(screen,(0,0,255), obstacle_rect)
        if death_shown != 1:
            screen.blit(balloon_prepop, balloon_rect)
            screen.blit(spikes, spike_rect)
            death_shown += 1
            pygame.display.flip()
            pygame.time.wait(1000)
            screen.blit(balloon_pop, balloon_rect)
            screen.blit(spikes, spike_rect)
            pygame.display.flip()
            pygame.time.wait(500)


        screen.blit(death_screen,(0,0))
        pygame.display.flip()


pygame.quit()