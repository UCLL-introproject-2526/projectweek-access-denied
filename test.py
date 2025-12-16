import pygame

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

BALLOON_SPEED = 0.1
OBSTACLE_SPEED = 0.03

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Dikke Nantoe Teger")

font = pygame.font.Font(None, 40)


balloon = pygame.image.load("images/red-balloon_transparant.png").convert_alpha()
balloon_rect = balloon.get_rect()
balloon_rect.midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 10)
balloon_x = float(balloon_rect.x)

# spikes = pygame.image.load("images/spikes.png")
# spike_rect = spikes.get_rect()

obstacle_rect = pygame.Rect(300,50, 90, 25)
obstacle_y = float(obstacle_rect.y)
obstacle_x = float(obstacle_rect.x)

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
    if not balloon_rect.colliderect(obstacle_rect):
        obstacle_y += OBSTACLE_SPEED

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
        obstacle_rect.y = int(obstacle_y)
        obstacle_rect.x = int(obstacle_x)
        
        
        pygame.draw.rect(screen,(0,0,255), obstacle_rect)

        screen.blit(balloon, balloon_rect)
        
        pygame.display.flip()
    
    if balloon_rect.colliderect(obstacle_rect):
        screen.fill((255,0,0))
        draw_text("Game Over",font,(255,255,255),230 ,100)
        BALLOON_SPEED = 0
        obstacle_rect = pygame.Rect(obstacle_rect.x,obstacle_rect.y, 90, 25)
        pygame.draw.rect(screen,(0,0,255), obstacle_rect)
        screen.blit(balloon, balloon_rect)
        
        pygame.display.flip()


pygame.quit()