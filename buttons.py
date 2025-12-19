import pygame

class Button:
    def __init__(self, x, y, w, h, text, font,
                 base_color=(0, 0, 0),
                 text_color=(255, 255, 255),
                 text_shadow_color=(0, 0, 0),
                 shadow_color=(0, 0, 0),
                 image=None,
                 dynamic_color=None
                 ):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.base_color = base_color
        self.text_color = text_color
        self.shadow_color = shadow_color
        self.text_shadow_color = text_shadow_color
        self.dynamic_color = dynamic_color
        self.image = image
        self.current_scale = 1.0

    def draw_gradient_rect(self, rect, start_color, end_color, vertical=True, border_radius=12):
        """Return a surface with gradient fill and rounded corners."""
        gradient_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)

        # Draw gradient
        if vertical:
            for i in range(rect.height):
                ratio = i / rect.height
                r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
                g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
                b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
                pygame.draw.line(gradient_surf, (r, g, b), (0, i), (rect.width, i))
        else:
            for i in range(rect.width):
                ratio = i / rect.width
                r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
                g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
                b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
                pygame.draw.line(gradient_surf, (r, g, b), (i, 0), (i, rect.height))

        # Mask with rounded rect
        mask = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(mask, (255, 255, 255, 255), mask.get_rect(), border_radius=border_radius)
        gradient_surf.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

        return gradient_surf

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mouse_pos)

        # Smooth hover animation
        target_scale = 1.025 if hovered else 1.0
        self.current_scale += (target_scale - self.current_scale) * 0.2

        new_w = int(self.rect.width * self.current_scale)
        new_h = int(self.rect.height * self.current_scale)
        enlarged_rect = pygame.Rect(0, 0, new_w, new_h)
        enlarged_rect.center = self.rect.center

        # --- Shadow ---
        if not self.image:
            shadow_offset = int(3 * self.current_scale)
            shadow_rect = enlarged_rect.copy()
            shadow_rect.move_ip(shadow_offset, shadow_offset)
            pygame.draw.rect(screen, self.shadow_color, shadow_rect, border_radius=12)

        # --- Gradient background ---
        if not self.image:
            base = self.dynamic_color if self.dynamic_color else self.base_color
            start_color = tuple(min(255, c + 60) for c in base)  # lighter top
            end_color   = tuple(max(0, c - 40) for c in base)    # darker bottom

            gradient_surf = self.draw_gradient_rect(enlarged_rect, start_color, end_color, vertical=True, border_radius=12)
            screen.blit(gradient_surf, enlarged_rect.topleft)

            # Outline
            pygame.draw.rect(screen, (0, 0, 0), enlarged_rect, width=2, border_radius=12)
        # --- Image button ---
        if self.image:
            scaled_img = pygame.transform.smoothscale(self.image, (enlarged_rect.width, enlarged_rect.height))
            screen.blit(scaled_img, enlarged_rect)
        else:
            # --- Text ---
            font_size = int(self.font.get_height() * self.current_scale)
            scaled_font = pygame.font.SysFont(
                self.font.get_name() if hasattr(self.font, "get_name") else None,
                font_size
            )
            text_surf = scaled_font.render(self.text, True, self.text_color)
            shadow_surf = scaled_font.render(self.text, True, self.text_shadow_color)
            shadow_rect = shadow_surf.get_rect(center=enlarged_rect.center)
            screen.blit(shadow_surf, shadow_rect.move(2, 2))
            screen.blit(text_surf, text_surf.get_rect(center=enlarged_rect.center))

    def is_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )
