import pygame
import math

class PoliceCar:
    def __init__(self, x, y):
        self.lanes = [200, 400, 600]
        self.x = x
        self.y = y
        self.width = 70
        self.height = 120
        self.siren_flash = 0
        self.target_x = x
        self.move_speed = 12  # Police follows player lane changes
        
    def update(self, player_x, player_lane, target_y):
        # Police car stays behind player and follows their lane
        self.target_x = self.lanes[player_lane]
        
        # Smooth following for x position (lane changes)
        if self.x < self.target_x:
            self.x = min(self.x + self.move_speed, self.target_x)
        elif self.x > self.target_x:
            self.x = max(self.x - self.move_speed, self.target_x)
        
        # Update y position based on distance from player
        self.y = target_y
        
        self.siren_flash += 0.2
        
    def draw(self, screen):
        # Draw police car body (dark blue/black)
        car_color = (30, 40, 70)
        pygame.draw.rect(screen, car_color, 
                       (self.x - self.width // 2, self.y, self.width, self.height), 
                       border_radius=10)
        
        # Draw white stripe on sides
        pygame.draw.rect(screen, (255, 255, 255), 
                       (self.x - self.width // 2 + 5, self.y + 40, 8, 50))
        pygame.draw.rect(screen, (255, 255, 255), 
                       (self.x + self.width // 2 - 13, self.y + 40, 8, 50))
        
        # Draw "POLICE" text
        font = pygame.font.Font(None, 18)
        police_text = font.render("POLICE", True, (255, 255, 255))
        text_rect = police_text.get_rect(center=(self.x, self.y + 65))
        screen.blit(police_text, text_rect)
        
        # Draw windshield (light blue)
        pygame.draw.rect(screen, (100, 150, 200), 
                       (self.x - self.width // 2 + 10, self.y + 15, 
                        self.width - 20, 25))
        
        # Draw hood/front bumper (darker)
        pygame.draw.rect(screen, (20, 25, 50), 
                       (self.x - self.width // 2, self.y, self.width, 12), 
                       border_radius=5)
        
        # Draw flashing sirens on top
        siren_state = int(self.siren_flash) % 2
        if siren_state == 0:
            # Blue light
            pygame.draw.circle(screen, (0, 100, 255), 
                             (int(self.x - 15), int(self.y + 8)), 6)
            pygame.draw.circle(screen, (255, 0, 0), 
                             (int(self.x + 15), int(self.y + 8)), 6)
        else:
            # Red light
            pygame.draw.circle(screen, (255, 0, 0), 
                             (int(self.x - 15), int(self.y + 8)), 6)
            pygame.draw.circle(screen, (0, 100, 255), 
                             (int(self.x + 15), int(self.y + 8)), 6)
        
        # Draw headlights
        pygame.draw.circle(screen, (255, 255, 200), 
                         (int(self.x - 20), int(self.y + 5)), 4)
        pygame.draw.circle(screen, (255, 255, 200), 
                         (int(self.x + 20), int(self.y + 5)), 4)
        
        # Draw wheels
        pygame.draw.circle(screen, (40, 40, 40), 
                         (int(self.x - self.width // 2 + 8), int(self.y + 30)), 8)
        pygame.draw.circle(screen, (40, 40, 40), 
                         (int(self.x + self.width // 2 - 8), int(self.y + 30)), 8)
        pygame.draw.circle(screen, (40, 40, 40), 
                         (int(self.x - self.width // 2 + 8), int(self.y + 90)), 8)
        pygame.draw.circle(screen, (40, 40, 40), 
                         (int(self.x + self.width // 2 - 8), int(self.y + 90)), 8)
        
        # Draw front grill
        pygame.draw.rect(screen, (15, 15, 30), 
                       (self.x - 25, self.y + 3, 50, 8))
