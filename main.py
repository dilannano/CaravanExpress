import pygame
import sys
import random
from player import Player
from obstacle import Obstacle
from collectible import Collectible
from background import Background
from police import PoliceCar
from multiplier import Multiplier

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Police Chase - Escape the Cops!")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 72)
        self.small_font = pygame.font.Font(None, 24)
        self.reset_game()
        
    def reset_game(self):
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
        self.police = PoliceCar(SCREEN_WIDTH // 2, SCREEN_HEIGHT + 50)  # Start further back
        self.obstacles = []
        self.collectibles = []
        self.multipliers = []
        self.background = Background(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.score = 0
        self.distance = 0
        self.game_speed = 4  # Slower starting speed
        self.game_over = False
        self.spawn_timer = 0
        self.collectible_timer = 0
        self.multiplier_timer = 0
        self.hit_count = 0  # Track number of obstacles hit
        self.warning_active = False
        self.time_since_last_hit = 0  # Timer for the 7-second grace period
        self.warning_flash = 0
        self.police_distance = 200  # Distance between player and police (in pixels)
        self.normal_police_distance = 200  # Normal safe distance
        self.close_police_distance = 80  # Close/danger distance
        
        # Multiplier system
        self.score_multiplier = 1
        self.multiplier_time_remaining = 0
        self.multiplier_duration = 600  # 10 seconds at 60 FPS
        
    def spawn_obstacle(self):
        lanes = [200, 400, 600]
        lane = random.choice(lanes)
        obstacle_type = random.choice(['traffic_light', 'stop_sign', 'roadblock'])
        self.obstacles.append(Obstacle(lane, -50, obstacle_type))
        
    def spawn_collectible(self):
        lanes = [200, 400, 600]
        lane = random.choice(lanes)
        self.collectibles.append(Collectible(lane, -50))
        
    def spawn_multiplier(self):
        lanes = [200, 400, 600]
        lane = random.choice(lanes)
        # Random multiplier value: 70% chance of 2x, 25% chance of 3x, 5% chance of 5x
        rand = random.random()
        if rand < 0.70:
            mult_value = 2
        elif rand < 0.95:
            mult_value = 3
        else:
            mult_value = 5
        self.multipliers.append(Multiplier(lane, -50, mult_value))
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if self.game_over and event.key == pygame.K_SPACE:
                    self.reset_game()
                elif not self.game_over:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.player.move_left()
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.player.move_right()
        return True
        
    def update(self):
        if self.game_over:
            return
            
        # Update player
        self.player.update()
        
        # Update background
        self.background.update(self.game_speed)
        
        # Update police distance based on hit status
        target_distance = self.close_police_distance if self.warning_active else self.normal_police_distance
        
        # Smoothly transition police distance
        if self.police_distance < target_distance:
            self.police_distance = min(self.police_distance + 2, target_distance)
        elif self.police_distance > target_distance:
            self.police_distance = max(self.police_distance - 3, target_distance)
        
        # Update police car position based on distance
        police_y = self.player.y + self.police_distance
        self.police.update(self.player.x, self.player.current_lane, police_y)
        
        # Update warning flash
        self.warning_flash += 0.15
        
        # Update multiplier timer
        if self.multiplier_time_remaining > 0:
            self.multiplier_time_remaining -= 1
            if self.multiplier_time_remaining <= 0:
                self.score_multiplier = 1  # Reset to normal
        
        # Update timer since last hit (7 second grace period)
        if self.hit_count > 0:
            self.time_since_last_hit += 1
            # 7 seconds at 60 FPS = 420 frames
            if self.time_since_last_hit >= 420:
                # Reset hits - you escaped the cops!
                self.hit_count = 0
                self.warning_active = False
                self.time_since_last_hit = 0
        
        # Spawn obstacles - slower spawn rate
        self.spawn_timer += 1
        # Slower progression: start at 90 frames, min at 50 frames
        spawn_delay = 90 - min(self.distance // 1000, 40)
        if self.spawn_timer > spawn_delay:
            self.spawn_obstacle()
            self.spawn_timer = 0
            
        # Spawn collectibles
        self.collectible_timer += 1
        if self.collectible_timer > 150:  # Less frequent collectibles
            self.spawn_collectible()
            self.collectible_timer = 0
            
        # Spawn multipliers (rare power-ups)
        self.multiplier_timer += 1
        if self.multiplier_timer > 400:  # Every ~6-7 seconds
            self.spawn_multiplier()
            self.multiplier_timer = 0
            
        # Update obstacles
        for obstacle in self.obstacles[:]:
            obstacle.update(self.game_speed)
            if obstacle.y > SCREEN_HEIGHT:
                self.obstacles.remove(obstacle)
                self.score += 10 * self.score_multiplier  # Apply multiplier!
            # Check collision
            elif self.player.collides_with(obstacle):
                self.obstacles.remove(obstacle)
                self.hit_count += 1
                self.time_since_last_hit = 0  # Reset the timer
                
                if self.hit_count == 1:
                    # First hit - warning!
                    self.warning_active = True
                elif self.hit_count >= 2:
                    # Second hit - game over!
                    self.game_over = True
                
        # Update collectibles (money bags)
        for collectible in self.collectibles[:]:
            collectible.update(self.game_speed)
            if collectible.y > SCREEN_HEIGHT:
                self.collectibles.remove(collectible)
            elif self.player.collects(collectible):
                self.collectibles.remove(collectible)
                self.score += 50 * self.score_multiplier  # Apply multiplier!
                
        # Update multipliers
        for multiplier in self.multipliers[:]:
            multiplier.update(self.game_speed)
            if multiplier.y > SCREEN_HEIGHT:
                self.multipliers.remove(multiplier)
            elif self.player.collects(multiplier):
                self.multipliers.remove(multiplier)
                # Activate or stack multiplier
                if self.multiplier_time_remaining > 0:
                    # Stack multipliers (max 5x)
                    self.score_multiplier = min(self.score_multiplier + multiplier.multiplier_value - 1, 5)
                else:
                    self.score_multiplier = multiplier.multiplier_value
                self.multiplier_time_remaining = self.multiplier_duration  # Reset timer
                
        # Update distance and speed - much slower progression
        self.distance += self.game_speed
        # Slower speed increase: starts at 4, increases more gradually
        self.game_speed = 4 + self.distance // 2000
        
    def draw(self):
        # Draw background
        self.background.draw(self.screen)
        
        # Draw police car (behind player)
        self.police.draw(self.screen)
        
        # Draw player
        self.player.draw(self.screen)
        
        # Draw obstacles
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
            
        # Draw collectibles
        for collectible in self.collectibles:
            collectible.draw(self.screen)
            
        # Draw multipliers
        for multiplier in self.multipliers:
            multiplier.draw(self.screen)
            
        # Draw score and distance
        score_color = WHITE
        if self.score_multiplier > 1:
            # Flash the score in color when multiplier is active
            if self.score_multiplier == 2:
                score_color = (100, 200, 255)
            elif self.score_multiplier == 3:
                score_color = (255, 150, 255)
            else:
                score_color = (255, 220, 100)
        
        score_text = self.font.render(f"Score: {self.score}", True, score_color)
        distance_text = self.font.render(f"Distance: {self.distance}m", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(distance_text, (10, 50))
        
        # Draw multiplier status
        if self.multiplier_time_remaining > 0:
            time_remaining_sec = self.multiplier_time_remaining / 60
            mult_color = score_color
            mult_text = self.large_font.render(f"{self.score_multiplier}X", True, mult_color)
            timer_text = self.small_font.render(f"{time_remaining_sec:.1f}s", True, WHITE)
            
            self.screen.blit(mult_text, (SCREEN_WIDTH - 100, 10))
            self.screen.blit(timer_text, (SCREEN_WIDTH - 80, 65))
        
        # Draw warning system
        if self.warning_active and self.hit_count == 1:
            # Calculate time remaining (7 seconds - current time)
            time_remaining = max(0, 7 - (self.time_since_last_hit / 60))
            
            # Flash red warning
            if int(self.warning_flash * 2) % 2 == 0:
                warning_text = self.large_font.render("WARNING!", True, RED)
                self.screen.blit(warning_text, (SCREEN_WIDTH // 2 - warning_text.get_width() // 2, 80))
            
            # Show timer and instruction
            timer_text = self.font.render(f"Avoid obstacles for {time_remaining:.1f}s!", True, (255, 200, 0))
            hit_text = self.small_font.render("One more hit and you're BUSTED!", True, WHITE)
            self.screen.blit(timer_text, (SCREEN_WIDTH // 2 - timer_text.get_width() // 2, 140))
            self.screen.blit(hit_text, (SCREEN_WIDTH // 2 - hit_text.get_width() // 2, 170))
        
        # Draw game over screen
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.large_font.render("BUSTED!", True, RED)
            caught_text = self.font.render("The police caught you!", True, WHITE)
            final_score = self.font.render(f"Final Score: {self.score}", True, WHITE)
            restart_text = self.font.render("Press SPACE to try again", True, WHITE)
            
            self.screen.blit(game_over_text, 
                           (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 180))
            self.screen.blit(caught_text, 
                           (SCREEN_WIDTH // 2 - caught_text.get_width() // 2, 260))
            self.screen.blit(final_score, 
                           (SCREEN_WIDTH // 2 - final_score.get_width() // 2, 310))
            self.screen.blit(restart_text, 
                           (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 360))
        
        pygame.display.flip()
        
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
