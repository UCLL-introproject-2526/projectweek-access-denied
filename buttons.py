import pygame

class Button:
    def __init__(self, x, y, w, h, text, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.base_color = (0, 0, 0, 150)
        self.hover_color = (50, 50, 50, 150)
        self.text_color = (255, 255, 255, 150)
        self.dynamic_color = None

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        color = self.dynamic_color if self.dynamic_color else self.base_color
        if self.rect.collidepoint(mouse_pos):
            color = tuple(min(255, c+40) for c in color)
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        text_surf = self.font.render(self.text, True, self.text_color)
        screen.blit(text_surf, text_surf.get_rect(center=self.rect.center))

    def is_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )
