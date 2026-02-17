"""
Maze system for Valentine's Pac-Man game.
Handles maze layout, rendering, and collision detection.
"""

import pygame
from config import (
    TILE_SIZE, MAZE_OFFSET_X, MAZE_OFFSET_Y,
    WALL_COLOR, PATH_COLOR, DOT_COLOR
)

# Maze layout:
# 0 = path with dot
# 1 = wall
# 2 = empty path (no dot)
# 3 = ghost house
# 4 = ghost house door

MAZE_LAYOUT = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,0,1],
    [1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,0,1],
    [1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,0,1],
    [1,0,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,0,1,1,1,1,1,2,1,1,2,1,1,1,1,1,0,1,1,1,1,1,1],
    [1,1,1,1,1,1,0,1,1,1,1,1,2,1,1,2,1,1,1,1,1,0,1,1,1,1,1,1],
    [1,1,1,1,1,1,0,1,1,2,2,2,2,2,2,2,2,2,2,1,1,0,1,1,1,1,1,1],
    [1,1,1,1,1,1,0,1,1,2,1,1,1,3,3,1,1,1,2,1,1,0,1,1,1,1,1,1],
    [1,1,1,1,1,1,0,1,1,2,1,3,3,3,3,3,3,1,2,1,1,0,1,1,1,1,1,1],
    [2,2,2,2,2,2,0,2,2,2,1,3,3,3,3,3,3,1,2,2,2,0,2,2,2,2,2,2],
    [1,1,1,1,1,1,0,1,1,2,1,3,3,3,3,3,3,1,2,1,1,0,1,1,1,1,1,1],
    [1,1,1,1,1,1,0,1,1,2,1,1,1,1,1,1,1,1,2,1,1,0,1,1,1,1,1,1],
    [1,1,1,1,1,1,0,1,1,2,2,2,2,2,2,2,2,2,2,1,1,0,1,1,1,1,1,1],
    [1,1,1,1,1,1,0,1,1,2,1,1,1,1,1,1,1,1,2,1,1,0,1,1,1,1,1,1],
    [1,1,1,1,1,1,0,1,1,2,1,1,1,1,1,1,1,1,2,1,1,0,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,0,1],
    [1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,0,1],
    [1,0,0,0,1,1,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,1,1,0,0,0,1],
    [1,1,1,0,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,0,1,1,1],
    [1,1,1,0,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,0,1,1,1],
    [1,0,0,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1],
    [1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]


class Maze:
    """Handles maze layout, rendering, and collision detection."""
    
    def __init__(self):
        self.layout = [row[:] for row in MAZE_LAYOUT]  # Deep copy
        self.width = len(self.layout[0])
        self.height = len(self.layout)
        self.dots_remaining = self._count_dots()
        self.total_dots = self.dots_remaining
        
    def _count_dots(self):
        """Count total number of dots in the maze."""
        count = 0
        for row in self.layout:
            for cell in row:
                if cell == 0:
                    count += 1
        return count
    
    def reset(self):
        """Reset maze to initial state."""
        self.layout = [row[:] for row in MAZE_LAYOUT]
        self.dots_remaining = self._count_dots()
    
    def get_cell(self, grid_x, grid_y):
        """Get cell value at grid position."""
        if 0 <= grid_x < self.width and 0 <= grid_y < self.height:
            return self.layout[grid_y][grid_x]
        return 1  # Treat out of bounds as wall
    
    def is_wall(self, grid_x, grid_y):
        """Check if a cell is a wall."""
        cell = self.get_cell(grid_x, grid_y)
        return cell == 1
    
    def is_ghost_house(self, grid_x, grid_y):
        """Check if a cell is in the ghost house."""
        cell = self.get_cell(grid_x, grid_y)
        return cell == 3
    
    def is_walkable(self, grid_x, grid_y, is_ghost=False):
        """Check if a cell is walkable."""
        cell = self.get_cell(grid_x, grid_y)
        if is_ghost:
            return cell != 1  # Ghosts can walk on ghost house
        return cell in [0, 2]  # Pac-Man can walk on paths
    
    def is_valid_position(self, pixel_x, pixel_y, is_ghost=False):
        """Check if a pixel position is valid (not in a wall)."""
        grid_x = int((pixel_x - MAZE_OFFSET_X) // TILE_SIZE)
        grid_y = int((pixel_y - MAZE_OFFSET_Y) // TILE_SIZE)
        return self.is_walkable(grid_x, grid_y, is_ghost)
    
    def eat_dot(self, grid_x, grid_y):
        """Eat a dot at the given position. Returns True if dot was eaten."""
        if 0 <= grid_x < self.width and 0 <= grid_y < self.height:
            if self.layout[grid_y][grid_x] == 0:
                self.layout[grid_y][grid_x] = 2  # Mark as empty path
                self.dots_remaining -= 1
                return True
        return False
    
    def get_empty_positions(self):
        """Get list of empty path positions (for spawning items)."""
        positions = []
        for y in range(self.height):
            for x in range(self.width):
                if self.layout[y][x] in [0, 2]:
                    positions.append((x, y))
        return positions
    
    def grid_to_pixel(self, grid_x, grid_y):
        """Convert grid position to pixel position (center of tile)."""
        pixel_x = MAZE_OFFSET_X + grid_x * TILE_SIZE + TILE_SIZE // 2
        pixel_y = MAZE_OFFSET_Y + grid_y * TILE_SIZE + TILE_SIZE // 2
        return pixel_x, pixel_y
    
    def pixel_to_grid(self, pixel_x, pixel_y):
        """Convert pixel position to grid position."""
        grid_x = int((pixel_x - MAZE_OFFSET_X) // TILE_SIZE)
        grid_y = int((pixel_y - MAZE_OFFSET_Y) // TILE_SIZE)
        return grid_x, grid_y
    
    def draw(self, screen):
        """Draw the maze on the screen."""
        for y in range(self.height):
            for x in range(self.width):
                cell = self.layout[y][x]
                rect_x = MAZE_OFFSET_X + x * TILE_SIZE
                rect_y = MAZE_OFFSET_Y + y * TILE_SIZE
                rect = pygame.Rect(rect_x, rect_y, TILE_SIZE, TILE_SIZE)
                
                if cell == 1:  # Wall
                    pygame.draw.rect(screen, WALL_COLOR, rect)
                    # Add inner darker rectangle for depth
                    inner_rect = pygame.Rect(rect_x + 2, rect_y + 2, 
                                            TILE_SIZE - 4, TILE_SIZE - 4)
                    darker_wall = (170, 80, 110)
                    pygame.draw.rect(screen, darker_wall, inner_rect)
                elif cell == 3:  # Ghost house
                    ghost_house_color = (40, 20, 30)
                    pygame.draw.rect(screen, ghost_house_color, rect)
                else:  # Path
                    pygame.draw.rect(screen, PATH_COLOR, rect)
                    
                    # Draw dot if present
                    if cell == 0:
                        dot_x = rect_x + TILE_SIZE // 2
                        dot_y = rect_y + TILE_SIZE // 2
                        pygame.draw.circle(screen, DOT_COLOR, (dot_x, dot_y), 3)
    
    def get_pacman_start(self):
        """Get Pac-Man's starting position (grid coordinates)."""
        return (13, 23)  # Classic starting position
    
    def get_ghost_start_positions(self):
        """Get ghosts' starting positions (grid coordinates)."""
        return [
            (13, 11),  # Blinky - above ghost house
            (13, 14),  # Pinky - center of ghost house
            (11, 14),  # Inky - left in ghost house
            (15, 14),  # Clyde - right in ghost house
        ]
    
    def get_ghost_house_exit(self):
        """Get the ghost house exit position."""
        return (13, 11)  # Just above the ghost house
