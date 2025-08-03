import numpy as np
import matplotlib.pyplot as plt
import random
import math
from rocket_simulation import RocketSimulation, ENGINES

def auto_flight_demo():
    """Run an automatic flight demonstration"""
    print("\n" + "="*50)
    print("🚀 ESTES ALPHA III AUTO FLIGHT DEMO 🚀")
    print("="*50)
    
    # Simulate choosing engine C for maximum excitement
    engine_choice = 'C'
    print(f"\nEngine Selected: {engine_choice} - High Power (~1200 ft)")
    
    # Generate random weather
    wind_speed = random.uniform(2, 5)
    wind_direction = random.uniform(0, 360)
    
    print(f"Weather Conditions:")
    print(f"Wind: {wind_speed:.1f} m/s from {wind_direction:.0f}°")
    
    # Run simulation
    print(f"\n🚀 LAUNCHING...")
    sim = RocketSimulation(engine_choice, wind_speed, wind_direction)
    max_altitude, landing = sim.simulate_flight()
    
    print(f"\n🚀 FLIGHT RESULTS:")
    print(f"Max Altitude: {max_altitude:.1f}m ({max_altitude*3.28:.0f}ft)")
    print(f"Landing Location: {landing}")
    print(f"Final Position: {sim.rocket.position[0]:.1f}m from launch point")
    
    # Show trajectory
    print(f"\n📊 Generating trajectory plot...")
    sim.plot_trajectory()
    
    if landing == "trees":
        print(f"\n⚠️ ROCKET STUCK IN TREES!")
        auto_baseball_recovery(sim.rocket.position)
    else:
        print(f"\n✅ SAFE LANDING ON FIELD!")
        print(f"🎉 Mission Success! Rocket recovered safely.")

def auto_baseball_recovery(rocket_position):
    """Automatic baseball recovery simulation"""
    print(f"\n🥎 BASEBALL RECOVERY SIMULATION")
    print(f"Rocket stuck {abs(rocket_position[0]):.1f}m away!")
    
    # Simulate a few throws
    attempts = 0
    max_attempts = 5
    
    while attempts < max_attempts:
        attempts += 1
        
        # Generate random throw parameters
        angle = random.uniform(20, 60)  # degrees
        power = random.uniform(0.4, 0.9)  # power level
        
        print(f"\nAttempt {attempts}: Angle={angle:.1f}°, Power={power:.2f}")
        
        # Simple success calculation based on reasonable parameters
        distance_accuracy = 1 - abs(power * 20 * math.cos(math.radians(angle)) - abs(rocket_position[0])) / 20
        height_accuracy = 1 - abs(power * 20 * math.sin(math.radians(angle)) - 6) / 10
        
        success_chance = max(0, (distance_accuracy + height_accuracy) / 2)
        
        if random.random() < success_chance or attempts == max_attempts:
            if attempts < max_attempts:
                print(f"🎯 HIT! Rocket knocked down!")
                print(f"🎉 Rocket recovered after {attempts} attempts!")
            else:
                print(f"🎯 Final throw... HIT! Lucky shot!")
                print(f"🎉 Rocket recovered on last attempt!")
            return True
        else:
            miss_reasons = ["Too short!", "Overshot!", "Too high!", "Close miss!"]
            print(f"❌ {random.choice(miss_reasons)}")
    
    print(f"💥 Out of baseballs! Rocket remains stuck.")
    return False

def run_multiple_auto_flights(num_flights=3):
    """Run multiple automatic flights"""
    print(f"\n🎮 RUNNING {num_flights} AUTO FLIGHTS")
    print("="*50)
    
    total_score = 0
    engines = ['A', 'B', 'C']
    
    for flight_num in range(1, num_flights + 1):
        print(f"\n--- AUTO FLIGHT {flight_num}/{num_flights} ---")
        
        # Rotate through engines
        engine = engines[(flight_num - 1) % 3]
        
        # Random weather
        wind_speed = random.uniform(1, 6)
        wind_direction = random.uniform(0, 360)
        
        print(f"Engine: {engine}, Wind: {wind_speed:.1f} m/s")
        
        # Simulate flight
        sim = RocketSimulation(engine, wind_speed, wind_direction)
        altitude, landing = sim.simulate_flight()
        
        print(f"Altitude: {altitude:.0f}m ({altitude*3.28:.0f}ft), Landing: {landing}")
        
        # Score calculation
        if landing == "field":
            points = {'A': 10, 'B': 15, 'C': 20}[engine]
            total_score += points
            print(f"✅ Safe landing! +{points} points")
        else:
            print(f"⚠️ Tree landing - attempting recovery...")
            if random.random() > 0.4:  # 60% recovery success
                total_score += 5
                print(f"🥎 Recovered! +5 points")
            else:
                print(f"❌ Lost rocket!")
    
    print(f"\n🏆 FINAL SCORE: {total_score} points")
    
    if total_score >= 50:
        print("🥇 Ace Rocketeer!")
    elif total_score >= 30:
        print("🥈 Skilled Pilot!")
    else:
        print("🥉 Keep Practicing!")

if __name__ == "__main__":
    print("🚀 AUTOMATIC ROCKET GAME DEMO")
    print("Choose demo type:")
    print("1. Single Flight Demo")
    print("2. Multiple Flight Demo")
    
    # Auto-select single flight for demo
    choice = "1"
    print(f"Auto-selecting: {choice}")
    
    if choice == "1":
        auto_flight_demo()
    else:
        run_multiple_auto_flights(3)
    
    print(f"\n🎮 For interactive mode, you would run the original game!")
    print("This demo shows what the full interactive experience would be like.")