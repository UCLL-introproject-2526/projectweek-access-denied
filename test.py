import pygame

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Dikke Nantoe Teger")


obstacles = []
obstacle_rect = pygame.Rect(100,50, 90, 25)

balloon = pygame.image.load("images/red-balloon_transparant.png").convert_alpha()
image_rect = balloon.get_rect()

image_rect.midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 10)

balloon_x = float(image_rect.x)

obstacle_y = float(obstacle_rect.y)

speed = 0.1

font = pygame.font.Font(None, 40)

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
    if not image_rect.colliderect(obstacle_rect):
        obstacle_y += 0.03

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            balloon_x -= speed
        if keys[pygame.K_RIGHT]:
            balloon_x += speed

        
        if balloon_x < 0:
            balloon_x = 0
        if balloon_x > SCREEN_WIDTH - image_rect.width:
            balloon_x = SCREEN_WIDTH - image_rect.width

        image_rect.x = int(balloon_x)
        obstacle_rect.y = int(obstacle_y)
        
        
        pygame.draw.rect(screen,(0,0,255), obstacle_rect)

        screen.blit(balloon, image_rect)
        
        pygame.display.flip()
    
    if image_rect.colliderect(obstacle_rect):
        screen.fill((255,0,0))
        draw_text("Game Over",font,(255,255,255),200,300)
        speed = 0
        obstacle_rect = pygame.Rect(100,obstacle_rect.y, 90, 25)
        pygame.draw.rect(screen,(0,0,255), obstacle_rect)
        screen.blit(balloon, image_rect)
        
        pygame.display.flip()


pygame.quit()