"""
Ghost characters for Valentine's Pac-Man game.
Each ghost has unique chase behavior.
"""

import pygame
import random
import math
from config import (
    TILE_SIZE, MAZE_OFFSET_X, MAZE_OFFSET_Y, GHOST_SPEED,
    BLINKY_COLOR, PINKY_COLOR, INKY_COLOR, CLYDE_COLOR,
    GHOST_RESPAWN_TIME, UP, DOWN, LEFT, RIGHT
)


class Ghost:
    """Base ghost class with common functionality."""
    
    def __init__(self, start_grid_x, start_grid_y, color, name):
        self.start_grid_x = start_grid_x
        self.start_grid_y = start_grid_y
        self.color = color
        self.name = name
        self.reset()
    
    def reset(self):
        """Reset ghost to starting position."""
        self.x = MAZE_OFFSET_X + self.start_grid_x * TILE_SIZE + TILE_SIZE // 2
        self.y = MAZE_OFFSET_Y + self.start_grid_y * TILE_SIZE + TILE_SIZE // 2
        self.direction = LEFT  # Start moving left (valid from exit position)
        self.speed = GHOST_SPEED
        self.radius = TILE_SIZE // 2 - 2
        self.alive = True
        self.respawn_time = 0
        self.in_ghost_house = self.start_grid_y >= 12 and self.start_grid_y <= 16
        self.exit_timer = random.randint(0, 3000)  # Stagger ghost exits
        self.last_grid_x = self.start_grid_x
        self.last_grid_y = self.start_grid_y
        self.made_decision_this_tile = False
    
    def _get_valid_directions(self, maze):
        """Get list of valid directions the ghost can move."""
        valid = []
        opposite = (-self.direction[0], -self.direction[1])
        current_grid_x = self.get_grid_x()
        current_grid_y = self.get_grid_y()
        
        for direction in [UP, DOWN, LEFT, RIGHT]:
            # Check if the NEXT tile in this direction is walkable
            next_grid_x = current_grid_x + direction[0]
            next_grid_y = current_grid_y + direction[1]
            
            if self._is_tile_walkable(next_grid_x, next_grid_y, maze):
                # Ghosts prefer not to reverse direction unless it's the only option
                if direction != opposite:
                    valid.append(direction)
        
        # If no valid non-reverse directions, allow reversing
        if not valid:
            for direction in [UP, DOWN, LEFT, RIGHT]:
                next_grid_x = current_grid_x + direction[0]
                next_grid_y = current_grid_y + direction[1]
                if self._is_tile_walkable(next_grid_x, next_grid_y, maze):
                    valid.append(direction)
        
        return valid if valid else [self.direction]
    
    def _is_tile_walkable(self, grid_x, grid_y, maze):
        """Check if a tile is walkable for this ghost."""
        cell = maze.get_cell(grid_x, grid_y)
        
        # Walls are never walkable
        if cell == 1:
            return False
        
        # Ghosts inside ghost house can move within it
        if self.in_ghost_house:
            return True
        
        # Ghosts outside cannot re-enter ghost house (cell value 3)
        if cell == 3:
            return False
        
        return True
    
    def _can_move(self, direction, maze):
        """Check if ghost can move in a given direction (for actual movement)."""
        # Check the next tile
        next_grid_x = self.get_grid_x() + direction[0]
        next_grid_y = self.get_grid_y() + direction[1]
        
        # But also need to handle being at tile boundaries
        # If we're near edge of current tile, check the adjacent tile
        tile_center_x = MAZE_OFFSET_X + self.get_grid_x() * TILE_SIZE + TILE_SIZE // 2
        tile_center_y = MAZE_OFFSET_Y + self.get_grid_y() * TILE_SIZE + TILE_SIZE // 2
        
        # If moving away from center, check next tile
        moving_away_x = direction[0] != 0 and (
            (direction[0] > 0 and self.x >= tile_center_x - 1) or
            (direction[0] < 0 and self.x <= tile_center_x + 1)
        )
        moving_away_y = direction[1] != 0 and (
            (direction[1] > 0 and self.y >= tile_center_y - 1) or
            (direction[1] < 0 and self.y <= tile_center_y + 1)
        )
        
        if moving_away_x or moving_away_y:
            return self._is_tile_walkable(next_grid_x, next_grid_y, maze)
        
        return True
    
    def _is_aligned_with_grid(self):
        """Check if ghost is aligned with the tile grid."""
        tile_center_x = MAZE_OFFSET_X + (self.get_grid_x() * TILE_SIZE) + TILE_SIZE // 2
        tile_center_y = MAZE_OFFSET_Y + (self.get_grid_y() * TILE_SIZE) + TILE_SIZE // 2
        
        tolerance = self.speed + 1
        return (abs(self.x - tile_center_x) <= tolerance and 
                abs(self.y - tile_center_y) <= tolerance)
    
    def _snap_to_grid(self):
        """Snap ghost to the nearest grid center."""
        self.x = MAZE_OFFSET_X + (self.get_grid_x() * TILE_SIZE) + TILE_SIZE // 2
        self.y = MAZE_OFFSET_Y + (self.get_grid_y() * TILE_SIZE) + TILE_SIZE // 2
    
    def get_target(self, pacman, maze):
        """Get target position for this ghost. Override in subclasses."""
        return (pacman.get_grid_x(), pacman.get_grid_y())
    
    def _choose_direction(self, target_x, target_y, maze):
        """Choose direction that moves closest to target."""
        valid_directions = self._get_valid_directions(maze)
        
        if not valid_directions:
            return self.direction
        
        best_direction = valid_directions[0]
        best_distance = float('inf')
        
        for direction in valid_directions:
            new_x = self.get_grid_x() + direction[0]
            new_y = self.get_grid_y() + direction[1]
            distance = (new_x - target_x) ** 2 + (new_y - target_y) ** 2
            
            if distance < best_distance:
                best_distance = distance
                best_direction = direction
        
        return best_direction
    
    def update(self, pacman, maze, current_time):
        """Update ghost position and state."""
        if not self.alive:
            # Check if ready to respawn
            if current_time - self.respawn_time > GHOST_RESPAWN_TIME:
                self.alive = True
                self.x = MAZE_OFFSET_X + 13 * TILE_SIZE + TILE_SIZE // 2
                self.y = MAZE_OFFSET_Y + 14 * TILE_SIZE + TILE_SIZE // 2
                self.in_ghost_house = True
                self.exit_timer = 500
            return
        
        # Handle ghost house exit
        if self.in_ghost_house:
            self.exit_timer -= 16  # Approximate frame time
            if self.exit_timer <= 0:
                # Move towards exit
                exit_x, exit_y = maze.get_ghost_house_exit()
                exit_px = MAZE_OFFSET_X + exit_x * TILE_SIZE + TILE_SIZE // 2
                exit_py = MAZE_OFFSET_Y + exit_y * TILE_SIZE + TILE_SIZE // 2
                
                if abs(self.x - exit_px) > self.speed:
                    self.x += self.speed if self.x < exit_px else -self.speed
                elif abs(self.y - exit_py) > self.speed:
                    self.y += self.speed if self.y < exit_py else -self.speed
                else:
                    self.in_ghost_house = False
                    # Start moving left (there's a valid path to the left from exit)
                    self.direction = LEFT
                    self.last_grid_x = exit_x
                    self.last_grid_y = exit_y
                    self.made_decision_this_tile = True
            return
        
        # Check if we've entered a new tile
        current_grid_x = self.get_grid_x()
        current_grid_y = self.get_grid_y()
        entered_new_tile = (current_grid_x != self.last_grid_x or 
                           current_grid_y != self.last_grid_y)
        
        if entered_new_tile:
            self.last_grid_x = current_grid_x
            self.last_grid_y = current_grid_y
            self.made_decision_this_tile = False
        
        # Change direction when aligned with tile center (only once per tile)
        if self._is_aligned_with_grid() and not self.made_decision_this_tile:
            target_x, target_y = self.get_target(pacman, maze)
            new_direction = self._choose_direction(target_x, target_y, maze)
            # Only change if the new direction is valid
            if self._can_move(new_direction, maze):
                self.direction = new_direction
            self.made_decision_this_tile = True
        
        # Move in current direction
        if self._can_move(self.direction, maze):
            self.x += self.direction[0] * self.speed
            self.y += self.direction[1] * self.speed
        else:
            # Current direction blocked - find ANY valid direction
            for try_dir in [UP, DOWN, LEFT, RIGHT]:
                if self._can_move(try_dir, maze):
                    self.direction = try_dir
                    self.x += self.direction[0] * self.speed
                    self.y += self.direction[1] * self.speed
                    break
            
        # Handle tunnel wrap-around
        if self.x < MAZE_OFFSET_X:
            self.x = MAZE_OFFSET_X + maze.width * TILE_SIZE - TILE_SIZE // 2
        elif self.x > MAZE_OFFSET_X + maze.width * TILE_SIZE:
            self.x = MAZE_OFFSET_X + TILE_SIZE // 2
    
    def kill(self, current_time):
        """Kill the ghost."""
        self.alive = False
        self.respawn_time = current_time
    
    def get_grid_x(self):
        """Get current grid X position."""
        return int((self.x - MAZE_OFFSET_X) // TILE_SIZE)
    
    def get_grid_y(self):
        """Get current grid Y position."""
        return int((self.y - MAZE_OFFSET_Y) // TILE_SIZE)
    
    def get_rect(self):
        """Get ghost's collision rectangle."""
        return pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )
    
    def collides_with(self, other_rect):
        """Check collision with another rectangle."""
        return self.get_rect().colliderect(other_rect)
    
    def draw(self, screen):
        """Draw the ghost on the screen."""
        if not self.alive:
            return
        
        x, y = int(self.x), int(self.y)
        r = self.radius
        
        # Ghost body (rounded top, wavy bottom)
        # Top semicircle
        pygame.draw.circle(screen, self.color, (x, y - 2), r)
        
        # Body rectangle
        pygame.draw.rect(screen, self.color, 
                        (x - r, y - 2, r * 2, r))
        
        # Wavy bottom
        wave_offset = (pygame.time.get_ticks() // 100) % 2
        for i in range(3):
            wave_x = x - r + (i * 2 * r // 3) + r // 3
            wave_y = y + r - 4
            wave_r = r // 3
            if (i + wave_offset) % 2 == 0:
                pygame.draw.circle(screen, self.color, (wave_x, wave_y), wave_r)
        
        # Eyes
        eye_offset = 4
        eye_radius = 4
        pupil_radius = 2
        
        # Eye direction based on movement
        pupil_offset_x = self.direction[0] * 2
        pupil_offset_y = self.direction[1] * 2
        
        # Left eye
        pygame.draw.circle(screen, (255, 255, 255), 
                          (x - eye_offset, y - 4), eye_radius)
        pygame.draw.circle(screen, (0, 0, 200), 
                          (x - eye_offset + pupil_offset_x, 
                           y - 4 + pupil_offset_y), pupil_radius)
        
        # Right eye
        pygame.draw.circle(screen, (255, 255, 255), 
                          (x + eye_offset, y - 4), eye_radius)
        pygame.draw.circle(screen, (0, 0, 200), 
                          (x + eye_offset + pupil_offset_x, 
                           y - 4 + pupil_offset_y), pupil_radius)


class Blinky(Ghost):
    """Red ghost - Direct chaser, always targets Pac-Man's position."""
    
    def __init__(self, start_grid_x, start_grid_y):
        super().__init__(start_grid_x, start_grid_y, BLINKY_COLOR, "Blinky")
        self.in_ghost_house = False  # Blinky starts outside
    
    def get_target(self, pacman, maze):
        """Direct chase - target Pac-Man's current position."""
        return (pacman.get_grid_x(), pacman.get_grid_y())


class Pinky(Ghost):
    """Pink ghost - Ambusher, targets 4 tiles ahead of Pac-Man."""
    
    def __init__(self, start_grid_x, start_grid_y):
        super().__init__(start_grid_x, start_grid_y, PINKY_COLOR, "Pinky")
    
    def get_target(self, pacman, maze):
        """Ambush - target 4 tiles ahead of Pac-Man."""
        target_x = pacman.get_grid_x() + pacman.facing_direction[0] * 4
        target_y = pacman.get_grid_y() + pacman.facing_direction[1] * 4
        
        # Clamp to maze bounds
        target_x = max(0, min(maze.width - 1, target_x))
        target_y = max(0, min(maze.height - 1, target_y))
        
        return (target_x, target_y)


class Inky(Ghost):
    """Cyan ghost - Unpredictable, uses Blinky's position for targeting."""
    
    def __init__(self, start_grid_x, start_grid_y, blinky=None):
        super().__init__(start_grid_x, start_grid_y, INKY_COLOR, "Inky")
        self.blinky = blinky
    
    def get_target(self, pacman, maze):
        """Flanking behavior using Blinky's position."""
        if self.blinky is None:
            return (pacman.get_grid_x(), pacman.get_grid_y())
        
        # Get position 2 tiles ahead of Pac-Man
        ahead_x = pacman.get_grid_x() + pacman.facing_direction[0] * 2
        ahead_y = pacman.get_grid_y() + pacman.facing_direction[1] * 2
        
        # Vector from Blinky to that position, doubled
        target_x = ahead_x + (ahead_x - self.blinky.get_grid_x())
        target_y = ahead_y + (ahead_y - self.blinky.get_grid_y())
        
        # Clamp to maze bounds
        target_x = max(0, min(maze.width - 1, target_x))
        target_y = max(0, min(maze.height - 1, target_y))
        
        return (target_x, target_y)


class Clyde(Ghost):
    """Orange ghost - Shy, chases when far but scatters when close."""
    
    def __init__(self, start_grid_x, start_grid_y):
        super().__init__(start_grid_x, start_grid_y, CLYDE_COLOR, "Clyde")
    
    def get_target(self, pacman, maze):
        """Chase when far (>8 tiles), scatter to corner when close."""
        distance = math.sqrt(
            (self.get_grid_x() - pacman.get_grid_x()) ** 2 +
            (self.get_grid_y() - pacman.get_grid_y()) ** 2
        )
        
        if distance > 8:
            # Chase Pac-Man
            return (pacman.get_grid_x(), pacman.get_grid_y())
        else:
            # Scatter to bottom-left corner
            return (1, maze.height - 2)


def create_ghosts(maze):
    """Create all four ghosts at their starting positions."""
    positions = maze.get_ghost_start_positions()
    
    blinky = Blinky(positions[0][0], positions[0][1])
    pinky = Pinky(positions[1][0], positions[1][1])
    inky = Inky(positions[2][0], positions[2][1], blinky)
    clyde = Clyde(positions[3][0], positions[3][1])
    
    return [blinky, pinky, inky, clyde]
