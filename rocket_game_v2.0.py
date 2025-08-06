import pygame
import numpy as np
import math
import random
from rocket_simulation import RocketSimulation, ENGINES

# Initialize Pygame
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

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
PURPLE = (128, 0, 128)
LIME_GREEN = (50, 205, 50)
SILVER = (192, 192, 192)
GOLD = (255, 215, 0)

class SoundManager:
    def __init__(self):
        self.sounds_enabled = True
        self.music_enabled = False  # Disabled background music
        self.volume = 0.7
        self.current_music = None
        
        # Create synthesized sound effects
        self.create_sound_effects()
        
    def create_sound_effects(self):
        """Create synthesized sound effects using pygame"""
        import numpy as np
        
        # Rocket launch sound (whoosh with engine roar)
        duration = 2.0
        sample_rate = 22050
        frames = int(duration * sample_rate)
        
        # Create rocket launch sound
        arr = np.zeros((frames, 2))
        for i in range(frames):
            t = float(i) / sample_rate
            # White noise for engine roar
            noise = np.random.uniform(-0.3, 0.3)
            # Low frequency rumble
            rumble = 0.4 * np.sin(2 * np.pi * 80 * t) * np.exp(-t * 0.5)
            # High frequency whoosh
            whoosh = 0.2 * np.sin(2 * np.pi * 400 * t) * np.exp(-t * 2.0)
            
            sound = noise + rumble + whoosh
            arr[i] = [sound, sound]
        
        # Convert to pygame sound
        arr = (arr * 32767).astype(np.int16)
        self.rocket_launch = pygame.sndarray.make_sound(arr)
        
        # Countdown beep
        frames = int(0.3 * sample_rate)
        arr = np.zeros((frames, 2))
        for i in range(frames):
            t = float(i) / sample_rate
            beep = 0.3 * np.sin(2 * np.pi * 800 * t) * np.exp(-t * 8)
            arr[i] = [beep, beep]
        arr = (arr * 32767).astype(np.int16)
        self.countdown_beep = pygame.sndarray.make_sound(arr)
        
        # Collection sound (crystal/energy pickup)
        frames = int(0.5 * sample_rate)
        arr = np.zeros((frames, 2))
        for i in range(frames):
            t = float(i) / sample_rate
            ding = 0.4 * np.sin(2 * np.pi * 1200 * t) * np.exp(-t * 4)
            ding += 0.2 * np.sin(2 * np.pi * 1600 * t) * np.exp(-t * 6)
            arr[i] = [ding, ding]
        arr = (arr * 32767).astype(np.int16)
        self.collect_sound = pygame.sndarray.make_sound(arr)
        
        # Time travel sound (magical whoosh)
        frames = int(1.5 * sample_rate)
        arr = np.zeros((frames, 2))
        for i in range(frames):
            t = float(i) / sample_rate
            freq = 200 + 800 * t  # Rising frequency
            magic = 0.3 * np.sin(2 * np.pi * freq * t) * (1 - t/1.5)
            # Add some reverb-like effect
            if i > 1000:
                magic += 0.1 * arr[i-1000][0]
            arr[i] = [magic, magic]
        arr = (arr * 32767).astype(np.int16)
        self.time_travel_sound = pygame.sndarray.make_sound(arr)
        
        # Baseball hit sound
        frames = int(0.2 * sample_rate)
        arr = np.zeros((frames, 2))
        for i in range(frames):
            t = float(i) / sample_rate
            # Sharp crack sound
            crack = 0.5 * np.random.uniform(-1, 1) * np.exp(-t * 15)
            arr[i] = [crack, crack]
        arr = (arr * 32767).astype(np.int16)
        self.baseball_hit = pygame.sndarray.make_sound(arr)
        
        # Parachute deploy sound
        frames = int(0.8 * sample_rate)
        arr = np.zeros((frames, 2))
        for i in range(frames):
            t = float(i) / sample_rate
            # Soft whoosh
            whoosh = 0.2 * np.sin(2 * np.pi * 120 * t) * np.exp(-t * 2)
            arr[i] = [whoosh, whoosh]
        arr = (arr * 32767).astype(np.int16)
        self.parachute_deploy = pygame.sndarray.make_sound(arr)
        
        # Game over sound (dramatic downward spiral)
        frames = int(2.0 * sample_rate)
        arr = np.zeros((frames, 2))
        for i in range(frames):
            t = float(i) / sample_rate
            freq = 400 * np.exp(-t * 2)  # Falling frequency
            drama = 0.4 * np.sin(2 * np.pi * freq * t) * (1 - t/2.0)
            # Add some dissonance
            drama += 0.2 * np.sin(2 * np.pi * freq * 0.7 * t) * (1 - t/2.0)
            arr[i] = [drama, drama]
        arr = (arr * 32767).astype(np.int16)
        self.game_over_sound = pygame.sndarray.make_sound(arr)
        
        # Menu click sound
        frames = int(0.1 * sample_rate)
        arr = np.zeros((frames, 2))
        for i in range(frames):
            t = float(i) / sample_rate
            click = 0.3 * np.sin(2 * np.pi * 600 * t) * np.exp(-t * 20)
            arr[i] = [click, click]
        arr = (arr * 32767).astype(np.int16)
        self.menu_click = pygame.sndarray.make_sound(arr)
        
        # Wind ambient sound
        frames = int(3.0 * sample_rate)
        arr = np.zeros((frames, 2))
        for i in range(frames):
            t = float(i) / sample_rate
            # Soft wind noise
            wind = 0.1 * np.random.uniform(-1, 1) * np.sin(2 * np.pi * 0.5 * t)
            arr[i] = [wind, wind]
        arr = (arr * 32767).astype(np.int16)
        self.wind_ambient = pygame.sndarray.make_sound(arr)
        
        # Dinosaur roar
        frames = int(1.5 * sample_rate)
        arr = np.zeros((frames, 2))
        for i in range(frames):
            t = float(i) / sample_rate
            # Deep roar with harmonics
            roar = 0.4 * np.sin(2 * np.pi * 120 * t) * np.exp(-t * 0.8)
            roar += 0.2 * np.sin(2 * np.pi * 240 * t) * np.exp(-t * 1.2)
            roar += 0.1 * np.random.uniform(-0.5, 0.5)  # Add growl texture
            arr[i] = [roar, roar]
        arr = (arr * 32767).astype(np.int16)
        self.dinosaur_roar = pygame.sndarray.make_sound(arr)
        
        # Robot beep
        frames = int(0.4 * sample_rate)
        arr = np.zeros((frames, 2))
        for i in range(frames):
            t = float(i) / sample_rate
            # Electronic beeping
            beep = 0.3 * np.sin(2 * np.pi * 880 * t) * np.exp(-t * 5)
            beep += 0.2 * np.sin(2 * np.pi * 1760 * t) * np.exp(-t * 8)
            arr[i] = [beep, beep]
        arr = (arr * 32767).astype(np.int16)
        self.robot_beep = pygame.sndarray.make_sound(arr)
        
    def play_sound(self, sound_name):
        """Play a sound effect"""
        if not self.sounds_enabled:
            return
            
        try:
            sound = getattr(self, sound_name)
            sound.set_volume(self.volume)
            sound.play()
        except AttributeError:
            pass  # Sound doesn't exist
    
    def create_background_music(self, music_type, duration=30.0):
        """Create looping background music"""
        import numpy as np
        
        sample_rate = 22050
        frames = int(duration * sample_rate)
        arr = np.zeros((frames, 2))
        
        if music_type == "menu":
            # Peaceful ambient menu music
            for i in range(frames):
                t = float(i) / sample_rate
                # Soft pad chords
                chord = 0.1 * np.sin(2 * np.pi * 220 * t)  # A3
                chord += 0.08 * np.sin(2 * np.pi * 277.18 * t)  # C#4
                chord += 0.06 * np.sin(2 * np.pi * 329.63 * t)  # E4
                # Add some subtle movement
                chord *= (1 + 0.2 * np.sin(2 * np.pi * 0.1 * t))
                arr[i] = [chord, chord]
                
        elif music_type == "flight":
            # Exciting flight music
            for i in range(frames):
                t = float(i) / sample_rate
                # Driving bassline
                bass = 0.15 * np.sin(2 * np.pi * 110 * t)  # A2
                # Exciting melody
                melody_freq = 440 + 100 * np.sin(2 * np.pi * 0.5 * t)
                melody = 0.1 * np.sin(2 * np.pi * melody_freq * t)
                # Add some percussion-like hits
                if int(t * 4) % 4 == 0:  # Every beat
                    percussion = 0.05 * np.exp(-(t % 0.25) * 20)
                else:
                    percussion = 0
                music = bass + melody + percussion
                arr[i] = [music, music]
                
        elif music_type == "time_travel":
            # Mystical time travel ambient
            for i in range(frames):
                t = float(i) / sample_rate
                # Ethereal pads with modulation
                pad1 = 0.08 * np.sin(2 * np.pi * 333 * t) * (1 + 0.3 * np.sin(2 * np.pi * 0.3 * t))
                pad2 = 0.06 * np.sin(2 * np.pi * 444 * t) * (1 + 0.2 * np.sin(2 * np.pi * 0.7 * t))
                # Add some sparkle
                sparkle = 0.04 * np.sin(2 * np.pi * 1333 * t) * np.sin(2 * np.pi * 0.1 * t)
                music = pad1 + pad2 + sparkle
                arr[i] = [music, music]
        
        # Convert to pygame sound
        arr = (arr * 32767).astype(np.int16)
        return pygame.sndarray.make_sound(arr)
    
    def play_background_music(self, music_type):
        """Generate and play background music"""
        if not self.music_enabled:
            return
            
        # Stop current music
        if hasattr(self, 'current_music_channel'):
            self.current_music_channel.stop()
            
        # Create and play new music
        if music_type != self.current_music:
            music_sound = self.create_background_music(music_type)
            music_sound.set_volume(self.volume * 0.3)  # Lower volume for background
            self.current_music_channel = music_sound.play(loops=-1)  # Loop forever
            self.current_music = music_type
            
    def toggle_sounds(self):
        """Toggle sound effects on/off"""
        self.sounds_enabled = not self.sounds_enabled
        
    def toggle_music(self):
        """Toggle background music on/off"""
        self.music_enabled = not self.music_enabled
        if not self.music_enabled:
            pygame.mixer.music.stop()
    
    def set_volume(self, volume):
        """Set master volume (0.0 to 1.0)"""
        self.volume = max(0.0, min(1.0, volume))

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
        pygame.display.set_caption("Estes Alpha III Rocket Simulation v2.0 - Time Travel Edition")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Initialize sound manager
        self.sound_manager = SoundManager()
        
        # Game state
        self.state = "menu"  # menu, countdown, flying, recovery, time_travel, results
        self.rocket_sprite = None
        self.simulation = None
        self.sim_time = 0
        self.time_step = 0.033  # ~30 FPS simulation steps for faster falling
        self.scale_factor = 2.5  # pixels per meter (much bigger field)
        
        # Manual parachute control
        self.manual_parachute_triggered = False
        
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
        # Randomize initial wind conditions for more variety
        self.wind_speed = random.uniform(0.5, 8.0)  # Random wind 0.5-8.0 m/s
        self.wind_direction = random.randint(0, 23) * 15  # Random direction in 15° increments
        
        # Baseball game variables
        self.baseball_angle = 45
        self.baseball_power = 0.5
        self.baseball_attempts = 0
        self.max_attempts = 10
        self.rocket_tree_x = 0
        self.rocket_tree_height = 6
        self.baseball_player_x = 100  # Player position in baseball game
        
        # Animation variables
        self.trajectory_points = []
        
        # Time travel mini-game variables
        self.time_era = "present"  # present, past, future
        self.time_power = 0.5
        self.collected_crystals = 0
        self.collected_energy = 0
        self.time_machine_x = SCREEN_WIDTH // 2
        self.time_machine_y = SCREEN_HEIGHT - 150
        self.player_x = 200
        self.dinosaur_x = SCREEN_WIDTH - 200
        self.robot_x = SCREEN_WIDTH - 300
        self.dinosaur_direction = random.choice([-1, 1])  # Movement direction
        self.dinosaur_stuck_counter = 0  # Counter to detect stuck state
        self.dinosaur_last_x = self.dinosaur_x  # Track previous position
        self.game_over_time = 0
        self.is_game_over = False
        self.player_y = SCREEN_HEIGHT - 120  # Ground level for player
        self.jump_velocity = 0
        self.is_jumping = False
        self.jump_start_time = 0
        self.jump_start_x = 0  # Starting X position for jump
        
        # Creature movement controls
        self.dinosaur_movement_enabled = False
        self.robot_movement_enabled = False
        
        # Win condition variables
        self.player_won = False
        self.win_start_time = 0
        
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
    
    def draw_time_machine(self, screen, x, y):
        # Garbage can base (silver/gray cylinder with details)
        can_width = 40
        can_height = 60
        pygame.draw.rect(screen, SILVER, (x - can_width//2, y - can_height, can_width, can_height))
        pygame.draw.ellipse(screen, GRAY, (x - can_width//2, y - can_height - 5, can_width, 10))
        
        # Add vertical ridges to garbage can
        for i in range(3):
            ridge_x = x - can_width//2 + 8 + i * 12
            pygame.draw.line(screen, GRAY, (ridge_x, y - can_height + 5), (ridge_x, y - 5), 1)
        
        # More realistic toilet seat - half blue, half red
        seat_width = 50
        seat_height = 15
        seat_thickness = 4
        
        # Draw outer rim in two halves
        # Left half (blue)
        blue_rect = pygame.Rect(x - seat_width//2, y - can_height - 20, seat_width//2, seat_height)
        pygame.draw.ellipse(screen, BLUE, blue_rect)
        
        # Right half (red)  
        red_rect = pygame.Rect(x, y - can_height - 20, seat_width//2, seat_height)
        pygame.draw.ellipse(screen, RED, red_rect)
        
        # Draw the complete outer ellipse outline
        pygame.draw.ellipse(screen, BLACK, (x - seat_width//2, y - can_height - 20, seat_width, seat_height), 2)
        
        # Inner hole (toilet opening)
        inner_width = 28
        inner_height = 8
        pygame.draw.ellipse(screen, BLACK, (x - inner_width//2, y - can_height - 17, inner_width, inner_height))
        
        # Add toilet seat hinge details
        hinge_y = y - can_height - 20
        pygame.draw.circle(screen, SILVER, (x - 20, hinge_y), 3)
        pygame.draw.circle(screen, SILVER, (x + 20, hinge_y), 3)
        pygame.draw.circle(screen, BLACK, (x - 20, hinge_y), 1)
        pygame.draw.circle(screen, BLACK, (x + 20, hinge_y), 1)
        
        # Time machine effects (swirling energy)
        if self.time_era != "present":
            for i in range(8):
                angle = (pygame.time.get_ticks() * 0.01 + i * math.pi / 4) % (2 * math.pi)
                effect_x = x + 30 * math.cos(angle)
                effect_y = y - 30 + 20 * math.sin(angle)
                color = PURPLE if i % 2 == 0 else GOLD
                pygame.draw.circle(screen, color, (int(effect_x), int(effect_y)), 3)
    
    def draw_crystal(self, screen, x, y, collected=False):
        if not collected:
            # Draw glowing crystal
            crystal_points = [
                (x, y - 10),  # top
                (x - 8, y - 5),
                (x - 8, y + 5),
                (x, y + 10),  # bottom
                (x + 8, y + 5),
                (x + 8, y - 5)
            ]
            pygame.draw.polygon(screen, LIME_GREEN, crystal_points)
            # Glow effect
            pygame.draw.circle(screen, (50, 255, 50, 50), (x, y), 15, 2)
    
    def draw_energy_orb(self, screen, x, y, collected=False):
        if not collected:
            # Draw floating energy orb
            pulse = 1.0 + 0.3 * math.sin(pygame.time.get_ticks() * 0.01)
            size = int(8 * pulse)
            pygame.draw.circle(screen, GOLD, (x, y), size)
            pygame.draw.circle(screen, YELLOW, (x, y), size - 2)
            # Electric effect
            for i in range(4):
                angle = i * math.pi / 2 + pygame.time.get_ticks() * 0.02
                spark_x = x + 15 * math.cos(angle)
                spark_y = y + 15 * math.sin(angle)
                pygame.draw.line(screen, YELLOW, (x, y), (spark_x, spark_y), 2)
    
    def draw_menu(self):
        self.screen.fill(SKY_BLUE)
        
        # Title
        title = self.font.render("ESTES ALPHA III ROCKET SIMULATOR v2.0", True, BLACK)
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
        wind_text = self.small_font.render(f"Wind: {self.wind_speed:.1f} m/s from {self.wind_direction:.0f}° (RANDOMIZED)", True, BLACK)
        self.screen.blit(wind_text, (50, 350))
        
        wind_help = self.small_font.render("Press UP/DOWN: wind speed, LEFT/RIGHT: direction, W: randomize", True, GRAY)
        self.screen.blit(wind_help, (50, 375))
        
        # Wind strength indicator
        wind_strength = "CALM" if self.wind_speed < 2 else "MODERATE" if self.wind_speed < 5 else "STRONG"
        wind_color = GREEN if self.wind_speed < 2 else ORANGE if self.wind_speed < 5 else RED
        strength_text = self.small_font.render(f"Wind Strength: {wind_strength}", True, wind_color)
        self.screen.blit(strength_text, (50, 400))
        
        # Launch button
        launch_text = self.font.render("Press SPACE to LAUNCH!", True, RED)
        launch_rect = launch_text.get_rect(center=(SCREEN_WIDTH//2, 500))
        self.screen.blit(launch_text, launch_rect)
        
        # Time travel feature hint
        time_hint = self.small_font.render("Successful missions unlock TIME TRAVEL! 🚀", True, PURPLE)
        time_rect = time_hint.get_rect(center=(SCREEN_WIDTH//2, 550))
        self.screen.blit(time_hint, time_rect)
        
        # Sound controls
        sound_status = "ON" if self.sound_manager.sounds_enabled else "OFF"
        sound_text = self.small_font.render(f"Sound Effects: {sound_status} (Press S to toggle)", True, BLACK)
        self.screen.blit(sound_text, (50, 650))
        
        volume_text = self.small_font.render(f"Volume: {int(self.sound_manager.volume * 100)}% (Press -/+ to adjust)", True, BLACK)
        self.screen.blit(volume_text, (50, 675))
        
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
            
            # Play countdown beep for each second
            prev_second = getattr(self, '_prev_countdown_second', 0)
            if seconds_left != prev_second and seconds_left > 0:
                self.sound_manager.play_sound('countdown_beep')
                self._prev_countdown_second = seconds_left
            
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
            # Play rocket launch sound when flight begins
            if not getattr(self, '_launch_sound_played', False):
                self.sound_manager.play_sound('rocket_launch')
                self._launch_sound_played = True
    
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
            
            # Check landing status first to determine proper visual height
            if self.simulation:
                landing_zone = self.simulation.check_landing_location()
                
                # If rocket has landed, use fixed visual positions
                if self.show_landing_marker:
                    if landing_zone == "trees":
                        # Rocket is stuck in trees - show at tree height
                        screen_y = ground_level - 60  # Tree height visual position
                    else:
                        # Rocket landed on field - show at ground level
                        screen_y = ground_level
                else:
                    # Rocket is still flying - use physics position
                    screen_y = ground_level - current_pos[1] * vertical_scale
                    
                    # Keep rocket on screen - if it goes too high, scale it down more
                    if screen_y < 50:  # Too high
                        vertical_scale = 0.3
                        screen_y = ground_level - current_pos[1] * vertical_scale
            else:
                screen_y = ground_level - current_pos[1] * vertical_scale
            
            # Draw rocket
            if self.rocket_sprite:
                self.rocket_sprite.x = screen_x
                self.rocket_sprite.y = screen_y
                
                # Add exhaust particles during burn phase
                engine_burning = self.sim_time <= self.simulation.engine.burn_time
                if (engine_burning and not self.rocket_sprite.parachute_deployed):
                    self.rocket_sprite.add_exhaust_particle(engine_burning)
                
                # Deploy parachute (only if manually triggered or automatic fallback)
                if self.simulation.rocket.parachute_deployed:
                    if not self.rocket_sprite.parachute_deployed:
                        self.sound_manager.play_sound('parachute_deploy')
                    self.rocket_sprite.parachute_deployed = True
                
                self.rocket_sprite.update_particles()
                self.rocket_sprite.draw_particles(self.screen)
                self.rocket_sprite.draw_rocket(self.screen)
                self.rocket_sprite.draw_parachute(self.screen)
            
            # Simple trajectory trail (only add points if rocket is still moving)
            if (len(self.simulation.velocity_history) == 0 or 
                np.linalg.norm(self.simulation.velocity_history[-1]) > 0.1):  # Only if moving
                self.trajectory_points.append((screen_x, screen_y))
                if len(self.trajectory_points) > 100:
                    self.trajectory_points.pop(0)
            
            # Draw trajectory trail
            if len(self.trajectory_points) > 1:
                pygame.draw.lines(self.screen, YELLOW, False, self.trajectory_points, 2)
        
        # Draw landing marker if rocket has landed
        if self.show_landing_marker and self.landing_position is not None:
            landing_screen_x = SCREEN_WIDTH // 2 + (self.landing_position[0] - 54.85) * self.scale_factor
            
            # Check if landing is in trees or field
            field_start = 0
            field_end = 109.7
            is_in_field = field_start <= self.landing_position[0] <= field_end
            
            if is_in_field:
                # Landing marker at ground level for field landing
                landing_screen_y = SCREEN_HEIGHT - 100
            else:
                # Landing marker at tree height for tree landing
                landing_screen_y = SCREEN_HEIGHT - 100 - 80  # Match the visual tree height
            
            # Pulsing landing marker
            pulse = int(20 * (1 + math.sin(pygame.time.get_ticks() * 0.01)))
            pygame.draw.circle(self.screen, RED, (int(landing_screen_x), int(landing_screen_y)), 15 + pulse, 3)
            pygame.draw.circle(self.screen, WHITE, (int(landing_screen_x), int(landing_screen_y)), 5)
            
            # Landing text positioning
            if is_in_field:
                landing_text = "LANDED HERE!"
                text_color = GREEN
            else:
                landing_text = "STUCK IN TREES!"
                text_color = RED
            
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
        
        # Add parachute deployment instructions
        if (not self.simulation.rocket.parachute_deployed and 
            self.sim_time > self.simulation.engine.burn_time):
            info_texts.append("Press SPACE to deploy parachute!")
        
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
            self.screen.blit(phase_text, (SCREEN_WIDTH - 250, 10))
        
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
        rocket_screen_height = ground_y - self.rocket_tree_height * 13  # Convert meters to pixels (increased multiplier for better visibility)
        stuck_rocket = RocketSprite(tree_x + 10, rocket_screen_height)
        stuck_rocket.scale = 0.8
        stuck_rocket.draw_rocket(self.screen)
        
        # Player position (stick figure) - now moveable
        player_x = self.baseball_player_x
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
            "A/D keys: Move left/right",
            "Press SPACE to throw!"
        ]
        
        for i, text in enumerate(info_texts):
            rendered = self.small_font.render(text, True, BLACK)
            self.screen.blit(rendered, (50, 100 + i * 30))
        
        # Distance indicator - calculate from player position to tree
        tree_screen_x = SCREEN_WIDTH // 2 + self.rocket_tree_x
        distance_pixels = abs(tree_screen_x - self.baseball_player_x)
        distance_meters = distance_pixels / 10  # Rough conversion to meters for display
        dist_text = self.small_font.render(f"Distance to rocket: {distance_meters:.0f}m", True, RED)
        self.screen.blit(dist_text, (50, 250))
    
    def draw_time_travel_game(self):
        # Background based on era
        if self.time_era == "past":
            # Prehistoric background - dark green/brown
            for y in range(SCREEN_HEIGHT):
                color_ratio = y / SCREEN_HEIGHT
                r = int(50 * (1 - color_ratio) + 100 * color_ratio)
                g = int(100 * (1 - color_ratio) + 150 * color_ratio)
                b = int(0 * (1 - color_ratio) + 50 * color_ratio)
                pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        elif self.time_era == "future":
            # Futuristic background - dark blue/purple
            for y in range(SCREEN_HEIGHT):
                color_ratio = y / SCREEN_HEIGHT
                r = int(20 * (1 - color_ratio) + 80 * color_ratio)
                g = int(20 * (1 - color_ratio) + 50 * color_ratio)
                b = int(80 * (1 - color_ratio) + 150 * color_ratio)
                pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        else:
            # Present day - normal sky
            self.screen.fill(SKY_BLUE)
        
        # Ground
        ground_y = SCREEN_HEIGHT - 100
        if self.time_era == "past":
            pygame.draw.rect(self.screen, BROWN, (0, ground_y, SCREEN_WIDTH, 100))
        elif self.time_era == "future":
            pygame.draw.rect(self.screen, SILVER, (0, ground_y, SCREEN_WIDTH, 100))
        else:
            pygame.draw.rect(self.screen, GREEN, (0, ground_y, SCREEN_WIDTH, 100))
        
        # Era-specific elements
        if self.time_era == "past":
            # Draw dinosaur (T-Rex)
            dino_x = self.dinosaur_x
            dino_y = ground_y - 80
            # Body
            pygame.draw.ellipse(self.screen, DARK_GREEN, (dino_x - 30, dino_y, 60, 40))
            # Head
            pygame.draw.ellipse(self.screen, DARK_GREEN, (dino_x + 20, dino_y - 20, 25, 25))
            # Tail
            pygame.draw.ellipse(self.screen, DARK_GREEN, (dino_x - 60, dino_y + 10, 40, 15))
            # Legs
            pygame.draw.rect(self.screen, DARK_GREEN, (dino_x - 15, dino_y + 35, 8, 20))
            pygame.draw.rect(self.screen, DARK_GREEN, (dino_x + 10, dino_y + 35, 8, 20))
            # Eyes
            pygame.draw.circle(self.screen, RED, (dino_x + 35, dino_y - 15), 3)
            
            # Draw crystals
            for i, x in enumerate([300, 500, 800]):
                collected = self.collected_crystals > i
                self.draw_crystal(self.screen, x, ground_y - 30, collected)
                
        elif self.time_era == "future":
            # Draw robot
            robot_x = self.robot_x
            robot_y = ground_y - 60
            # Body
            pygame.draw.rect(self.screen, SILVER, (robot_x - 15, robot_y, 30, 40))
            # Head
            pygame.draw.rect(self.screen, SILVER, (robot_x - 10, robot_y - 20, 20, 20))
            # Arms
            pygame.draw.rect(self.screen, SILVER, (robot_x - 25, robot_y + 10, 10, 20))
            pygame.draw.rect(self.screen, SILVER, (robot_x + 15, robot_y + 10, 10, 20))
            # Legs
            pygame.draw.rect(self.screen, SILVER, (robot_x - 10, robot_y + 35, 8, 20))
            pygame.draw.rect(self.screen, SILVER, (robot_x + 2, robot_y + 35, 8, 20))
            # Eyes (glowing)
            pygame.draw.circle(self.screen, BLUE, (robot_x - 5, robot_y - 15), 2)
            pygame.draw.circle(self.screen, BLUE, (robot_x + 5, robot_y - 15), 2)
            
            # Flying cars in sky
            for i, x in enumerate([200, 600, 1000]):
                car_y = 150 + 30 * math.sin(pygame.time.get_ticks() * 0.005 + i)
                pygame.draw.ellipse(self.screen, SILVER, (x, car_y, 40, 15))
                pygame.draw.circle(self.screen, BLUE, (x + 10, car_y + 7), 3)
                pygame.draw.circle(self.screen, BLUE, (x + 30, car_y + 7), 3)
            
            # Draw energy orbs
            for i, x in enumerate([350, 550, 750]):
                collected = self.collected_energy > i
                self.draw_energy_orb(self.screen, x, ground_y - 40, collected)
        
        # Draw time machine
        self.draw_time_machine(self.screen, self.time_machine_x, self.time_machine_y)
        
        # Draw player (stick figure) with jump animation
        player_y = self.player_y
        pygame.draw.circle(self.screen, (255, 220, 177), (self.player_x, int(player_y - 10)), 8)  # Head
        pygame.draw.line(self.screen, BLACK, (self.player_x, int(player_y - 2)), (self.player_x, int(player_y + 15)), 3)  # Body
        pygame.draw.line(self.screen, BLACK, (self.player_x - 8, int(player_y + 5)), (self.player_x + 8, int(player_y + 5)), 3)  # Arms
        
        # Legs change based on jumping state
        if self.is_jumping:
            # Legs tucked up while jumping
            pygame.draw.line(self.screen, BLACK, (self.player_x - 3, int(player_y + 12)), (self.player_x + 3, int(player_y + 12)), 3)  # Tucked legs
        else:
            # Normal standing legs
            pygame.draw.line(self.screen, BLACK, (self.player_x - 5, int(player_y + 15)), (self.player_x + 5, int(player_y + 15)), 3)  # Legs
        
        # UI
        title = self.font.render("TIME TRAVEL ADVENTURE", True, WHITE if self.time_era != "present" else BLACK)
        self.screen.blit(title, (50, 50))
        
        era_text = f"Era: {self.time_era.upper()}"
        if self.time_era == "past":
            era_text += " (Dinosaur Age)"
        elif self.time_era == "future":
            era_text += " (Year 3000)"
        
        info_texts = [
            era_text,
            f"Time Power: {self.time_power:.2f} (LEFT/RIGHT arrows)",
            "UP/DOWN: Choose era",
            f"Crystals: {self.collected_crystals}/3" if self.time_era == "past" else f"Energy: {self.collected_energy}/3" if self.time_era == "future" else "WASD: Move around",
            "E or SPACE: Jump over creatures to avoid collision",
            "Press 4 or 5: Start creature movement",
            "Collect all items and jump into time machine to win!",
            "Press R to return to rocket game"
        ]
        
        text_color = WHITE if self.time_era != "present" else BLACK
        for i, text in enumerate(info_texts):
            rendered = self.small_font.render(text, True, text_color)
            self.screen.blit(rendered, (50, 100 + i * 30))
        
        # Win condition overlay
        if self.player_won:
            # Check if player reached time machine
            time_machine_distance = abs(self.player_x - self.time_machine_x)
            if time_machine_distance < 60:  # Player reached time machine
                # Dark overlay
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                overlay.fill(BLACK)
                overlay.set_alpha(150)
                self.screen.blit(overlay, (0, 0))
                
                # YOU WIN text with pulsing effect
                pulse = 1.0 + 0.3 * math.sin(pygame.time.get_ticks() * 0.01)
                font_size = int(120 * pulse)
                big_font = pygame.font.Font(None, font_size)
                
                win_text = big_font.render("YOU WIN!!!", True, GOLD)
                win_rect = win_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
                self.screen.blit(win_text, win_rect)
                
                # Restart message
                restart_text = self.small_font.render("Press ENTER to return to main menu", True, WHITE)
                restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 80))
                self.screen.blit(restart_text, restart_rect)
                
                return  # Don't draw game over overlay
        
        # Game over overlay
        if self.is_game_over:
            # Dark overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.fill(BLACK)
            overlay.set_alpha(150)
            self.screen.blit(overlay, (0, 0))
            
            # Game over text with pulsing effect
            pulse = 1.0 + 0.3 * math.sin(pygame.time.get_ticks() * 0.01)
            font_size = int(80 * pulse)
            big_font = pygame.font.Font(None, font_size)
            
            # Determine cause of death
            if self.time_era == "past":
                death_cause = "EATEN BY DINOSAUR!"
                death_color = RED
            else:
                death_cause = "DESTROYED BY ROBOT!"
                death_color = BLUE
            
            game_over_text = big_font.render("GAME OVER", True, RED)
            cause_text = self.font.render(death_cause, True, death_color)
            restart_text = self.small_font.render("Press SPACEBAR to start over at rocket launch", True, WHITE)
            
            # Center the text
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
            cause_rect = cause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 80))
            
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(cause_text, cause_rect)
            self.screen.blit(restart_text, restart_rect)
    
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
                player_x = self.baseball_player_x
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
                    rocket_y = SCREEN_HEIGHT - 100 - self.rocket_tree_height * 13  # Match the visual height
                    
                    distance = math.sqrt((x - rocket_x)**2 + (y - rocket_y)**2)
                    if distance < 20 and not hit_occurred:
                        hit_occurred = True
                        hit_time = pygame.time.get_ticks()
                        self.sound_manager.play_sound('baseball_hit')
            
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
        
        # Reset sound flags
        self._launch_sound_played = False
        self._prev_countdown_second = 0
        
        # Reset manual parachute control
        self.manual_parachute_triggered = False
        
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
            
            # Parachute deployment is now manual only (handled in event handler)
            # No automatic deployment - player must press spacebar
            
            # Calculate forces
            thrust = self.simulation.thrust_force(time)
            drag = self.simulation.drag_force(self.simulation.rocket.velocity)
            gravity = np.array([0.0, -self.simulation.rocket.mass * self.simulation.g])
            
            # Add wind force throughout flight (horizontal only)
            wind_force = np.array([0.0, 0.0])
            if time <= self.simulation.engine.burn_time:
                # Light wind during powered flight
                wind_force = np.array([self.simulation.wind_vector[0] * 0.02, 0.0])
            elif self.simulation.rocket.parachute_deployed:
                # Stronger wind force during parachute descent
                wind_force = np.array([self.simulation.wind_vector[0] * 0.05, 0.0])
            else:
                # Medium wind force during unpowered flight (no parachute)
                wind_force = np.array([self.simulation.wind_vector[0] * 0.03, 0.0])
            
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
                self.simulation.rocket.velocity = np.array([0.0, 0.0])  # Stop all movement (horizontal and vertical)
                
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
                        # Keep tree visible on screen by clamping position
                        raw_tree_x = self.simulation.rocket.position[0] - 54.85
                        # Clamp tree position to keep it between 200 pixels from edges
                        max_tree_offset = (SCREEN_WIDTH // 2) - 200
                        min_tree_offset = -(SCREEN_WIDTH // 2) + 200
                        self.rocket_tree_x = max(min_tree_offset, min(max_tree_offset, raw_tree_x))
                        self.rocket_tree_height = tree_height
                        self.baseball_attempts = 0
                        self.baseball_player_x = 100  # Reset player position for baseball game
                        return  # Stop simulation updates
                else:
                    # Wait 3 seconds to show successful field landing
                    if self.sim_time - self.landing_time > 3.0:
                        self.state = "time_travel"  # Go to time travel instead of results
                        self.time_era = "present"
                        self.collected_crystals = 0
                        self.collected_energy = 0
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
                        self.sound_manager.play_sound('menu_click')
                    elif event.key == pygame.K_b:
                        self.selected_engine = 'B'
                        self.sound_manager.play_sound('menu_click')
                    elif event.key == pygame.K_c:
                        self.selected_engine = 'C'
                        self.sound_manager.play_sound('menu_click')
                    elif event.key == pygame.K_SPACE:
                        self.start_flight()
                        self.sound_manager.play_sound('menu_click')
                    elif event.key == pygame.K_UP:
                        self.wind_speed = min(10, self.wind_speed + 0.5)
                    elif event.key == pygame.K_DOWN:
                        self.wind_speed = max(0, self.wind_speed - 0.5)
                    elif event.key == pygame.K_LEFT:
                        self.wind_direction = (self.wind_direction - 15) % 360
                    elif event.key == pygame.K_RIGHT:
                        self.wind_direction = (self.wind_direction + 15) % 360
                    elif event.key == pygame.K_w:
                        # Randomize wind conditions
                        self.wind_speed = random.uniform(0.5, 8.0)
                        self.wind_direction = random.randint(0, 23) * 15
                    elif event.key == pygame.K_s:
                        # Toggle sound effects
                        self.sound_manager.toggle_sounds()
                    elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                        # Decrease volume
                        self.sound_manager.set_volume(self.sound_manager.volume - 0.1)
                    elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS or event.key == pygame.K_EQUALS:
                        # Increase volume
                        self.sound_manager.set_volume(self.sound_manager.volume + 0.1)
                    elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        return False  # Quit game
                
                elif self.state == "flying":
                    if event.key == pygame.K_SPACE:
                        # Manual parachute deployment
                        if (not self.manual_parachute_triggered and 
                            not self.simulation.rocket.parachute_deployed and
                            self.sim_time > self.simulation.engine.burn_time):  # Only after engine burn
                            self.manual_parachute_triggered = True
                            self.simulation.rocket.parachute_deployed = True
                            self.simulation.rocket.flight_phase = "descent"
                            self.sound_manager.play_sound('parachute_deploy')
                
                elif self.state == "recovery":
                    if event.key == pygame.K_UP:
                        self.baseball_angle = min(90, self.baseball_angle + 5)
                    elif event.key == pygame.K_DOWN:
                        self.baseball_angle = max(0, self.baseball_angle - 5)
                    elif event.key == pygame.K_LEFT:
                        self.baseball_power = max(0.1, self.baseball_power - 0.05)
                    elif event.key == pygame.K_RIGHT:
                        self.baseball_power = min(1.0, self.baseball_power + 0.05)
                    elif event.key == pygame.K_a:
                        # Move player left
                        self.baseball_player_x = max(50, self.baseball_player_x - 20)
                    elif event.key == pygame.K_d:
                        # Move player right
                        self.baseball_player_x = min(SCREEN_WIDTH - 50, self.baseball_player_x + 20)
                    elif event.key == pygame.K_SPACE:
                        self.throw_baseball()
                
                elif self.state == "time_travel":
                    if self.player_won:
                        # Player won - wait for Enter key to restart
                        if event.key == pygame.K_RETURN:
                            # Restart entire game to menu
                            self.restart_game()
                            self.sound_manager.play_sound('menu_click')
                    elif self.is_game_over:
                        # Only allow restart when game over
                        if event.key == pygame.K_SPACE:
                            # Restart entire game to menu
                            self.restart_game()
                            self.sound_manager.play_sound('menu_click')
                    else:
                        # Normal time travel controls
                        if event.key == pygame.K_UP:
                            if self.time_era == "present":
                                self.time_era = "past"
                                self.sound_manager.play_sound('time_travel_sound')
                            elif self.time_era == "future":
                                self.time_era = "present"
                                self.sound_manager.play_sound('time_travel_sound')
                        elif event.key == pygame.K_DOWN:
                            if self.time_era == "present":
                                self.time_era = "future"
                                self.sound_manager.play_sound('time_travel_sound')
                            elif self.time_era == "past":
                                self.time_era = "present"
                                self.sound_manager.play_sound('time_travel_sound')
                        elif event.key == pygame.K_LEFT:
                            self.time_power = max(0.1, self.time_power - 0.1)
                        elif event.key == pygame.K_RIGHT:
                            self.time_power = min(1.0, self.time_power + 0.1)
                        elif event.key == pygame.K_w:
                            self.player_x = max(50, self.player_x - 10)
                        elif event.key == pygame.K_s:
                            self.player_x = min(SCREEN_WIDTH - 50, self.player_x + 10)
                        elif event.key == pygame.K_a:
                            self.player_x = max(50, self.player_x - 10)
                        elif event.key == pygame.K_d:
                            self.player_x = min(SCREEN_WIDTH - 50, self.player_x + 10)
                        elif event.key == pygame.K_e or event.key == pygame.K_SPACE:
                            # Jump key (E or SPACE)
                            if not self.is_jumping:
                                self.is_jumping = True
                                self.jump_start_time = pygame.time.get_ticks()
                                self.jump_start_x = self.player_x  # Record starting position
                                self.sound_manager.play_sound('menu_click')  # Jump sound
                        elif event.key == pygame.K_4 or event.key == pygame.K_5:
                            # Start creature movement for current era (either key works)
                            if self.time_era == "past":
                                self.dinosaur_movement_enabled = True
                            elif self.time_era == "future":
                                self.robot_movement_enabled = True
                        elif event.key == pygame.K_r:
                            self.state = "results"
                
                elif self.state == "results":
                    if event.key == pygame.K_SPACE:
                        self.state = "menu"
                        # Randomize wind for next flight
                        self.wind_speed = random.uniform(0.5, 8.0)
                        self.wind_direction = random.randint(0, 23) * 15
        
        return True
    
    def throw_baseball(self):
        self.baseball_attempts += 1
        
        # Run animation and get whether hit occurred
        hit_occurred = self.animate_baseball_throw()
        
        # If hit occurred during animation, show rocket falling
        if hit_occurred:
            self.animate_rocket_falling()
            self.state = "time_travel"  # Go to time travel after successful recovery
            self.time_era = "present"
            self.collected_crystals = 0
            self.collected_energy = 0
        elif self.baseball_attempts >= self.max_attempts:
            self.state = "results"
    
    def update_time_travel(self):
        # Skip updates if game over
        if self.is_game_over:
            return
            
        # Collection mechanics
        ground_y = SCREEN_HEIGHT - 100
        
        if self.time_era == "past":
            # Check crystal collection
            crystal_positions = [300, 500, 800]
            for i, crystal_x in enumerate(crystal_positions):
                if i >= self.collected_crystals:  # Not yet collected
                    distance = abs(self.player_x - crystal_x)
                    if distance < 30:  # Close enough to collect
                        self.collected_crystals = i + 1
                        self.sound_manager.play_sound('collect_sound')
                        
                        # Check if all crystals collected
                        if self.collected_crystals >= 3:
                            self.player_won = True
                            self.win_start_time = pygame.time.get_ticks()
            
            # Check collision with dinosaur (only if player is on ground and hasn't won)
            dino_distance = abs(self.player_x - self.dinosaur_x)
            if dino_distance < 50 and not self.is_jumping and not self.player_won:  # Collision only on ground and if not won
                self.is_game_over = True
                self.game_over_time = pygame.time.get_ticks()
                self.sound_manager.play_sound('dinosaur_roar')
                self.sound_manager.play_sound('game_over_sound')
        
        elif self.time_era == "future":
            # Check energy orb collection
            orb_positions = [350, 550, 750]
            for i, orb_x in enumerate(orb_positions):
                if i >= self.collected_energy:  # Not yet collected
                    distance = abs(self.player_x - orb_x)
                    if distance < 30:  # Close enough to collect
                        self.collected_energy = i + 1
                        self.sound_manager.play_sound('collect_sound')
                        
                        # Check if all energy orbs collected
                        if self.collected_energy >= 3:
                            self.player_won = True
                            self.win_start_time = pygame.time.get_ticks()
            
            # Check collision with robot (only if player is on ground and hasn't won)
            robot_distance = abs(self.player_x - self.robot_x)
            if robot_distance < 50 and not self.is_jumping and not self.player_won:  # Collision only on ground and if not won
                self.is_game_over = True
                self.game_over_time = pygame.time.get_ticks()
                self.sound_manager.play_sound('robot_beep')
                self.sound_manager.play_sound('game_over_sound')
        
        # Enhanced AI movement for dinosaur and robot
        dt = 1.0 / 60.0  # Assume 60 FPS
        
        if self.time_era == "past" and self.dinosaur_movement_enabled:
            # Dinosaur AI - Aggressive predator that always chases player
            
            # Always move toward player - no stuck detection needed
            player_dist = abs(self.dinosaur_x - self.player_x)
            
            # Determine direction to player
            if self.player_x > self.dinosaur_x:
                target_direction = 1  # Move right
            elif self.player_x < self.dinosaur_x:
                target_direction = -1  # Move left
            else:
                target_direction = self.dinosaur_direction  # Keep current direction if same position
            
            # Set movement speed based on distance to player (reduced to 1/3 speed)
            if player_dist > 300:
                # Player is far - sprint to catch up
                move_speed = random.uniform(1.3, 2.0)  # Was 4.0-6.0
            elif player_dist > 100:
                # Player is medium distance - chase actively
                move_speed = random.uniform(1.0, 1.7)  # Was 3.0-5.0
            else:
                # Player is close - aggressive pursuit
                move_speed = random.uniform(0.8, 1.5)  # Was 2.5-4.5
            
            # Move dinosaur toward player
            self.dinosaur_x += target_direction * move_speed
            
            # Add aggressive hunting behavior - occasional quick lunges (reduced)
            if random.random() < 0.05:  # 5% chance for a lunge
                lunge_distance = random.uniform(7, 13)  # Was 20-40, now 1/3 speed
                self.dinosaur_x += target_direction * lunge_distance
            
            # Add some unpredictable movement (reduced)
            if random.random() < 0.1:  # 10% chance for random movement
                self.dinosaur_x += random.uniform(-3, 3)  # Was -10,10, now 1/3 speed
            
            # Keep dinosaur on screen but allow more aggressive edge behavior
            if self.dinosaur_x < 30:
                self.dinosaur_x = 35
            elif self.dinosaur_x > SCREEN_WIDTH - 30:
                self.dinosaur_x = SCREEN_WIDTH - 35
            
            # Update direction for next frame
            self.dinosaur_direction = target_direction
        
        elif self.time_era == "future" and self.robot_movement_enabled:
            # Robot AI - improved to avoid getting stuck
            orb_positions = [350, 550, 750]
            target_x = self.player_x  # Default target is player
            
            # Find closest uncollected orb
            closest_orb_dist = float('inf')
            closest_orb_x = None
            
            for i, orb_x in enumerate(orb_positions):
                if i >= self.collected_energy:  # Orb not collected
                    orb_dist = abs(self.robot_x - orb_x)
                    if orb_dist < closest_orb_dist:
                        closest_orb_dist = orb_dist
                        closest_orb_x = orb_x
            
            # Robot decision: intercept player near orbs or chase directly
            player_dist = abs(self.robot_x - self.player_x)
            if (closest_orb_x is not None and 
                abs(closest_orb_x - self.player_x) < 100 and  # Player near orb
                closest_orb_dist < 200):  # Robot can reach orb
                target_x = closest_orb_x  # Intercept at orb
            else:
                target_x = self.player_x  # Direct chase
            
            # Move robot toward target with improved logic
            distance_to_target = abs(target_x - self.robot_x)
            
            if distance_to_target > 3:  # Only move if not too close
                move_speed = random.uniform(2.0, 4.0)  # Increased and variable speed
                if target_x > self.robot_x:
                    self.robot_x += move_speed
                elif target_x < self.robot_x:
                    self.robot_x -= move_speed
            
            # Add systematic patrol behavior when far from target
            if distance_to_target > 200:
                patrol_movement = 10 * math.sin(pygame.time.get_ticks() * 0.01)
                self.robot_x += patrol_movement
            
            # Keep robot on screen
            self.robot_x = max(50, min(SCREEN_WIDTH - 50, self.robot_x))
        
        # Handle jumping physics with horizontal movement
        ground_level = SCREEN_HEIGHT - 120
        if self.is_jumping:
            # Apply gravity and update jump
            current_time = pygame.time.get_ticks()
            jump_duration = current_time - self.jump_start_time
            
            # Simple parabolic jump (peak at 0.3 seconds)
            if jump_duration < 600:  # 0.6 second jump duration
                t = jump_duration / 600.0  # Normalize to 0-1
                # Parabolic arc: height = 4 * jump_height * t * (1 - t)
                jump_height = 220  # Even higher jump (increased from 180)
                current_jump_offset = 4 * jump_height * t * (1 - t)
                self.player_y = ground_level - current_jump_offset
                
                # Horizontal movement during jump 
                jump_distance = 450  # 3x farther jump (150 * 3 = 450)
                
                # If player won, jump towards time machine, otherwise jump forward
                if self.player_won:
                    # Jump towards time machine (calculate distance and direction)
                    distance_to_machine = self.time_machine_x - self.jump_start_x
                    # Limit jump distance to not overshoot too much
                    clamped_distance = max(-jump_distance, min(jump_distance, distance_to_machine))
                    horizontal_progress = clamped_distance * t
                else:
                    # Normal forward jump
                    horizontal_progress = jump_distance * t
                    
                self.player_x = self.jump_start_x + horizontal_progress
                
                # Keep player on screen during jump
                self.player_x = max(50, min(SCREEN_WIDTH - 50, self.player_x))
            else:
                # Jump finished, return to ground
                self.is_jumping = False
                self.player_y = ground_level
        else:
            self.player_y = ground_level
    
    def restart_game(self):
        """Restart the entire game from the beginning"""
        # Reset to menu state
        self.state = "menu"
        
        # Reset rocket simulation variables
        self.rocket_sprite = None
        self.simulation = None
        self.sim_time = 0
        self.trajectory_points = []
        
        # Reset landing variables
        self.landing_position = None
        self.landing_time = 0
        self.show_landing_marker = False
        
        # Reset baseball game variables
        self.baseball_angle = 45
        self.baseball_power = 0.5
        self.baseball_attempts = 0
        self.rocket_tree_x = 0
        self.rocket_tree_height = 6
        self.baseball_player_x = 100
        
        # Reset time travel variables
        self.time_era = "present"
        self.time_power = 0.5
        self.collected_crystals = 0
        self.collected_energy = 0
        self.player_x = 200
        self.dinosaur_x = SCREEN_WIDTH - 200
        self.robot_x = SCREEN_WIDTH - 300
        self.dinosaur_direction = random.choice([-1, 1])
        self.dinosaur_stuck_counter = 0
        self.dinosaur_last_x = self.dinosaur_x
        self.is_game_over = False
        self.player_y = SCREEN_HEIGHT - 120
        self.is_jumping = False
        self.jump_velocity = 0
        self.jump_start_x = 0
        
        # Reset creature movement controls
        self.dinosaur_movement_enabled = False
        self.robot_movement_enabled = False
        
        # Reset win condition
        self.player_won = False
        self.win_start_time = 0
        
        # Reset sound flags
        self._launch_sound_played = False
        self._prev_countdown_second = 0
        
        # Randomize wind for new game
        self.wind_speed = random.uniform(0.5, 8.0)
        self.wind_direction = random.randint(0, 23) * 15
    
    def animate_rocket_falling(self):
        """Show rocket falling from tree after being hit"""
        start_time = pygame.time.get_ticks()
        ground_y = SCREEN_HEIGHT - 100
        tree_x = SCREEN_WIDTH // 2 + self.rocket_tree_x
        
        # Starting position in tree
        start_y = ground_y - self.rocket_tree_height * 13  # Match the visual height
        
        while pygame.time.get_ticks() - start_time < 1500:  # 1.5 second fall
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            
            # Draw background and trees (but not the stuck rocket)
            self.draw_background()
            
            # Draw trees with NO stuck rocket
            self.draw_tree(tree_x, ground_y)
            
            # Draw player at current position
            player_x = self.baseball_player_x
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
            elif self.state == "time_travel":
                self.update_time_travel()
                self.draw_time_travel_game()
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