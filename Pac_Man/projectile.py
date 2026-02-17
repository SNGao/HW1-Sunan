"""
Heart projectiles for Valentine's Pac-Man game.
Hearts are shot when Pac-Man is powered up by the rose.
"""

import pygame
import math
from config import (
    TILE_SIZE, MAZE_OFFSET_X, MAZE_OFFSET_Y,
    HEART_SPEED, HEART_COLOR, HEART_FIRE_RATE
)


class Heart:
    """Heart projectile that eliminates ghosts."""
    
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = HEART_SPEED
        self.size = 8
        self.active = True
        self.trail = []  # Trail effect positions
        self.max_trail_length = 5
    
    def update(self, maze):
        """Update heart position."""
        if not self.active:
            return
        
        # Add current position to trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)
        
        # Move heart
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed
        
        # Check wall collision
        grid_x = int((self.x - MAZE_OFFSET_X) // TILE_SIZE)
        grid_y = int((self.y - MAZE_OFFSET_Y) // TILE_SIZE)
        
        if maze.is_wall(grid_x, grid_y):
            self.active = False
            return
        
        # Check bounds
        if (self.x < MAZE_OFFSET_X or 
            self.x > MAZE_OFFSET_X + maze.width * TILE_SIZE or
            self.y < MAZE_OFFSET_Y or 
            self.y > MAZE_OFFSET_Y + maze.height * TILE_SIZE):
            self.active = False
    
    def get_rect(self):
        """Get heart's collision rectangle."""
        return pygame.Rect(
            self.x - self.size // 2,
            self.y - self.size // 2,
            self.size,
            self.size
        )
    
    def collides_with_ghost(self, ghost):
        """Check collision with a ghost."""
        if not self.active or not ghost.alive:
            return False
        return self.get_rect().colliderect(ghost.get_rect())
    
    def draw(self, screen):
        """Draw the heart on the screen."""
        if not self.active:
            return
        
        # Draw trail
        for i, (tx, ty) in enumerate(self.trail):
            alpha = (i + 1) / len(self.trail)
            trail_size = int(self.size * alpha * 0.6)
            trail_color = (
                int(255 * alpha),
                int(105 * alpha),
                int(180 * alpha)
            )
            self._draw_heart_shape(screen, int(tx), int(ty), 
                                   trail_size, trail_color)
        
        # Draw main heart
        self._draw_heart_shape(screen, int(self.x), int(self.y), 
                              self.size, HEART_COLOR)
        
        # Add glow effect
        glow_color = (255, 200, 220)
        pygame.draw.circle(screen, glow_color, 
                          (int(self.x), int(self.y - 1)), 2)
    
    def _draw_heart_shape(self, screen, x, y, size, color):
        """Draw a heart shape at the given position."""
        # Heart made of two circles and a triangle
        half = size // 2
        quarter = size // 4
        
        # Top circles
        pygame.draw.circle(screen, color, (x - quarter, y - quarter), half)
        pygame.draw.circle(screen, color, (x + quarter, y - quarter), half)
        
        # Bottom triangle
        points = [
            (x - half, y - quarter + 2),
            (x + half, y - quarter + 2),
            (x, y + half)
        ]
        pygame.draw.polygon(screen, color, points)


class HeartManager:
    """Manages heart projectile creation and updates."""
    
    def __init__(self):
        self.hearts = []
        self.last_fire_time = 0
        self.fire_rate = HEART_FIRE_RATE
    
    def reset(self):
        """Reset all hearts."""
        self.hearts = []
        self.last_fire_time = 0
    
    def fire(self, pacman, current_time):
        """Fire a heart from Pac-Man if powered up and fire rate allows."""
        if not pacman.powered_up:
            return
        
        if current_time - self.last_fire_time < self.fire_rate:
            return
        
        # Don't fire if not moving
        if pacman.facing_direction == (0, 0):
            return
        
        # Create new heart
        heart = Heart(pacman.x, pacman.y, pacman.facing_direction)
        self.hearts.append(heart)
        self.last_fire_time = current_time
    
    def update(self, maze, ghosts, current_time):
        """Update all hearts and check collisions with ghosts."""
        ghosts_killed = []
        
        for heart in self.hearts[:]:  # Iterate over copy
            heart.update(maze)
            
            # Check ghost collisions
            for ghost in ghosts:
                if heart.collides_with_ghost(ghost):
                    ghost.kill(current_time)
                    ghosts_killed.append(ghost)
                    heart.active = False
                    break
            
            # Remove inactive hearts
            if not heart.active:
                self.hearts.remove(heart)
        
        return ghosts_killed
    
    def draw(self, screen):
        """Draw all hearts."""
        for heart in self.hearts:
            heart.draw(screen)
