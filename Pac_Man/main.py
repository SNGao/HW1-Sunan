"""
Valentine's Pac-Man Game - Main Entry Point

A Valentine-themed Pac-Man game with special features:
- Classic Pac-Man mechanics with maze, dots, and ghosts
- Rose power-up that enables heart shooting
- Hearts eliminate ghosts on contact

Controls:
- Arrow keys or WASD: Move Pac-Man
- P or ESC: Pause game
- R: Restart game
- SPACE: Start game / Restart after game over

This file is compatible with both:
- Standard pygame (python main.py)
- pygbag for browser deployment (pygbag main.py)
"""

import asyncio
import sys
import pygame


async def main():
    """Main game loop."""
    # Import config after pygame is ready
    from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
    from game import Game
    
    # Initialize pygame
    pygame.init()
    
    # Try to initialize mixer, but don't fail if it doesn't work (web browsers)
    try:
        pygame.mixer.init()
    except Exception:
        pass  # Audio may not work in browser
    
    # Set up display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pac-Man: Valentine's Special")
    
    # Set up clock for frame rate
    clock = pygame.time.Clock()
    
    # Create game instance
    game = Game(screen)
    
    # Main game loop
    while game.running:
        # Handle events
        game.handle_events()
        
        # Update game state
        game.update()
        
        # Draw everything
        game.draw()
        
        # Update display
        pygame.display.flip()
        
        # Control frame rate
        clock.tick(FPS)
        
        # Required for pygbag (web browser compatibility)
        # This yields control back to the browser event loop
        await asyncio.sleep(0)
    
    # Clean up
    pygame.quit()


# Entry point
if __name__ == "__main__":
    asyncio.run(main())
