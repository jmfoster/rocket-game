"""
Estes Alpha III Rocket Simulation Game - Version 1.0
====================================================

A realistic model rocket launch simulation and game featuring:
- Accurate Estes Alpha III physics with A/B/C engine types
- Real-time flight simulation with wind effects
- Interactive baseball recovery mini-game
- Spectacular visual effects and animations

Author: Created with Claude Code
Version: 1.0
Date: 2025-08-03

Controls:
- A/B/C: Select engine type
- Arrow Keys: Adjust wind speed and direction
- SPACE: Launch rocket
- ESC/Q: Quit game

Features:
- 6-second countdown with rainbow "BLAST OFF!!!" 
- White smoke and red flame effects during launch
- Realistic physics with parachute deployment
- Wind drift affecting rocket trajectory
- Tree-height landing (rocket stops at branch level)
- Baseball recovery mini-game with realistic physics
- Visual hit effects and falling animations
"""

import pygame
import numpy as np
import math
import random
from rocket_simulation import RocketSimulation, ENGINES

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
DARK_GREEN = (0, 100, 0)
SKY_BLUE = (135, 206, 235)
BROWN = (139, 69, 19)

class Particle:
    def __init__(self, x, y, vx, vy, life, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = life
        self.max_life = life
        self.color = color
        self.size = random.uniform(2, 5)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1  # gravity
        self.life -= 1
        
        # Fade color based on life
        alpha = self.life / self.max_life
        self.current_color = (
            int(self.color[0] * alpha),
            int(self.color[1] * alpha),
            int(self.color[2] * alpha)
        )
    
    def draw(self, screen):
        if self.life > 0:
            pygame.draw.circle(screen, self.current_color, 
                             (int(self.x), int(self.y)), int(self.size))

class RocketSprite:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.scale = 1.0
        self.exhaust_particles = []
        self.parachute_deployed = False
        
    def draw_rocket(self, screen):
        # Rocket body (blue with red tip)
        rocket_points = [
            (self.x, self.y - 15 * self.scale),  # tip
            (self.x - 3 * self.scale, self.y - 10 * self.scale),
            (self.x - 3 * self.scale, self.y + 10 * self.scale),
            (self.x + 3 * self.scale, self.y + 10 * self.scale),
            (self.x + 3 * self.scale, self.y - 10 * self.scale)
        ]
        pygame.draw.polygon(screen, BLUE, rocket_points)
        
        # Red nose cone
        nose_points = [
            (self.x, self.y - 15 * self.scale),
            (self.x - 3 * self.scale, self.y - 10 * self.scale),
            (self.x + 3 * self.scale, self.y - 10 * self.scale)
        ]
        pygame.draw.polygon(screen, RED, nose_points)
        
        # Fins
        fin_points = [
            (self.x - 3 * self.scale, self.y + 8 * self.scale),
            (self.x - 8 * self.scale, self.y + 15 * self.scale),
            (self.x - 3 * self.scale, self.y + 10 * self.scale)
        ]
        pygame.draw.polygon(screen, GRAY, fin_points)
        
        fin_points_right = [
            (self.x + 3 * self.scale, self.y + 8 * self.scale),
            (self.x + 8 * self.scale, self.y + 15 * self.scale),
            (self.x + 3 * self.scale, self.y + 10 * self.scale)
        ]
        pygame.draw.polygon(screen, GRAY, fin_points_right)
        
    def draw_parachute(self, screen):
        if self.parachute_deployed:
            # Parachute canopy (semi-circle)
            parachute_radius = 25
            pygame.draw.arc(screen, RED, 
                          (self.x - parachute_radius, self.y - 50 - parachute_radius,
                           parachute_radius * 2, parachute_radius * 2),
                          0, math.pi, 3)
            
            # Parachute lines
            for i in range(-2, 3):
                line_x = self.x + i * 8
                pygame.draw.line(screen, WHITE, 
                               (line_x, self.y - 50), (self.x, self.y - 15), 1)
    
    def add_exhaust_particle(self, engine_burning=False):
        if not self.parachute_deployed:
            # Add red exhaust particles (flames) when engine is burning
            if engine_burning:
                for _ in range(5):
                    px = self.x + random.uniform(-3, 3)
                    py = self.y + 15
                    pvx = random.uniform(-2, 2)
                    pvy = random.uniform(3, 8)
                    life = random.randint(15, 30)
                    color = RED  # Red flames
                    self.exhaust_particles.append(Particle(px, py, pvx, pvy, life, color))
                
                # Add white smoke particles for launch effect
                for _ in range(8):
                    px = self.x + random.uniform(-5, 5)
                    py = self.y + 18 + random.uniform(0, 10)
                    pvx = random.uniform(-3, 3)
                    pvy = random.uniform(1, 4)
                    life = random.randint(40, 80)
                    # White smoke with some gray variation
                    gray_val = random.randint(200, 255)
                    color = (gray_val, gray_val, gray_val)
                    self.exhaust_particles.append(Particle(px, py, pvx, pvy, life, color))
    
    def update_particles(self):
        self.exhaust_particles = [p for p in self.exhaust_particles if p.life > 0]
        for particle in self.exhaust_particles:
            particle.update()
    
    def draw_particles(self, screen):
        for particle in self.exhaust_particles:
            particle.draw(screen)

class VisualRocketGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Estes Alpha III Rocket Simulation - v1.0")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Game state
        self.state = "menu"  # menu, countdown, flying, recovery, results
        self.rocket_sprite = None
        self.simulation = None
        self.sim_time = 0
        self.time_step = 0.033  # ~30 FPS simulation steps for faster falling
        self.scale_factor = 2.5  # pixels per meter (much bigger field)
        
        # Countdown variables
        self.countdown_start_time = 0
        self.countdown_duration = 6000  # 6 seconds in milliseconds
        self.blast_off_duration = 2000  # Show BLAST OFF for 2 seconds
        
        # Landing variables
        self.landing_position = None
        self.landing_time = 0
        self.show_landing_marker = False
        
        # Menu variables
        self.selected_engine = 'B'
        self.wind_speed = 3.0  # Start with moderate wind
        self.wind_direction = 0  # East wind (blows rocket west toward left trees)
        
        # Baseball game variables
        self.baseball_angle = 45
        self.baseball_power = 0.5
        self.baseball_attempts = 0
        self.max_attempts = 10
        self.rocket_tree_x = 0
        self.rocket_tree_height = 6
        
        # Animation variables
        self.trajectory_points = []
        
    def draw_background(self):
        # Sky gradient
        for y in range(SCREEN_HEIGHT):
            color_ratio = y / SCREEN_HEIGHT
            r = int(135 * (1 - color_ratio) + 255 * color_ratio)
            g = int(206 * (1 - color_ratio) + 255 * color_ratio)
            b = int(235 * (1 - color_ratio) + 255 * color_ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Ground
        ground_y = SCREEN_HEIGHT - 100
        pygame.draw.rect(self.screen, GREEN, (0, ground_y, SCREEN_WIDTH, 100))
        
        # Football field - match simulation coordinates (109.7m field length)
        field_half_width = 109.7 * self.scale_factor / 2  # Half field width in pixels
        field_start_x = SCREEN_WIDTH // 2 - field_half_width
        field_end_x = SCREEN_WIDTH // 2 + field_half_width
        field_width_pixels = field_half_width * 2
        pygame.draw.rect(self.screen, (0, 150, 0), 
                        (field_start_x, ground_y, field_width_pixels, 100))
        
        # Field lines
        num_lines = 5
        for i in range(num_lines):
            x = field_start_x + i * (field_width_pixels / (num_lines - 1))
            pygame.draw.line(self.screen, WHITE, (x, ground_y), (x, ground_y + 100), 2)
        
        # Trees - fewer trees, more spaced out
        for x in range(0, int(field_start_x), 60):
            self.draw_tree(x + 30, ground_y)
        for x in range(int(field_end_x), SCREEN_WIDTH, 60):
            self.draw_tree(x + 30, ground_y)
    
    def draw_tree(self, x, ground_y):
        # Tree trunk
        pygame.draw.rect(self.screen, BROWN, (x - 5, ground_y - 40, 10, 40))
        # Tree foliage
        pygame.draw.circle(self.screen, DARK_GREEN, (x, ground_y - 60), 20)
    
    def draw_baseball(self, screen, x, y, size=5):
        # Draw baseball with white base and red stitching
        pygame.draw.circle(screen, WHITE, (int(x), int(y)), size)
        # Red stitching lines
        pygame.draw.arc(screen, RED, (int(x-size), int(y-size), size*2, size*2), 0, math.pi, 2)
        pygame.draw.arc(screen, RED, (int(x-size), int(y-size), size*2, size*2), math.pi, 2*math.pi, 2)
    
    def draw_menu(self):
        self.screen.fill(SKY_BLUE)
        
        # Title
        title = self.font.render("ESTES ALPHA III ROCKET SIMULATOR v1.0", True, BLACK)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.screen.blit(title, title_rect)
        
        # Engine selection
        engine_text = self.small_font.render(f"Engine: {self.selected_engine} (Press A/B/C)", True, BLACK)
        self.screen.blit(engine_text, (50, 200))
        
        # Engine specs
        engine = ENGINES[self.selected_engine]
        specs_text = [
            f"Total Impulse: {engine.total_impulse} N-s",
            f"Average Thrust: {engine.average_thrust} N",
            f"Burn Time: {engine.burn_time:.2f} s"
        ]
        
        for i, spec in enumerate(specs_text):
            text = self.small_font.render(spec, True, BLACK)
            self.screen.blit(text, (70, 230 + i * 25))
        
        # Wind conditions
        wind_text = self.small_font.render(f"Wind: {self.wind_speed:.1f} m/s from {self.wind_direction:.0f}°", True, BLACK)
        self.screen.blit(wind_text, (50, 350))
        
        wind_help = self.small_font.render("Press UP/DOWN: wind speed, LEFT/RIGHT: direction", True, GRAY)
        self.screen.blit(wind_help, (50, 375))
        
        # Launch button
        launch_text = self.font.render("Press SPACE to LAUNCH!", True, RED)
        launch_rect = launch_text.get_rect(center=(SCREEN_WIDTH//2, 500))
        self.screen.blit(launch_text, launch_rect)
        
        # Controls
        controls_text = [
            "Controls: ESC/Q = Quit, Arrows = Wind, A/B/C = Engine",
            "Features: Realistic physics, wind effects, tree recovery mini-game"
        ]
        for i, text in enumerate(controls_text):
            rendered = self.small_font.render(text, True, GRAY)
            self.screen.blit(rendered, (50, 550 + i * 25))
        
        # Draw preview rocket
        preview_rocket = RocketSprite(SCREEN_WIDTH//2, 600)
        preview_rocket.scale = 2.0
        preview_rocket.draw_rocket(self.screen)