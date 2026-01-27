import pygame
import math

class Collectible:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 35
        self.height = 35
        self.color = (50, 150, 50)  # Green money bag
        self.animation_offset = 0
        
    def update(self, speed):
        self.y += speed
        self.animation_offset += 0.2
        
    def get_rect(self):
        return pygame.Rect(self.x - self.width // 2, self.y, self.width, self.height)
        
    def draw(self, screen):
        # Animated floating money bag effect
        offset = math.sin(self.animation_offset) * 5
        
        # Draw money bag body (green)
        bag_points = [
            (self.x, int(self.y + offset) - 8),  # Top
            (self.x - 15, int(self.y + offset) + 5),  # Left
            (self.x - 12, int(self.y + offset) + 18),  # Bottom left
            (self.x + 12, int(self.y + offset) + 18),  # Bottom right
            (self.x + 15, int(self.y + offset) + 5),  # Right
        ]
        pygame.draw.polygon(screen, self.color, bag_points)
        
        # Draw tied top (darker green)
        pygame.draw.rect(screen, (40, 120, 40), 
                       (self.x - 8, int(self.y + offset) - 12, 16, 8), 
                       border_radius=2)
        
        # Draw dollar sign
        font = pygame.font.Font(None, 28)
        dollar_text = font.render("$", True, (255, 255, 200))
        text_rect = dollar_text.get_rect(center=(self.x, int(self.y + offset) + 5))
        screen.blit(dollar_text, text_rect)
