import pygame
import math

class Multiplier:
    def __init__(self, x, y, multiplier_value=2):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.multiplier_value = multiplier_value  # 2x, 3x, etc.
        self.animation_offset = 0
        
        # Colors based on multiplier value
        if multiplier_value == 2:
            self.color = (50, 150, 255)  # Blue for 2x
        elif multiplier_value == 3:
            self.color = (255, 100, 255)  # Purple for 3x
        else:
            self.color = (255, 200, 50)  # Gold for higher
        
    def update(self, speed):
        self.y += speed
        self.animation_offset += 0.3
        
    def get_rect(self):
        return pygame.Rect(self.x - self.width // 2, self.y, self.width, self.height)
        
    def draw(self, screen):
        # Animated spinning multiplier effect
        offset = math.sin(self.animation_offset) * 8
        rotation = self.animation_offset * 50
        
        # Draw outer glow circle
        for i in range(3, 0, -1):
            alpha_surface = pygame.Surface((self.width + i*6, self.height + i*6), pygame.SRCALPHA)
            glow_color = (*self.color, 50)
            pygame.draw.circle(alpha_surface, glow_color, 
                             (self.width // 2 + i*3, self.height // 2 + i*3), 
                             20 + i*3)
            screen.blit(alpha_surface, 
                       (self.x - self.width // 2 - i*3, int(self.y + offset) - i*3))
        
        # Draw main circle
        pygame.draw.circle(screen, self.color, 
                         (int(self.x), int(self.y + offset)), 22)
        
        # Draw inner lighter circle
        lighter_color = tuple(min(c + 80, 255) for c in self.color)
        pygame.draw.circle(screen, lighter_color, 
                         (int(self.x), int(self.y + offset)), 18)
        
        # Draw multiplier text
        font = pygame.font.Font(None, 32)
        mult_text = font.render(f"{self.multiplier_value}X", True, (255, 255, 255))
        text_rect = mult_text.get_rect(center=(self.x, int(self.y + offset)))
        
        # Draw text shadow
        shadow_text = font.render(f"{self.multiplier_value}X", True, (0, 0, 0))
        shadow_rect = shadow_text.get_rect(center=(self.x + 2, int(self.y + offset) + 2))
        screen.blit(shadow_text, shadow_rect)
        screen.blit(mult_text, text_rect)
