# Valentine's Pac-Man Game - Development Plan

## Overview

Build a Valentine-themed Pac-Man game using **Pygame + pygbag** with emoji-based sprites and a classic 28x31 maze. The game runs in any browser via WebAssembly and can be deployed to GitHub Pages.

---

## Technology Stack

- **Pygame**: Python game development library
- **pygbag**: Compiles Pygame to WebAssembly for browser deployment
- **Emoji sprites**: Fast implementation, universally supported

---

## Project Structure

```
Pac_Man/
├── main.py          # Async entry point for pygbag
├── game.py          # Game loop and state management
├── pacman.py        # Pac-Man class (movement, collision, power-up state)
├── ghost.py         # Ghost classes with AI behaviors
├── maze.py          # Maze loading, rendering, collision
├── projectile.py    # Heart projectile class
├── powerup.py       # Rose power-up class
├── config.py        # Constants (colors, speeds, sizes)
└── requirements.txt # pygame dependency
```

---

## Implementation Steps

### 1. Build Maze System (`maze.py`)
- Define 28x31 grid using integers: `0`=path, `1`=wall, `2`=dot, `3`=empty
- Render walls in dark pink (`#DB7093`), paths in black
- Dots rendered as white circles
- Provide `is_wall(x, y)` and `eat_dot(x, y)` methods

### 2. Implement Pac-Man (`pacman.py`)
- Respond to arrow keys for 4-direction movement
- Smooth tile-based movement with `PACMAN_SPEED = 4`
- Track `facing_direction` for heart shooting
- States: `NORMAL`, `POWERED_UP`
- Render as yellow circle with mouth

### 3. Implement Ghosts (`ghost.py`)
- Create 4 ghosts with distinct colors and AI:
  - **Blinky** (Red): Direct pathfinding to Pac-Man
  - **Pinky** (Pink): Target 4 tiles ahead of Pac-Man
  - **Inky** (Cyan): Complex flanking behavior
  - **Clyde** (Orange): Chase when far, scatter when close
- Use simple pathfinding (BFS or direct chase)
- Respawn at center after being eliminated

### 4. Implement Rose Power-Up (`powerup.py`)
- Class `Rose` with position and active state
- Spawn randomly on empty path tile every 10-15 seconds
- Render as rose sprite
- When collected: set `pacman.powered_up = True`, start 5-second timer

### 5. Implement Heart Projectiles (`projectile.py`)
- Class `Heart` with position, direction, speed
- Spawn from Pac-Man every 300ms while powered up
- Travel in `pacman.facing_direction` at `HEART_SPEED = 8`
- Render as heart sprite
- Collision check: eliminate ghost, remove heart

### 6. Implement Game States (`game.py`)
- `START`: Show Valentine's title screen, "Press SPACE to play"
- `PLAYING`: Main game loop
- `PAUSED`: Press P to pause/resume
- `GAME_OVER`: Show score, "Press R to restart"
- `WIN`: All dots eaten celebration screen

---

## Build & Deployment

```bash
# Install dependencies
pip install pygame pygbag

# Run locally
python main.py

# Build for browser (from Pac_Man directory)
pygbag main.py --build

# Output in build/web/ — copy to your GitHub Pages site
```

---

## Core Features Checklist

- [x] Arrow keys move Pac-Man
- [x] Ghosts pursue with varied behaviors
- [x] Eating dots increases score
- [x] Ghost contact decreases lives
- [x] Rose spawns every ~12 seconds
- [x] Collecting rose triggers 5s power-up
- [x] Hearts fire automatically during power-up
- [x] Hearts destroy ghosts on contact
- [x] Game over at 0 lives
- [x] Win when all dots eaten
- [x] Runs in browser via pygbag
