"""
Rose power-up for Valentine's Pac-Man game.
When collected, Pac-Man shoots hearts for a limited duration.
"""

import pygame
import random
import math
from config import (
    TILE_SIZE, MAZE_OFFSET_X, MAZE_OFFSET_Y,
    ROSE_SPAWN_INTERVAL
)


class Rose:
    """Rose power-up that enables heart shooting."""
    
    def __init__(self):
        self.x = 0
        self.y = 0
        self.grid_x = 0
        self.grid_y = 0
        self.active = False
        self.last_spawn_time = 0
        self.radius = TILE_SIZE // 2 - 2
        self.animation_offset = 0
    
    def spawn(self, maze, current_time):
        """Spawn rose at a random empty position."""
        empty_positions = maze.get_empty_positions()
        
        # Filter out positions too close to ghost house
        valid_positions = [
            (x, y) for x, y in empty_positions
            if not (11 <= x <= 16 and 12 <= y <= 16)  # Avoid ghost house area
        ]
        
        if valid_positions:
            self.grid_x, self.grid_y = random.choice(valid_positions)
            self.x = MAZE_OFFSET_X + self.grid_x * TILE_SIZE + TILE_SIZE // 2
            self.y = MAZE_OFFSET_Y + self.grid_y * TILE_SIZE + TILE_SIZE // 2
            self.active = True
            self.last_spawn_time = current_time
    
    def update(self, current_time):
        """Update rose animation."""
        if self.active:
            # Floating animation
            self.animation_offset = math.sin(current_time / 200) * 3
    
    def check_spawn(self, maze, current_time):
        """Check if it's time to spawn a new rose."""
        if not self.active:
            if current_time - self.last_spawn_time > ROSE_SPAWN_INTERVAL:
                self.spawn(maze, current_time)
    
    def collect(self):
        """Collect the rose."""
        if self.active:
            self.active = False
            return True
        return False
    
    def get_rect(self):
        """Get rose's collision rectangle."""
        return pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )
    
    def collides_with(self, other_rect):
        """Check collision with another rectangle."""
        if not self.active:
            return False
        return self.get_rect().colliderect(other_rect)
    
    def draw(self, screen):
        """Draw the rose on the screen."""
        if not self.active:
            return
        
        x = int(self.x)
        y = int(self.y + self.animation_offset)
        
        # Draw rose stem
        stem_color = (34, 139, 34)  # Forest green
        pygame.draw.line(screen, stem_color, 
                        (x, y + 4), (x, y + 10), 2)
        
        # Draw small leaves
        leaf_points_left = [(x - 2, y + 6), (x - 5, y + 4), (x - 2, y + 8)]
        leaf_points_right = [(x + 2, y + 7), (x + 5, y + 5), (x + 2, y + 9)]
        pygame.draw.polygon(screen, stem_color, leaf_points_left)
        pygame.draw.polygon(screen, stem_color, leaf_points_right)
        
        # Draw rose petals (layered circles for flower effect)
        petal_colors = [
            (255, 20, 60),   # Crimson (outer)
            (255, 0, 80),    # Deep pink
            (220, 20, 60),   # Crimson variant
            (255, 105, 180), # Hot pink (center)
        ]
        
        # Outer petals
        for i in range(5):
            angle = i * (2 * math.pi / 5) + self.animation_offset / 50
            px = x + 5 * math.cos(angle)
            py = y - 2 + 5 * math.sin(angle)
            pygame.draw.circle(screen, petal_colors[0], (int(px), int(py)), 4)
        
        # Middle petals
        for i in range(5):
            angle = i * (2 * math.pi / 5) + math.pi / 5 + self.animation_offset / 50
            px = x + 3 * math.cos(angle)
            py = y - 2 + 3 * math.sin(angle)
            pygame.draw.circle(screen, petal_colors[1], (int(px), int(py)), 3)
        
        # Center of rose
        pygame.draw.circle(screen, petal_colors[3], (x, y - 2), 3)
        
        # Add sparkle effect
        sparkle_offset = (pygame.time.get_ticks() // 100) % 8
        if sparkle_offset < 4:
            sparkle_x = x + 6 - sparkle_offset
            sparkle_y = y - 8 + sparkle_offset
            pygame.draw.circle(screen, (255, 255, 200), 
                             (sparkle_x, sparkle_y), 2)


class RoseManager:
    """Manages rose spawning and collection."""
    
    def __init__(self):
        self.rose = Rose()
        self.spawn_interval = ROSE_SPAWN_INTERVAL
    
    def reset(self):
        """Reset the rose manager."""
        self.rose = Rose()
    
    def update(self, maze, pacman, current_time):
        """Update rose state and check for collection."""
        # Check if rose should spawn
        self.rose.check_spawn(maze, current_time)
        
        # Update rose animation
        self.rose.update(current_time)
        
        # Check for collection
        if self.rose.active and self.rose.collides_with(pacman.get_rect()):
            self.rose.collect()
            return True  # Rose was collected
        
        return False
    
    def draw(self, screen):
        """Draw the rose."""
        self.rose.draw(screen)
