import pygame

class Background:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.color = (30, 30, 50)
        
        # Road lanes
        self.lanes = [200, 400, 600]
        self.lane_width = 120
        
        # Road markings
        self.road_markings = []
        for i in range(10):
            self.road_markings.append(i * 100 - 50)
            
    def update(self, speed):
        # Update road markings
        for i in range(len(self.road_markings)):
            self.road_markings[i] += speed
            if self.road_markings[i] > self.height:
                self.road_markings[i] = -50
                
    def draw(self, screen):
        # Draw background
        screen.fill(self.color)
        
        # Draw road lanes
        for lane in self.lanes:
            pygame.draw.rect(screen, (60, 60, 80), 
                           (lane - self.lane_width // 2, 0, 
                            self.lane_width, self.height))
        
        # Draw lane dividers
        for lane in self.lanes[:-1]:
            for marking_y in self.road_markings:
                pygame.draw.rect(screen, (255, 255, 255), 
                               (lane + self.lane_width // 2 - 5, marking_y, 
                                10, 40))
        
        # Draw road edges
        pygame.draw.rect(screen, (100, 100, 120), 
                       (self.lanes[0] - self.lane_width // 2 - 10, 0, 10, self.height))
        pygame.draw.rect(screen, (100, 100, 120), 
                       (self.lanes[-1] + self.lane_width // 2, 0, 10, self.height))
