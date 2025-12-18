import pygame

class Button:
    def __init__(self, x, y, width, height, text, font, color=(100, 100, 200)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.dynamic_color = color
        self.hovered = False
        self.pressed = False

    # Hover check
    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    # Klik check
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered(pygame.mouse.get_pos()):
            return True
        return False

    # Tekenen van de knop
    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.is_hovered(mouse_pos)

        # --- Offset voor 3D-effect ---
        offset = 4 if self.hovered else 2

        # --- Achtergrondschaduw (donkerder) ---
        shadow_color = (30, 30, 30)
        pygame.draw.rect(screen, shadow_color,
                        (self.rect.x + offset, self.rect.y + offset, self.rect.width, self.rect.height),
                        border_radius=8)

        # --- Lichte rand boven/links ---
        top_left_color = (255, 255, 255)
        pygame.draw.rect(screen, top_left_color,
                        (self.rect.x, self.rect.y, self.rect.width, self.rect.height),
                        border_radius=8)

        # --- Body van de knop ---
        body_color = self.dynamic_color
        if self.hovered:
            # Lichter maken bij hover
            body_color = tuple(min(255, c + 80) for c in body_color)

        # Gradient voor bol effect
        for i in range(self.rect.height):
            ratio = i / self.rect.height
            color = (
                int(body_color[0] * (1 - ratio) + body_color[0]*0.8 * ratio),
                int(body_color[1] * (1 - ratio) + body_color[1]*0.8 * ratio),
                int(body_color[2] * (1 - ratio) + body_color[2]*0.8 * ratio)
            )
            pygame.draw.line(screen, color,
                            (self.rect.x + 1, self.rect.y + 1 + i),
                            (self.rect.x + self.rect.width - 2, self.rect.y + 1 + i))

        # --- Tekst centreren ---
        text_surf = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
