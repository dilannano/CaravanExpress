import pygame

class Player:
    def __init__(self, x, y):
        self.lanes = [200, 400, 600]
        self.current_lane = 1
        self.x = self.lanes[self.current_lane]
        self.y = y
        self.width = 50
        self.height = 80
        self.color = (240, 240, 245)  # White/light gray for minivan
        
        # No jumping or sliding - Temple Run style
        
        # Animation
        self.target_x = self.x
        self.move_speed = 15
        
    def move_left(self):
        if self.current_lane > 0:
            self.current_lane -= 1
            self.target_x = self.lanes[self.current_lane]
            
    def move_right(self):
        if self.current_lane < len(self.lanes) - 1:
            self.current_lane += 1
            self.target_x = self.lanes[self.current_lane]
            
    def update(self):
        # Smooth lane transition
        if self.x < self.target_x:
            self.x = min(self.x + self.move_speed, self.target_x)
        elif self.x > self.target_x:
            self.x = max(self.x - self.move_speed, self.target_x)
                
    def get_rect(self):
        return pygame.Rect(self.x - self.width // 2, self.y, self.width, self.height)
        
    def collides_with(self, obstacle):
        player_rect = self.get_rect()
        obstacle_rect = obstacle.get_rect()
        return player_rect.colliderect(obstacle_rect)
        
    def collects(self, collectible):
        player_rect = self.get_rect()
        collectible_rect = collectible.get_rect()
        return player_rect.colliderect(collectible_rect)
        
    def draw(self, screen):
        # Draw simple top-down view of white Dodge Caravan
        
        # Main car body (rounded rectangle for minivan shape)
        car_color = (240, 240, 245)  # White
        pygame.draw.rect(screen, car_color, 
                       (self.x - self.width // 2, self.y, self.width, self.height), 
                       border_radius=8)
        
        # Draw darker outline
        pygame.draw.rect(screen, (180, 180, 190), 
                       (self.x - self.width // 2, self.y, self.width, self.height), 
                       width=2, border_radius=8)
        
        # Draw windshield (front window - darker blue)
        windshield_color = (80, 120, 150)
        pygame.draw.rect(screen, windshield_color, 
                       (self.x - self.width // 2 + 8, self.y + self.height - 20, 
                        self.width - 16, 15), border_radius=3)
        
        # Draw rear window
        pygame.draw.rect(screen, windshield_color, 
                       (self.x - self.width // 2 + 8, self.y + 5, 
                        self.width - 16, 12), border_radius=3)
        
        # Draw side mirrors
        mirror_color = (200, 200, 210)
        pygame.draw.rect(screen, mirror_color, 
                       (self.x - self.width // 2 - 4, self.y + 40, 4, 8))
        pygame.draw.rect(screen, mirror_color, 
                       (self.x + self.width // 2, self.y + 40, 4, 8))
        
        # Draw headlights (front)
        pygame.draw.circle(screen, (255, 255, 200), 
                         (int(self.x - 15), int(self.y + self.height - 5)), 3)
        pygame.draw.circle(screen, (255, 255, 200), 
                         (int(self.x + 15), int(self.y + self.height - 5)), 3)
        
        # Draw taillights (rear - red)
        pygame.draw.circle(screen, (200, 50, 50), 
                         (int(self.x - 15), int(self.y + 5)), 3)
        pygame.draw.circle(screen, (200, 50, 50), 
                         (int(self.x + 15), int(self.y + 5)), 3)
