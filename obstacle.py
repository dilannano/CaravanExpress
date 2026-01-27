import pygame

class Obstacle:
    def __init__(self, x, y, obstacle_type='traffic_light'):
        self.x = x
        self.y = y
        self.obstacle_type = obstacle_type
        
        # Different sizes for different obstacles
        if obstacle_type == 'traffic_light':
            self.width = 50
            self.height = 100
            self.color = (100, 100, 100)
        elif obstacle_type == 'stop_sign':
            self.width = 60
            self.height = 80
            self.color = (220, 20, 20)
        else:  # roadblock
            self.width = 70
            self.height = 50
            self.color = (255, 140, 0)
            
    def update(self, speed):
        self.y += speed
        
    def get_rect(self):
        return pygame.Rect(self.x - self.width // 2, self.y, self.width, self.height)
        
    def draw(self, screen):
        if self.obstacle_type == 'traffic_light':
            # Draw traffic light pole
            pygame.draw.rect(screen, (80, 80, 80), 
                           (self.x - 8, self.y + 50, 16, self.height - 50))
            
            # Draw traffic light box
            pygame.draw.rect(screen, (60, 60, 60), 
                           (self.x - self.width // 2, self.y, self.width, 55), 
                           border_radius=5)
            
            # Draw three lights (RED on top - that's why it's illegal to run!)
            pygame.draw.circle(screen, (255, 50, 50), 
                             (int(self.x), int(self.y + 12)), 10)  # RED
            pygame.draw.circle(screen, (100, 80, 0), 
                             (int(self.x), int(self.y + 28)), 9)   # Yellow (dim)
            pygame.draw.circle(screen, (0, 80, 0), 
                             (int(self.x), int(self.y + 43)), 9)   # Green (dim)
                
        elif self.obstacle_type == 'stop_sign':
            # Draw octagonal STOP sign
            # Draw pole
            pygame.draw.rect(screen, (150, 150, 150), 
                           (self.x - 6, self.y + 50, 12, 30))
            
            # Draw octagon (simplified as rect with corners)
            sign_size = 45
            pygame.draw.rect(screen, (220, 20, 20), 
                           (self.x - sign_size // 2, self.y, sign_size, sign_size), 
                           border_radius=5)
            
            # Draw white border
            pygame.draw.rect(screen, (255, 255, 255), 
                           (self.x - sign_size // 2, self.y, sign_size, sign_size), 
                           width=3, border_radius=5)
            
            # Draw "STOP" text
            font = pygame.font.Font(None, 28)
            stop_text = font.render("STOP", True, (255, 255, 255))
            text_rect = stop_text.get_rect(center=(self.x, self.y + sign_size // 2))
            screen.blit(stop_text, text_rect)
                           
        else:  # roadblock
            # Draw construction/police roadblock
            # Draw base
            pygame.draw.rect(screen, (100, 100, 100), 
                           (self.x - self.width // 2 - 5, self.y + 35, 
                            self.width + 10, 15))
            
            # Draw barrier with police/caution stripes
            pygame.draw.rect(screen, self.color, 
                           (self.x - self.width // 2, self.y, self.width, 35), 
                           border_radius=3)
            
            # Draw diagonal stripes
            stripe_color = (255, 255, 255)
            for i in range(-self.width, self.width, 20):
                start_x = self.x - self.width // 2 + i
                end_x = start_x + 15
                pygame.draw.polygon(screen, stripe_color, [
                    (start_x, self.y),
                    (end_x, self.y),
                    (end_x + 10, self.y + 35),
                    (start_x + 10, self.y + 35)
                ])
            
            # Draw warning lights
            pygame.draw.circle(screen, (255, 200, 0), 
                             (int(self.x - self.width // 3), int(self.y + 17)), 6)
            pygame.draw.circle(screen, (255, 200, 0), 
                             (int(self.x + self.width // 3), int(self.y + 17)), 6)
