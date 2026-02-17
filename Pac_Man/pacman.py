"""
Pac-Man character class for Valentine's Pac-Man game.
Handles movement, power-up state, and rendering.
"""

import pygame
import math
from config import (
    TILE_SIZE, MAZE_OFFSET_X, MAZE_OFFSET_Y,
    PACMAN_SPEED, PACMAN_COLOR, POWERUP_DURATION,
    UP, DOWN, LEFT, RIGHT, NONE, HEART_COLOR
)


class PacMan:
    """Pac-Man character with movement and power-up abilities."""
    
    def __init__(self, start_grid_x, start_grid_y):
        # Position (pixel coordinates - center of Pac-Man)
        self.start_grid_x = start_grid_x
        self.start_grid_y = start_grid_y
        self.reset()
        
    def reset(self):
        """Reset Pac-Man to starting position and state."""
        self.x = MAZE_OFFSET_X + self.start_grid_x * TILE_SIZE + TILE_SIZE // 2
        self.y = MAZE_OFFSET_Y + self.start_grid_y * TILE_SIZE + TILE_SIZE // 2
        self.direction = NONE
        self.next_direction = NONE
        self.facing_direction = RIGHT  # Direction for shooting hearts
        self.speed = PACMAN_SPEED
        self.radius = TILE_SIZE // 2 - 2
        
        # Power-up state
        self.powered_up = False
        self.powerup_start_time = 0
        
        # Animation
        self.mouth_angle = 45
        self.mouth_opening = True
        self.animation_speed = 5
        
    def handle_input(self, keys):
        """Handle keyboard input for direction changes."""
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.next_direction = UP
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.next_direction = DOWN
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.next_direction = LEFT
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.next_direction = RIGHT
    
    def _can_move(self, direction, maze):
        """Check if Pac-Man can move in a given direction."""
        # Calculate next position
        test_x = self.x + direction[0] * self.speed * 2
        test_y = self.y + direction[1] * self.speed * 2
        
        # Check all corners of Pac-Man's bounding box
        corners = [
            (test_x - self.radius + 2, test_y - self.radius + 2),
            (test_x + self.radius - 2, test_y - self.radius + 2),
            (test_x - self.radius + 2, test_y + self.radius - 2),
            (test_x + self.radius - 2, test_y + self.radius - 2),
        ]
        
        for corner_x, corner_y in corners:
            grid_x = int((corner_x - MAZE_OFFSET_X) // TILE_SIZE)
            grid_y = int((corner_y - MAZE_OFFSET_Y) // TILE_SIZE)
            if maze.is_wall(grid_x, grid_y) or maze.is_ghost_house(grid_x, grid_y):
                return False
        return True
    
    def _is_aligned_with_grid(self):
        """Check if Pac-Man is aligned with the tile grid."""
        tile_center_x = MAZE_OFFSET_X + (self.get_grid_x() * TILE_SIZE) + TILE_SIZE // 2
        tile_center_y = MAZE_OFFSET_Y + (self.get_grid_y() * TILE_SIZE) + TILE_SIZE // 2
        
        tolerance = self.speed + 1
        return (abs(self.x - tile_center_x) <= tolerance and 
                abs(self.y - tile_center_y) <= tolerance)
    
    def _snap_to_grid(self):
        """Snap Pac-Man to the nearest grid center."""
        tile_center_x = MAZE_OFFSET_X + (self.get_grid_x() * TILE_SIZE) + TILE_SIZE // 2
        tile_center_y = MAZE_OFFSET_Y + (self.get_grid_y() * TILE_SIZE) + TILE_SIZE // 2
        
        if self.direction[0] == 0:  # Moving vertically
            self.x = tile_center_x
        if self.direction[1] == 0:  # Moving horizontally
            self.y = tile_center_y
    
    def update(self, maze, current_time):
        """Update Pac-Man's position and state."""
        # Check power-up expiration
        if self.powered_up:
            if current_time - self.powerup_start_time > POWERUP_DURATION:
                self.powered_up = False
        
        # Try to change direction if aligned with grid
        if self.next_direction != NONE and self._is_aligned_with_grid():
            if self._can_move(self.next_direction, maze):
                self.direction = self.next_direction
                if self.direction != NONE:
                    self.facing_direction = self.direction
                self._snap_to_grid()
        
        # Move in current direction
        if self.direction != NONE:
            if self._can_move(self.direction, maze):
                self.x += self.direction[0] * self.speed
                self.y += self.direction[1] * self.speed
                
                # Handle tunnel wrap-around
                if self.x < MAZE_OFFSET_X:
                    self.x = MAZE_OFFSET_X + maze.width * TILE_SIZE - TILE_SIZE // 2
                elif self.x > MAZE_OFFSET_X + maze.width * TILE_SIZE:
                    self.x = MAZE_OFFSET_X + TILE_SIZE // 2
            else:
                # Stop when hitting a wall
                self._snap_to_grid()
        
        # Update mouth animation
        if self.direction != NONE:
            if self.mouth_opening:
                self.mouth_angle += self.animation_speed
                if self.mouth_angle >= 45:
                    self.mouth_opening = False
            else:
                self.mouth_angle -= self.animation_speed
                if self.mouth_angle <= 5:
                    self.mouth_opening = True
    
    def activate_powerup(self, current_time):
        """Activate power-up state."""
        self.powered_up = True
        self.powerup_start_time = current_time
    
    def get_powerup_remaining(self, current_time):
        """Get remaining power-up time in milliseconds."""
        if not self.powered_up:
            return 0
        remaining = POWERUP_DURATION - (current_time - self.powerup_start_time)
        return max(0, remaining)
    
    def get_grid_x(self):
        """Get current grid X position."""
        return int((self.x - MAZE_OFFSET_X) // TILE_SIZE)
    
    def get_grid_y(self):
        """Get current grid Y position."""
        return int((self.y - MAZE_OFFSET_Y) // TILE_SIZE)
    
    def get_rect(self):
        """Get Pac-Man's collision rectangle."""
        return pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )
    
    def draw(self, screen):
        """Draw Pac-Man on the screen."""
        # Calculate mouth direction angle
        if self.facing_direction == RIGHT:
            start_angle = self.mouth_angle
        elif self.facing_direction == LEFT:
            start_angle = 180 + self.mouth_angle
        elif self.facing_direction == UP:
            start_angle = 90 + self.mouth_angle
        else:  # DOWN
            start_angle = 270 + self.mouth_angle
        
        end_angle = start_angle + (360 - 2 * self.mouth_angle)
        
        # Draw Pac-Man body
        color = PACMAN_COLOR
        if self.powered_up:
            # Pulsing effect when powered up
            pulse = abs(math.sin(pygame.time.get_ticks() / 100)) * 50
            color = (255, int(223 - pulse), int(pulse))
        
        # Draw as pie slice (mouth open)
        points = [(int(self.x), int(self.y))]
        for angle in range(int(start_angle), int(end_angle) + 1, 10):
            rad = math.radians(angle)
            px = self.x + self.radius * math.cos(rad)
            py = self.y - self.radius * math.sin(rad)
            points.append((int(px), int(py)))
        points.append((int(self.x), int(self.y)))
        
        if len(points) > 2:
            pygame.draw.polygon(screen, color, points)
        
        # Draw eye
        eye_offset_x = self.radius * 0.3
        eye_offset_y = -self.radius * 0.3
        if self.facing_direction == LEFT:
            eye_offset_x = -eye_offset_x
        elif self.facing_direction == UP:
            eye_offset_x = self.radius * 0.3 if self.facing_direction != LEFT else -self.radius * 0.3
            eye_offset_y = -self.radius * 0.1
        elif self.facing_direction == DOWN:
            eye_offset_y = -self.radius * 0.5
        
        eye_x = int(self.x + eye_offset_x)
        eye_y = int(self.y + eye_offset_y)
        pygame.draw.circle(screen, (0, 0, 0), (eye_x, eye_y), 3)
        
        # Draw power-up indicator if active
        if self.powered_up:
            # Draw small hearts around Pac-Man
            for i in range(3):
                angle = pygame.time.get_ticks() / 500 + i * (2 * math.pi / 3)
                hx = self.x + (self.radius + 5) * math.cos(angle)
                hy = self.y + (self.radius + 5) * math.sin(angle)
                self._draw_mini_heart(screen, int(hx), int(hy), 4)
    
    def _draw_mini_heart(self, screen, x, y, size):
        """Draw a small heart at the given position."""
        points = [
            (x, y + size // 2),
            (x - size // 2, y - size // 4),
            (x - size // 4, y - size // 2),
            (x, y - size // 4),
            (x + size // 4, y - size // 2),
            (x + size // 2, y - size // 4),
        ]
        pygame.draw.polygon(screen, HEART_COLOR, points)
