"""
Main game logic for Valentine's Pac-Man game.
Handles game states, collisions, scoring, and rendering.
"""

import pygame
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BG_COLOR, TEXT_COLOR,
    DOT_SCORE, GHOST_SCORE, ROSE_SCORE, STARTING_LIVES,
    STATE_START, STATE_PLAYING, STATE_PAUSED, STATE_GAME_OVER, STATE_WIN,
    HEART_COLOR, WALL_COLOR
)
from maze import Maze
from pacman import PacMan
from ghost import create_ghosts
from powerup import RoseManager
from projectile import HeartManager


class Game:
    """Main game class handling all game logic."""
    
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.state = STATE_START
        
        # Initialize game objects
        self.maze = Maze()
        
        # Initialize Pac-Man
        start_x, start_y = self.maze.get_pacman_start()
        self.pacman = PacMan(start_x, start_y)
        
        # Initialize ghosts
        self.ghosts = create_ghosts(self.maze)
        
        # Initialize managers
        self.rose_manager = RoseManager()
        self.heart_manager = HeartManager()
        
        # Game state
        self.score = 0
        self.lives = STARTING_LIVES
        self.level = 1
        
        # Fonts
        self.font_large = pygame.font.Font(None, 64)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Death animation
        self.death_animation = False
        self.death_time = 0
        self.death_duration = 1500  # milliseconds
    
    def reset_level(self):
        """Reset the level after death or for new level."""
        self.pacman.reset()
        for ghost in self.ghosts:
            ghost.reset()
        self.heart_manager.reset()
        self.death_animation = False
    
    def reset_game(self):
        """Reset the entire game."""
        self.maze.reset()
        self.reset_level()
        self.rose_manager.reset()
        self.score = 0
        self.lives = STARTING_LIVES
        self.level = 1
        self.state = STATE_PLAYING
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            
            if event.type == pygame.KEYDOWN:
                if self.state == STATE_START:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                
                elif self.state == STATE_PLAYING:
                    if event.key == pygame.K_p:
                        self.state = STATE_PAUSED
                    elif event.key == pygame.K_ESCAPE:
                        self.state = STATE_PAUSED
                
                elif self.state == STATE_PAUSED:
                    if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                        self.state = STATE_PLAYING
                    elif event.key == pygame.K_r:
                        self.reset_game()
                
                elif self.state in [STATE_GAME_OVER, STATE_WIN]:
                    if event.key == pygame.K_r:
                        self.reset_game()
                    elif event.key == pygame.K_SPACE:
                        self.reset_game()
        
        # Handle continuous key presses for movement
        if self.state == STATE_PLAYING and not self.death_animation:
            keys = pygame.key.get_pressed()
            self.pacman.handle_input(keys)
    
    def update(self):
        """Update game state."""
        if self.state != STATE_PLAYING:
            return
        
        current_time = pygame.time.get_ticks()
        
        # Handle death animation
        if self.death_animation:
            if current_time - self.death_time > self.death_duration:
                self.lives -= 1
                if self.lives <= 0:
                    self.state = STATE_GAME_OVER
                else:
                    self.reset_level()
            return
        
        # Update Pac-Man
        self.pacman.update(self.maze, current_time)
        
        # Check dot eating
        grid_x = self.pacman.get_grid_x()
        grid_y = self.pacman.get_grid_y()
        if self.maze.eat_dot(grid_x, grid_y):
            self.score += DOT_SCORE
        
        # Check win condition
        if self.maze.dots_remaining <= 0:
            self.state = STATE_WIN
            return
        
        # Update rose power-up
        if self.rose_manager.update(self.maze, self.pacman, current_time):
            self.score += ROSE_SCORE
            self.pacman.activate_powerup(current_time)
        
        # Fire hearts if powered up
        self.heart_manager.fire(self.pacman, current_time)
        
        # Update hearts and check ghost kills
        ghosts_killed = self.heart_manager.update(
            self.maze, self.ghosts, current_time
        )
        for ghost in ghosts_killed:
            self.score += GHOST_SCORE
        
        # Update ghosts
        for ghost in self.ghosts:
            ghost.update(self.pacman, self.maze, current_time)
            
            # Check collision with Pac-Man
            if ghost.alive and ghost.collides_with(self.pacman.get_rect()):
                # Pac-Man dies
                self.death_animation = True
                self.death_time = current_time
                return
    
    def draw(self):
        """Draw everything to the screen."""
        # Clear screen
        self.screen.fill(BG_COLOR)
        
        if self.state == STATE_START:
            self._draw_start_screen()
        elif self.state == STATE_PLAYING or self.state == STATE_PAUSED:
            self._draw_game()
            if self.state == STATE_PAUSED:
                self._draw_pause_overlay()
        elif self.state == STATE_GAME_OVER:
            self._draw_game()
            self._draw_game_over_overlay()
        elif self.state == STATE_WIN:
            self._draw_game()
            self._draw_win_overlay()
    
    def _draw_start_screen(self):
        """Draw the start screen."""
        # Title
        title_text = "PAC-MAN"
        title_surface = self.font_large.render(title_text, True, WALL_COLOR)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title_surface, title_rect)
        
        # Subtitle
        subtitle_text = "Valentine's Special"
        subtitle_surface = self.font_medium.render(subtitle_text, True, HEART_COLOR)
        subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(subtitle_surface, subtitle_rect)
        
        # Draw decorative hearts
        self._draw_heart_decoration(SCREEN_WIDTH // 2, 260, 30)
        
        # Instructions
        instructions = [
            "Use ARROW KEYS to move",
            "Eat all dots to win",
            "Collect ROSES to shoot HEARTS",
            "Hearts eliminate ghosts!",
            "",
            "Press SPACE to start"
        ]
        
        y_offset = 320
        for line in instructions:
            text_surface = self.font_small.render(line, True, TEXT_COLOR)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(text_surface, text_rect)
            y_offset += 30
        
        # Draw sample characters
        self._draw_sample_characters()
    
    def _draw_sample_characters(self):
        """Draw sample game characters on start screen."""
        # Draw Pac-Man sample
        pygame.draw.circle(self.screen, (255, 223, 0), (150, 550), 15)
        
        # Draw ghost samples
        colors = [(255, 0, 0), (255, 184, 255), (0, 255, 255), (255, 184, 82)]
        for i, color in enumerate(colors):
            x = 250 + i * 40
            pygame.draw.circle(self.screen, color, (x, 545), 12)
            pygame.draw.rect(self.screen, color, (x - 12, 545, 24, 12))
    
    def _draw_heart_decoration(self, x, y, size):
        """Draw a decorative heart."""
        half = size // 2
        quarter = size // 4
        pygame.draw.circle(self.screen, HEART_COLOR, (x - quarter, y - quarter), half)
        pygame.draw.circle(self.screen, HEART_COLOR, (x + quarter, y - quarter), half)
        points = [
            (x - half, y - quarter + 2),
            (x + half, y - quarter + 2),
            (x, y + half)
        ]
        pygame.draw.polygon(self.screen, HEART_COLOR, points)
    
    def _draw_game(self):
        """Draw the main game elements."""
        # Draw HUD
        self._draw_hud()
        
        # Draw maze
        self.maze.draw(self.screen)
        
        # Draw rose
        self.rose_manager.draw(self.screen)
        
        # Draw hearts
        self.heart_manager.draw(self.screen)
        
        # Draw ghosts
        for ghost in self.ghosts:
            ghost.draw(self.screen)
        
        # Draw Pac-Man (unless death animation)
        if not self.death_animation:
            self.pacman.draw(self.screen)
        else:
            self._draw_death_animation()
    
    def _draw_hud(self):
        """Draw the heads-up display (score, lives, power-up timer)."""
        # Score
        score_text = f"SCORE: {self.score}"
        score_surface = self.font_small.render(score_text, True, TEXT_COLOR)
        self.screen.blit(score_surface, (10, 10))
        
        # Lives
        lives_text = "LIVES:"
        lives_surface = self.font_small.render(lives_text, True, TEXT_COLOR)
        self.screen.blit(lives_surface, (SCREEN_WIDTH - 150, 10))
        
        # Draw Pac-Man icons for lives
        for i in range(self.lives):
            x = SCREEN_WIDTH - 80 + i * 25
            pygame.draw.circle(self.screen, (255, 223, 0), (x, 18), 8)
        
        # Power-up timer
        current_time = pygame.time.get_ticks()
        remaining = self.pacman.get_powerup_remaining(current_time)
        if remaining > 0:
            timer_text = f"POWER: {remaining // 1000 + 1}s"
            timer_surface = self.font_small.render(timer_text, True, HEART_COLOR)
            timer_rect = timer_surface.get_rect(center=(SCREEN_WIDTH // 2, 15))
            self.screen.blit(timer_surface, timer_rect)
    
    def _draw_death_animation(self):
        """Draw death animation for Pac-Man."""
        current_time = pygame.time.get_ticks()
        progress = (current_time - self.death_time) / self.death_duration
        
        # Shrinking circle
        radius = int(self.pacman.radius * (1 - progress))
        if radius > 0:
            pygame.draw.circle(
                self.screen, 
                (255, 223, 0), 
                (int(self.pacman.x), int(self.pacman.y)), 
                radius
            )
    
    def _draw_pause_overlay(self):
        """Draw pause overlay."""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        pause_text = "PAUSED"
        pause_surface = self.font_large.render(pause_text, True, TEXT_COLOR)
        pause_rect = pause_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        self.screen.blit(pause_surface, pause_rect)
        
        # Instructions
        resume_text = "Press P to resume"
        resume_surface = self.font_small.render(resume_text, True, TEXT_COLOR)
        resume_rect = resume_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(resume_surface, resume_rect)
        
        restart_text = "Press R to restart"
        restart_surface = self.font_small.render(restart_text, True, TEXT_COLOR)
        restart_rect = restart_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(restart_surface, restart_rect)
    
    def _draw_game_over_overlay(self):
        """Draw game over overlay."""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(180)
        self.screen.blit(overlay, (0, 0))
        
        # Game Over text
        game_over_text = "GAME OVER"
        game_over_surface = self.font_large.render(game_over_text, True, (255, 0, 0))
        game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(game_over_surface, game_over_rect)
        
        # Final score
        score_text = f"Final Score: {self.score}"
        score_surface = self.font_medium.render(score_text, True, TEXT_COLOR)
        score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
        self.screen.blit(score_surface, score_rect)
        
        # Restart instruction
        restart_text = "Press SPACE or R to play again"
        restart_surface = self.font_small.render(restart_text, True, TEXT_COLOR)
        restart_rect = restart_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(restart_surface, restart_rect)
    
    def _draw_win_overlay(self):
        """Draw win overlay."""
        # Semi-transparent overlay with pink tint
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((50, 0, 30))
        overlay.set_alpha(180)
        self.screen.blit(overlay, (0, 0))
        
        # Win text
        win_text = "YOU WIN!"
        win_surface = self.font_large.render(win_text, True, HEART_COLOR)
        win_rect = win_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        self.screen.blit(win_surface, win_rect)
        
        # Draw hearts decoration
        for i in range(5):
            x = 100 + i * 90
            self._draw_heart_decoration(x, SCREEN_HEIGHT // 2 - 20, 20)
        
        # Final score
        score_text = f"Final Score: {self.score}"
        score_surface = self.font_medium.render(score_text, True, TEXT_COLOR)
        score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        self.screen.blit(score_surface, score_rect)
        
        # Restart instruction
        restart_text = "Press SPACE or R to play again"
        restart_surface = self.font_small.render(restart_text, True, TEXT_COLOR)
        restart_rect = restart_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        self.screen.blit(restart_surface, restart_rect)
