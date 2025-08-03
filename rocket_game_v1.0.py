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
        pygame.display.set_caption("Estes Alpha III Rocket Simulation")
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
        title = self.font.render("ESTES ALPHA III ROCKET SIMULATOR", True, BLACK)
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
        
        # Draw preview rocket
        preview_rocket = RocketSprite(SCREEN_WIDTH//2, 600)
        preview_rocket.scale = 2.0
        preview_rocket.draw_rocket(self.screen)
    
    def draw_countdown(self):
        self.draw_background()
        
        # Calculate countdown time
        elapsed = pygame.time.get_ticks() - self.countdown_start_time
        remaining = self.countdown_duration - elapsed
        
        if remaining > 0:
            seconds_left = int(remaining / 1000) + 1
            
            # Draw countdown number or message
            if seconds_left > 0:
                countdown_text = str(seconds_left)
                color = RED if seconds_left <= 3 else BLACK
                # Large countdown display
                big_font = pygame.font.Font(None, 120)
                text = big_font.render(countdown_text, True, color)
                text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
                self.screen.blit(text, text_rect)
            else:
                # BLAST OFF! with fun effects
                countdown_text = "BLAST OFF!!!"
                
                # Pulsing and scaling effect (keep font size reasonable)
                pulse = 1.0 + 0.2 * math.sin(pygame.time.get_ticks() * 0.02)
                font_size = int(100 * pulse)  # Smaller base size
                big_font = pygame.font.Font(None, font_size)
                
                # Rainbow color cycling
                time_factor = pygame.time.get_ticks() * 0.01
                r = int(128 + 127 * math.sin(time_factor))
                g = int(128 + 127 * math.sin(time_factor + 2))
                b = int(128 + 127 * math.sin(time_factor + 4))
                color = (r, g, b)
                
                # Simple centered text without complex glow effects
                text = big_font.render(countdown_text, True, color)
                text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
                
                # Simple outline effect
                outline_color = (255, 255, 255)  # White outline
                for dx in [-2, -1, 0, 1, 2]:
                    for dy in [-2, -1, 0, 1, 2]:
                        if dx != 0 or dy != 0:
                            outline_text = big_font.render(countdown_text, True, outline_color)
                            outline_rect = outline_text.get_rect(center=(SCREEN_WIDTH//2 + dx, SCREEN_HEIGHT//2 + dy))
                            self.screen.blit(outline_text, outline_rect)
                
                # Main text on top
                self.screen.blit(text, text_rect)
            
            # Draw rocket at launch position
            if self.rocket_sprite:
                self.rocket_sprite.x = SCREEN_WIDTH // 2
                self.rocket_sprite.y = SCREEN_HEIGHT - 100
                self.rocket_sprite.draw_rocket(self.screen)
        elif elapsed < self.countdown_duration + self.blast_off_duration:
            # Show BLAST OFF!!! for 2 seconds after countdown
            countdown_text = "BLAST OFF!!!"
            
            # Pulsing and scaling effect (keep font size reasonable)
            pulse = 1.0 + 0.2 * math.sin(pygame.time.get_ticks() * 0.02)
            font_size = int(100 * pulse)  # Smaller base size
            big_font = pygame.font.Font(None, font_size)
            
            # Rainbow color cycling
            time_factor = pygame.time.get_ticks() * 0.01
            r = int(128 + 127 * math.sin(time_factor))
            g = int(128 + 127 * math.sin(time_factor + 2))
            b = int(128 + 127 * math.sin(time_factor + 4))
            color = (r, g, b)
            
            # Simple centered text without complex glow effects
            text = big_font.render(countdown_text, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            
            # Simple outline effect
            outline_color = (255, 255, 255)  # White outline
            for dx in [-2, -1, 0, 1, 2]:
                for dy in [-2, -1, 0, 1, 2]:
                    if dx != 0 or dy != 0:
                        outline_text = big_font.render(countdown_text, True, outline_color)
                        outline_rect = outline_text.get_rect(center=(SCREEN_WIDTH//2 + dx, SCREEN_HEIGHT//2 + dy))
                        self.screen.blit(outline_text, outline_rect)
            
            # Main text on top
            self.screen.blit(text, text_rect)
            
            # Draw rocket at launch position
            if self.rocket_sprite:
                self.rocket_sprite.x = SCREEN_WIDTH // 2
                self.rocket_sprite.y = SCREEN_HEIGHT - 100
                self.rocket_sprite.draw_rocket(self.screen)
        else:
            # BLAST OFF finished, start flight
            self.state = "flying"
    
    def draw_flight(self):
        self.draw_background()
        
        # Get current rocket position from simulation
        if self.simulation and len(self.simulation.position_history) > 0:
            current_pos = self.simulation.position_history[-1]
            
            # Separate scale factors for horizontal and vertical
            ground_level = SCREEN_HEIGHT - 100
            horizontal_scale = self.scale_factor  # Use full scale for field width
            vertical_scale = 0.8  # Much smaller scale for altitude to keep rocket on screen
            
            screen_x = SCREEN_WIDTH // 2 + (current_pos[0] - 54.85) * horizontal_scale
            screen_y = ground_level - current_pos[1] * vertical_scale
            
            # Keep rocket on screen - if it goes too high, scale it down more
            if screen_y < 50:  # Too high
                vertical_scale = 0.3
                screen_y = ground_level - current_pos[1] * vertical_scale
            
            # Don't let rocket go below appropriate landing surface
            if self.simulation:
                landing_zone = self.simulation.check_landing_location()
                
                if landing_zone == "trees" and current_pos[1] <= 6.1:  # Small buffer for tree height
                    # Rocket is in trees and at/below tree height - clamp to tree height (make it more visible)
                    tree_screen_y = ground_level - 30  # Fixed 30 pixels above ground for visibility
                    screen_y = tree_screen_y
                else:
                    # Normal altitude or field landing - clamp to ground
                    screen_y = min(screen_y, ground_level)
            
            # Draw rocket
            if self.rocket_sprite:
                self.rocket_sprite.x = screen_x
                self.rocket_sprite.y = screen_y
                
                # Add exhaust particles during burn phase
                engine_burning = self.sim_time <= self.simulation.engine.burn_time
                if (engine_burning and not self.rocket_sprite.parachute_deployed):
                    self.rocket_sprite.add_exhaust_particle(engine_burning)
                
                # Deploy parachute
                if (self.sim_time > self.simulation.engine.burn_time + self.simulation.engine.delay and
                    len(self.simulation.velocity_history) > 0 and
                    self.simulation.velocity_history[-1][1] <= 0):
                    self.rocket_sprite.parachute_deployed = True
                
                self.rocket_sprite.update_particles()
                self.rocket_sprite.draw_particles(self.screen)
                self.rocket_sprite.draw_rocket(self.screen)
                self.rocket_sprite.draw_parachute(self.screen)
            
            # Simple trajectory trail
            self.trajectory_points.append((screen_x, screen_y))
            if len(self.trajectory_points) > 100:
                self.trajectory_points.pop(0)
            
            # Draw trajectory trail
            if len(self.trajectory_points) > 1:
                pygame.draw.lines(self.screen, YELLOW, False, self.trajectory_points, 2)
        
        # Draw landing marker if rocket has landed
        if self.show_landing_marker and self.landing_position is not None:
            landing_screen_x = SCREEN_WIDTH // 2 + (self.landing_position[0] - 54.85) * self.scale_factor
            # Landing marker at ground level
            landing_screen_y = SCREEN_HEIGHT - 100
            
            # Pulsing landing marker
            pulse = int(20 * (1 + math.sin(pygame.time.get_ticks() * 0.01)))
            pygame.draw.circle(self.screen, RED, (int(landing_screen_x), int(landing_screen_y)), 15 + pulse, 3)
            pygame.draw.circle(self.screen, WHITE, (int(landing_screen_x), int(landing_screen_y)), 5)
            
            # Landing text and rocket positioning
            field_start = 0
            field_end = 109.7
            is_in_field = field_start <= self.landing_position[0] <= field_end
            
            if is_in_field:
                landing_text = "LANDED HERE!"
                text_color = GREEN
                # Rocket on ground
                rocket_y_offset = 0
            else:
                landing_text = "STUCK IN TREES!"
                text_color = RED
                # Show rocket slightly above ground (in tree)
                rocket_y_offset = -30
            
            rendered_text = self.small_font.render(landing_text, True, text_color)
            text_rect = rendered_text.get_rect(center=(int(landing_screen_x), int(landing_screen_y - 40)))
            self.screen.blit(rendered_text, text_rect)
            
            # Don't draw separate landed rocket - main rocket sprite handles landing
        
        # Flight info
        info_texts = [
            f"Time: {self.sim_time:.1f}s",
            f"Engine: {self.selected_engine}",
            f"Wind: {self.wind_speed:.1f} m/s"
        ]
        
        if self.simulation and len(self.simulation.position_history) > 0:
            current_pos = self.simulation.position_history[-1]
            current_vel = self.simulation.velocity_history[-1] if len(self.simulation.velocity_history) > 0 else np.array([0, 0])
            speed = np.linalg.norm(current_vel)
            
            info_texts.extend([
                f"Altitude: {current_pos[1]:.0f}m ({current_pos[1]*3.28:.0f}ft)",
                f"Horizontal: {current_pos[0]:.0f}m",
                f"Speed: {speed:.1f} m/s", 
                f"Vertical Speed: {current_vel[1]:.1f} m/s",
                f"Engine Burn: {self.sim_time:.1f}/{self.simulation.engine.burn_time:.1f}s",
                f"Mass: {self.simulation.rocket.mass:.3f}kg",
                f"Parachute: {'YES' if self.simulation.rocket.parachute_deployed else 'NO'}"
            ])
            
            # Add phase indicator
            if self.sim_time <= self.simulation.engine.burn_time:
                phase = "🚀 POWERED ASCENT"
                phase_color = RED
            elif current_vel[1] > 0:
                phase = "⬆️ COASTING UP"
                phase_color = BLUE
            elif not self.rocket_sprite.parachute_deployed:
                phase = "⬇️ FREE FALL"
                phase_color = ORANGE
            else:
                phase = "🪂 PARACHUTE DESCENT"
                phase_color = GREEN
            
            phase_text = self.small_font.render(phase, True, phase_color)
            self.screen.blit(phase_text, (10, 140))
        
        for i, text in enumerate(info_texts):
            rendered = self.small_font.render(text, True, BLACK)
            self.screen.blit(rendered, (10, 10 + i * 25))
    
    def draw_baseball_game(self):
        self.screen.fill(SKY_BLUE)
        
        # Ground and trees
        ground_y = SCREEN_HEIGHT - 100
        pygame.draw.rect(self.screen, GREEN, (0, ground_y, SCREEN_WIDTH, 100))
        
        # Draw trees with stuck rocket
        tree_x = SCREEN_WIDTH // 2 + self.rocket_tree_x
        self.draw_tree(tree_x, ground_y)
        
        # Draw stuck rocket in tree at proper height
        rocket_screen_height = ground_y - self.rocket_tree_height * 10  # Convert meters to pixels
        stuck_rocket = RocketSprite(tree_x + 10, rocket_screen_height)
        stuck_rocket.scale = 0.8
        stuck_rocket.draw_rocket(self.screen)
        
        # Player position (stick figure)
        player_x = 100
        player_y = ground_y - 20
        # Draw simple stick figure player
        pygame.draw.circle(self.screen, (255, 220, 177), (player_x, player_y - 10), 8)  # Head
        pygame.draw.line(self.screen, BLACK, (player_x, player_y - 2), (player_x, player_y + 15), 3)  # Body
        pygame.draw.line(self.screen, BLACK, (player_x - 8, player_y + 5), (player_x + 8, player_y + 5), 3)  # Arms
        pygame.draw.line(self.screen, BLACK, (player_x - 5, player_y + 15), (player_x + 5, player_y + 15), 3)  # Legs
        
        # Aiming line
        angle_rad = math.radians(self.baseball_angle)
        line_length = 100 * self.baseball_power
        end_x = player_x + line_length * math.cos(angle_rad)
        end_y = player_y - line_length * math.sin(angle_rad)
        pygame.draw.line(self.screen, RED, (player_x, player_y), (end_x, end_y), 3)
        
        # UI
        title = self.font.render("ROCKET RECOVERY - BASEBALL THROW", True, BLACK)
        self.screen.blit(title, (50, 50))
        
        info_texts = [
            f"Attempts: {self.baseball_attempts}/{self.max_attempts}",
            f"Angle: {self.baseball_angle:.0f}° (UP/DOWN arrows)",
            f"Power: {self.baseball_power:.2f} (LEFT/RIGHT arrows)",
            "Press SPACE to throw!"
        ]
        
        for i, text in enumerate(info_texts):
            rendered = self.small_font.render(text, True, BLACK)
            self.screen.blit(rendered, (50, 100 + i * 30))
        
        # Distance indicator
        distance = abs(self.rocket_tree_x)
        dist_text = self.small_font.render(f"Distance to rocket: {distance:.0f}m", True, RED)
        self.screen.blit(dist_text, (50, 250))
    
    def animate_baseball_throw(self):
        # Baseball trajectory animation with hit effects
        start_time = pygame.time.get_ticks()
        hit_occurred = False
        hit_time = 0
        
        while pygame.time.get_ticks() - start_time < 2500:  # 2.5 second animation
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
            
            self.draw_baseball_game()
            
            # Animate baseball
            t = (pygame.time.get_ticks() - start_time) / 2000.0
            if t <= 1.0:
                player_x = 100
                player_y = SCREEN_HEIGHT - 120
                
                # Calculate trajectory
                angle_rad = math.radians(self.baseball_angle)
                initial_v = self.baseball_power * 30
                vx = initial_v * math.cos(angle_rad)
                vy = initial_v * math.sin(angle_rad)
                
                x = player_x + vx * t * 100
                y = player_y - (vy * t * 100 - 0.5 * 980 * t * t)
                
                if y < SCREEN_HEIGHT:
                    # Draw baseball with stitching
                    self.draw_baseball(self.screen, x, y, 5)
                    
                    # Check for hit near rocket position
                    rocket_x = SCREEN_WIDTH // 2 + self.rocket_tree_x
                    rocket_y = SCREEN_HEIGHT - 100 - self.rocket_tree_height * 10
                    
                    distance = math.sqrt((x - rocket_x)**2 + (y - rocket_y)**2)
                    if distance < 20 and not hit_occurred:
                        hit_occurred = True
                        hit_time = pygame.time.get_ticks()
            
            # Show hit effects
            if hit_occurred:
                time_since_hit = pygame.time.get_ticks() - hit_time
                if time_since_hit < 500:  # Show effect for 0.5 seconds
                    # Flash effect
                    flash_alpha = 255 - (time_since_hit / 500) * 255
                    # Draw impact burst
                    burst_size = int(time_since_hit / 10)
                    for i in range(8):
                        angle = i * math.pi / 4
                        end_x = rocket_x + math.cos(angle) * burst_size
                        end_y = rocket_y + math.sin(angle) * burst_size
                        pygame.draw.line(self.screen, YELLOW, (rocket_x, rocket_y), (end_x, end_y), 3)
                    
                    # Hit text
                    hit_text = self.font.render("HIT!", True, RED)
                    self.screen.blit(hit_text, (rocket_x - 20, rocket_y - 50))
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        return hit_occurred
    
    def start_flight(self):
        self.state = "countdown"
        self.countdown_start_time = pygame.time.get_ticks()
        self.simulation = RocketSimulation(self.selected_engine, self.wind_speed, self.wind_direction)
        self.rocket_sprite = RocketSprite(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.sim_time = 0
        self.trajectory_points = []
        
        # Reset landing variables
        self.landing_position = None
        self.landing_time = 0
        self.show_landing_marker = False
        
        # Start simulation
        self.simulation.rocket.position = np.array([54.85, 0.0])  # Center of field
        self.simulation.rocket.velocity = np.array([0.0, 0.0])
        self.simulation.rocket.mass = self.simulation.rocket.dry_mass + 0.012
    
    def update_simulation(self):
        if self.simulation and self.state == "flying":
            # Run one physics step
            time = self.sim_time
            
            # Check for parachute deployment
            if (not self.simulation.rocket.parachute_deployed and 
                time > self.simulation.engine.burn_time + self.simulation.engine.delay and
                len(self.simulation.velocity_history) > 0 and
                self.simulation.velocity_history[-1][1] <= 0):
                self.simulation.rocket.parachute_deployed = True
                self.simulation.rocket.flight_phase = "descent"
            
            # Calculate forces
            thrust = self.simulation.thrust_force(time)
            drag = self.simulation.drag_force(self.simulation.rocket.velocity)
            gravity = np.array([0.0, -self.simulation.rocket.mass * self.simulation.g])
            
            # Add minimal wind force during parachute descent (horizontal only)
            wind_force = np.array([0.0, 0.0])
            if self.simulation.rocket.parachute_deployed:
                # Very gentle horizontal wind push
                wind_force = np.array([self.simulation.wind_vector[0] * 0.05, 0.0])
            
            # Safety check for mass
            if self.simulation.rocket.mass <= 0:
                self.simulation.rocket.mass = self.simulation.rocket.dry_mass
            
            # Total force and acceleration
            total_force = thrust + drag + gravity + wind_force
            acceleration = total_force / self.simulation.rocket.mass
            
            # Burn propellant during engine burn
            if time <= self.simulation.engine.burn_time:
                # Reduce mass as propellant burns (simple linear model)
                propellant_used = (time / self.simulation.engine.burn_time) * 0.012
                self.simulation.rocket.mass = self.simulation.rocket.dry_mass + 0.012 - propellant_used
            
            # Update velocity and position
            self.simulation.rocket.velocity += acceleration * self.time_step
            self.simulation.rocket.position += self.simulation.rocket.velocity * self.time_step
            
            # Record history
            self.simulation.time_history.append(time)
            self.simulation.position_history.append(self.simulation.rocket.position.copy())
            self.simulation.velocity_history.append(self.simulation.rocket.velocity.copy())
            
            # Check for landing (ground or tree height)
            landing = self.simulation.check_landing_location()
            tree_height = 6.0  # meters above ground
            
            # Determine landing altitude based on location
            if landing == "trees":
                landing_altitude = tree_height
            else:
                landing_altitude = 0.0
            
            if self.simulation.rocket.position[1] <= landing_altitude:
                # Stop rocket at appropriate height
                self.simulation.rocket.position[1] = landing_altitude
                self.simulation.rocket.velocity[1] = 0  # Stop falling
                
                # Record landing position and show marker (only once)
                if not self.show_landing_marker:
                    self.landing_position = self.simulation.rocket.position.copy()
                    self.landing_time = self.sim_time
                    self.show_landing_marker = True
                
                # Continue simulation for a few seconds to show landing
                if landing == "trees":
                    # Wait 2 seconds to show tree landing, then go to recovery
                    if self.sim_time - self.landing_time > 2.0:
                        self.state = "recovery"
                        self.rocket_tree_x = self.simulation.rocket.position[0] - 54.85
                        self.rocket_tree_height = tree_height
                        self.baseball_attempts = 0
                        return  # Stop simulation updates
                else:
                    # Wait 3 seconds to show successful field landing
                    if self.sim_time - self.landing_time > 3.0:
                        self.state = "results"
                        return  # Stop simulation updates
            
            self.sim_time += self.time_step
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if self.state == "menu":
                    if event.key == pygame.K_a:
                        self.selected_engine = 'A'
                    elif event.key == pygame.K_b:
                        self.selected_engine = 'B'
                    elif event.key == pygame.K_c:
                        self.selected_engine = 'C'
                    elif event.key == pygame.K_SPACE:
                        self.start_flight()
                    elif event.key == pygame.K_UP:
                        self.wind_speed = min(10, self.wind_speed + 0.5)
                    elif event.key == pygame.K_DOWN:
                        self.wind_speed = max(0, self.wind_speed - 0.5)
                    elif event.key == pygame.K_LEFT:
                        self.wind_direction = (self.wind_direction - 15) % 360
                    elif event.key == pygame.K_RIGHT:
                        self.wind_direction = (self.wind_direction + 15) % 360
                    elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        return False  # Quit game
                
                elif self.state == "recovery":
                    if event.key == pygame.K_UP:
                        self.baseball_angle = min(90, self.baseball_angle + 5)
                    elif event.key == pygame.K_DOWN:
                        self.baseball_angle = max(0, self.baseball_angle - 5)
                    elif event.key == pygame.K_LEFT:
                        self.baseball_power = max(0.1, self.baseball_power - 0.05)
                    elif event.key == pygame.K_RIGHT:
                        self.baseball_power = min(1.0, self.baseball_power + 0.05)
                    elif event.key == pygame.K_SPACE:
                        self.throw_baseball()
                
                elif self.state == "results":
                    if event.key == pygame.K_SPACE:
                        self.state = "menu"
        
        return True
    
    def throw_baseball(self):
        self.baseball_attempts += 1
        
        # Run animation and get whether hit occurred
        hit_occurred = self.animate_baseball_throw()
        
        # If hit occurred during animation, show rocket falling
        if hit_occurred:
            self.animate_rocket_falling()
            self.state = "results"
        elif self.baseball_attempts >= self.max_attempts:
            self.state = "results"
    
    def animate_rocket_falling(self):
        """Show rocket falling from tree after being hit"""
        start_time = pygame.time.get_ticks()
        ground_y = SCREEN_HEIGHT - 100
        tree_x = SCREEN_WIDTH // 2 + self.rocket_tree_x
        
        # Starting position in tree
        start_y = ground_y - self.rocket_tree_height * 10
        
        while pygame.time.get_ticks() - start_time < 1500:  # 1.5 second fall
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            
            # Draw background and trees (but not the stuck rocket)
            self.draw_background()
            
            # Draw trees with NO stuck rocket
            self.draw_tree(tree_x, ground_y)
            
            # Draw player
            player_x = 100
            player_y = ground_y - 20
            pygame.draw.circle(self.screen, (255, 220, 177), (player_x, player_y - 10), 8)  # Head
            pygame.draw.line(self.screen, BLACK, (player_x, player_y - 2), (player_x, player_y + 15), 3)  # Body
            pygame.draw.line(self.screen, BLACK, (player_x - 8, player_y + 5), (player_x + 8, player_y + 5), 3)  # Arms
            pygame.draw.line(self.screen, BLACK, (player_x - 5, player_y + 15), (player_x + 5, player_y + 15), 3)  # Legs
            
            # Calculate falling rocket position
            t = (pygame.time.get_ticks() - start_time) / 1500.0
            if t <= 1.0:
                # Simple gravity fall
                fall_distance = 0.5 * 981 * (t * 1.5)**2  # gravity in cm/s^2, 1.5 sec fall time
                rocket_y = start_y + fall_distance
                rocket_y = min(rocket_y, ground_y)  # Don't go below ground
                
                # Draw ONLY the falling rocket (no duplicate)
                falling_rocket = RocketSprite(tree_x + 10, rocket_y)
                falling_rocket.scale = 0.8
                falling_rocket.draw_rocket(self.screen)
            
            pygame.display.flip()
            self.clock.tick(FPS)
    
    def run(self):
        running = True
        
        while running:
            running = self.handle_events()
            
            if self.state == "menu":
                self.draw_menu()
            elif self.state == "countdown":
                self.draw_countdown()
            elif self.state == "flying":
                self.update_simulation()
                self.draw_flight()
            elif self.state == "recovery":
                self.draw_baseball_game()
            elif self.state == "results":
                self.draw_background()
                result_text = self.font.render("Mission Complete! Press SPACE for new flight", True, BLACK)
                result_rect = result_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
                self.screen.blit(result_text, result_rect)
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()

if __name__ == "__main__":
    game = VisualRocketGame()
    game.run()