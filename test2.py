import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))

image = pygame.image.load("images/red-balloon.png").convert_alpha()

# Create a rect that matches the image size
image_rect = image.get_rect()

# Set position
image_rect.topleft = (100, 150)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pos = pygame.mouse.get_pos()
    image_rect.center = pos

    screen.fill((30, 30, 30))

    # Draw image using its rect
    screen.blit(image, image_rect)

    pygame.display.flip()
