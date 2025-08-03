import numpy as np
import matplotlib.pyplot as plt
import random
import math

class RocketEngine:
    def __init__(self, name, total_impulse, average_thrust, burn_time, delay):
        self.name = name
        self.total_impulse = total_impulse  # Newton-seconds
        self.average_thrust = average_thrust  # Newtons
        self.burn_time = burn_time  # seconds
        self.delay = delay  # seconds

class Rocket:
    def __init__(self, mass=0.034, diameter=0.0248, length=0.311, cd=0.3):
        self.dry_mass = mass  # kg (34g converted)
        self.diameter = diameter  # meters (24.8mm converted)
        self.length = length  # meters (31.1cm converted)
        self.cd = cd  # drag coefficient (estimated for model rocket)
        self.area = math.pi * (diameter/2)**2  # cross-sectional area
        
        # State variables
        self.position = np.array([0.0, 0.0])  # [x, y] in meters
        self.velocity = np.array([0.0, 0.0])  # [vx, vy] in m/s
        self.mass = mass
        self.parachute_deployed = False
        self.engine_burning = False
        self.flight_phase = "launch"  # launch, coast, descent

# Engine specifications based on research
ENGINES = {
    'A': RocketEngine('A8-3', 2.5, 8.0, 0.3125, 3.0),
    'B': RocketEngine('B6-4', 5.0, 6.0, 0.833, 4.0), 
    'C': RocketEngine('C6-5', 10.0, 6.0, 1.667, 5.0)
}

class RocketSimulation:
    def __init__(self, engine_type='B', wind_speed=0, wind_direction=0):
        self.rocket = Rocket()
        self.engine = ENGINES[engine_type]
        self.wind_speed = wind_speed  # m/s
        self.wind_direction = wind_direction  # degrees (0 = east, 90 = north)
        self.wind_vector = np.array([
            wind_speed * math.cos(math.radians(wind_direction)),
            wind_speed * math.sin(math.radians(wind_direction))
        ])
        
        # Environment constants
        self.g = 9.81  # gravity m/s^2
        self.air_density = 1.225  # kg/m^3 at sea level
        self.dt = 0.01  # time step in seconds
        
        # Football field dimensions (120 yards x 53 yards including end zones)
        self.field_length = 109.7  # meters
        self.field_width = 48.8  # meters
        self.tree_height = 10.0  # meters (estimated)
        
        # Simulation data
        self.time_history = []
        self.position_history = []
        self.velocity_history = []
        
    def drag_force(self, velocity):
        """Calculate drag force based on velocity"""
        relative_velocity = velocity - self.wind_vector
        speed = np.linalg.norm(relative_velocity)
        if speed == 0:
            return np.array([0.0, 0.0])
        
        # Parachute has almost no effect - rocket falls nearly at free fall speed
        cd = self.rocket.cd if self.rocket.parachute_deployed else self.rocket.cd  # Same drag as rocket
        area = self.rocket.area if self.rocket.parachute_deployed else self.rocket.area  # Same area as rocket
        
        drag_magnitude = 0.5 * self.air_density * cd * area * speed**2
        drag_direction = -relative_velocity / speed
        return drag_magnitude * drag_direction
    
    def thrust_force(self, time):
        """Calculate thrust force during engine burn"""
        if time <= self.engine.burn_time:
            return np.array([0.0, self.engine.average_thrust])
        return np.array([0.0, 0.0])
    
    def simulate_flight(self):
        """Run the complete flight simulation"""
        time = 0.0
        self.rocket.position = np.array([self.field_length/2, 0.0])  # Start at center of field
        self.rocket.velocity = np.array([0.0, 0.0])
        self.rocket.mass = self.rocket.dry_mass + 0.012  # Add propellant mass (estimated)
        
        # Clear history
        self.time_history = []
        self.position_history = []
        self.velocity_history = []
        
        max_altitude = 0
        apogee_time = 0
        
        while True:
            # Record current state
            self.time_history.append(time)
            self.position_history.append(self.rocket.position.copy())
            self.velocity_history.append(self.rocket.velocity.copy())
            
            # Track maximum altitude
            if self.rocket.position[1] > max_altitude:
                max_altitude = self.rocket.position[1]
                apogee_time = time
            
            # Check for parachute deployment (at apogee + delay)
            if (not self.rocket.parachute_deployed and 
                time > self.engine.burn_time + self.engine.delay and
                self.rocket.velocity[1] <= 0):
                self.rocket.parachute_deployed = True
                self.rocket.flight_phase = "descent"
            
            # Calculate forces
            thrust = self.thrust_force(time)
            drag = self.drag_force(self.rocket.velocity)
            gravity = np.array([0.0, -self.rocket.mass * self.g])
            
            # Total force and acceleration
            total_force = thrust + drag + gravity
            acceleration = total_force / self.rocket.mass
            
            # Update velocity and position (Euler integration)
            self.rocket.velocity += acceleration * self.dt
            self.rocket.position += self.rocket.velocity * self.dt
            
            # Check for ground impact
            if self.rocket.position[1] <= 0:
                break
                
            time += self.dt
            
            # Safety check for runaway simulation
            if time > 300:  # 5 minutes max
                break
        
        return max_altitude, self.check_landing_location()
    
    def check_landing_location(self):
        """Determine if rocket landed on field or in trees"""
        final_x = self.rocket.position[0]
        
        # Check if within field boundaries
        if 0 <= final_x <= self.field_length:
            return "field"
        else:
            return "trees"
    
    def plot_trajectory(self):
        """Plot the rocket trajectory"""
        positions = np.array(self.position_history)
        
        plt.figure(figsize=(12, 8))
        plt.plot(positions[:, 0], positions[:, 1], 'b-', linewidth=2, label='Trajectory')
        
        # Mark launch and landing points
        plt.plot(positions[0, 0], positions[0, 1], 'go', markersize=10, label='Launch')
        plt.plot(positions[-1, 0], positions[-1, 1], 'ro', markersize=10, label='Landing')
        
        # Draw field boundaries
        field_x = [0, self.field_length, self.field_length, 0, 0]
        field_y = [0, 0, 0, 0, 0]
        plt.fill([0, self.field_length, self.field_length, 0], 
                 [0, 0, 0, 0], 'lightgreen', alpha=0.3, label='Football Field')
        
        # Draw tree areas
        plt.fill([-50, 0, 0, -50], [0, 0, self.tree_height, self.tree_height], 
                 'darkgreen', alpha=0.5, label='Trees')
        plt.fill([self.field_length, self.field_length+50, self.field_length+50, self.field_length], 
                 [0, 0, self.tree_height, self.tree_height], 
                 'darkgreen', alpha=0.5)
        
        plt.xlabel('Horizontal Distance (m)')
        plt.ylabel('Altitude (m)')
        plt.title(f'Rocket Trajectory - Engine: {self.engine.name}, Wind: {self.wind_speed} m/s')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.axis('equal')
        plt.show()

def run_simulation(engine_type='B', wind_speed=2, wind_direction=270, show_plot=True):
    """Run a single simulation"""
    sim = RocketSimulation(engine_type, wind_speed, wind_direction)
    max_altitude, landing = sim.simulate_flight()
    
    print(f"Engine: {engine_type}")
    print(f"Max Altitude: {max_altitude:.1f} m ({max_altitude*3.28:.0f} ft)")
    print(f"Landing Location: {landing}")
    print(f"Final Position: x={sim.rocket.position[0]:.1f}m")
    
    if show_plot:
        sim.plot_trajectory()
    
    return max_altitude, landing, sim.rocket.position[0]

def run_multiple_simulations(engine_type='B', num_runs=100):
    """Run multiple simulations with random wind conditions"""
    results = {"field": 0, "trees": 0}
    altitudes = []
    
    for i in range(num_runs):
        # Random wind conditions
        wind_speed = random.uniform(0, 8)  # 0-8 m/s wind
        wind_direction = random.uniform(0, 360)  # random direction
        
        sim = RocketSimulation(engine_type, wind_speed, wind_direction)
        altitude, landing = sim.simulate_flight()
        
        results[landing] += 1
        altitudes.append(altitude)
    
    print(f"\n=== Results for {num_runs} flights with Engine {engine_type} ===")
    print(f"Landed on field: {results['field']} ({results['field']/num_runs*100:.1f}%)")
    print(f"Stuck in trees: {results['trees']} ({results['trees']/num_runs*100:.1f}%)")
    print(f"Average altitude: {np.mean(altitudes):.1f}m ({np.mean(altitudes)*3.28:.0f}ft)")
    print(f"Max altitude: {np.max(altitudes):.1f}m ({np.max(altitudes)*3.28:.0f}ft)")
    
    return results

if __name__ == "__main__":
    # Run single simulation
    print("Single Flight Simulation:")
    run_simulation('C', wind_speed=3, wind_direction=270)
    
    # Run multiple simulations for each engine type
    for engine in ['A', 'B', 'C']:
        run_multiple_simulations(engine, 50)