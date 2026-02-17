"""
Configuration constants for Valentine's Pac-Man game.
"""

# Screen dimensions
SCREEN_WIDTH = 560
SCREEN_HEIGHT = 680
TILE_SIZE = 20

# Maze dimensions (in tiles)
MAZE_WIDTH = 28
MAZE_HEIGHT = 31

# Offsets for centering maze
MAZE_OFFSET_X = 0
MAZE_OFFSET_Y = 40  # Space for score/lives display

# Game settings
FPS = 60
PACMAN_SPEED = 2
GHOST_SPEED = 1.8
HEART_SPEED = 6
POWERUP_DURATION = 5000  # milliseconds
HEART_FIRE_RATE = 300    # milliseconds between heart shots
ROSE_SPAWN_INTERVAL = 12000  # milliseconds between rose spawns
GHOST_RESPAWN_TIME = 3000  # milliseconds

# Valentine color palette
WALL_COLOR = (219, 112, 147)      # Pale violet red
PATH_COLOR = (20, 20, 20)          # Near black
DOT_COLOR = (255, 255, 255)        # White
PACMAN_COLOR = (255, 223, 0)       # Gold/Yellow
HEART_COLOR = (255, 105, 180)      # Hot pink
ROSE_COLOR = (255, 0, 100)         # Deep pink/red
BG_COLOR = (30, 0, 15)             # Dark romantic purple
TEXT_COLOR = (255, 182, 193)       # Light pink

# Ghost colors
BLINKY_COLOR = (255, 0, 0)         # Red
PINKY_COLOR = (255, 184, 255)      # Pink
INKY_COLOR = (0, 255, 255)         # Cyan
CLYDE_COLOR = (255, 184, 82)       # Orange

# Scoring
DOT_SCORE = 10
GHOST_SCORE = 200
ROSE_SCORE = 50

# Lives
STARTING_LIVES = 3

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
NONE = (0, 0)

# Game states
STATE_START = "start"
STATE_PLAYING = "playing"
STATE_PAUSED = "paused"
STATE_GAME_OVER = "game_over"
STATE_WIN = "win"
