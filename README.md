# 🚀 Estes Alpha III Rocket Simulation Game

A realistic model rocket launch simulation and game featuring accurate physics, spectacular visual effects, and interactive gameplay.

![Rocket Game](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.6+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Features

- **Realistic Physics**: Accurate Estes Alpha III rocket specifications with proper thrust, drag, and mass calculations
- **Three Engine Types**: A8-3 (~600ft), B6-4 (~900ft), and C6-5 (~1200ft) with realistic performance
- **Dynamic Weather**: Adjustable wind speed and direction affecting rocket trajectory
- **Visual Effects**: 
  - 6-second countdown with rainbow "BLAST OFF!" animation
  - White smoke and red flame exhaust particles
  - Real-time trajectory tracking
  - Parachute deployment visualization
- **Interactive Gameplay**:
  - Football field launch environment with surrounding trees
  - Tree-height landing detection (rocket stops at branch level)
  - Baseball recovery mini-game for rockets stuck in trees
  - Hit detection with visual effects and falling animations

## 🎮 Controls

### Main Menu
- **A/B/C** - Select engine type
- **Arrow Keys** - Adjust wind conditions
  - **UP/DOWN** - Wind speed (0-10 m/s)
  - **LEFT/RIGHT** - Wind direction (15° increments)
- **SPACEBAR** - Launch rocket
- **ESC/Q** - Quit game

### Baseball Recovery (when rocket lands in trees)
- **UP/DOWN** - Adjust throw angle (0-90°)
- **LEFT/RIGHT** - Adjust throw power (0.1-1.0)
- **SPACEBAR** - Throw baseball
- **Goal**: Hit the rocket to knock it down (10 attempts max)

## 🛠️ Installation

### Prerequisites
- Python 3.9 or higher
- pygame 2.6 or higher
- numpy

### Install Dependencies
```bash
pip install pygame numpy
```

### Clone and Run
```bash
git clone https://github.com/jmfoster/rocket-game.git
cd rocket-game
python3 rocket_game_v1.0.py
```

## 🚀 How to Play

1. **Select Your Engine**: Choose A, B, or C engine based on desired altitude
2. **Set Weather Conditions**: Adjust wind speed and direction using arrow keys
3. **Launch**: Press SPACEBAR to start the 6-second countdown
4. **Watch the Flight**: Observe realistic rocket physics with:
   - Powered ascent phase with exhaust effects
   - Coasting phase to apogee
   - Parachute deployment
   - Wind-affected descent
5. **Recovery**: 
   - **Field Landing**: Mission success! Press SPACE for new flight
   - **Tree Landing**: Play baseball mini-game to recover rocket

## 📊 Technical Details

### Engine Specifications
| Engine | Total Impulse | Avg Thrust | Burn Time | Delay | Expected Altitude |
|--------|---------------|------------|-----------|-------|-------------------|
| A8-3   | 2.5 N⋅s      | 8.0 N      | 0.31 s    | 3 s   | ~600 ft          |
| B6-4   | 5.0 N⋅s      | 6.0 N      | 0.83 s    | 4 s   | ~900 ft          |
| C6-5   | 10.0 N⋅s     | 6.0 N      | 1.67 s    | 5 s   | ~1200 ft         |

### Physics Model
- **Rocket Mass**: 34g (Estes Alpha III specifications)
- **Drag Coefficient**: 0.3 (typical for model rockets)
- **Parachute Deployment**: At apogee + engine delay
- **Wind Effects**: Horizontal drift during parachute descent
- **Landing Detection**: Ground level (0m) or tree height (6m)

## 🗂️ File Structure

```
rocket-game/
├── README.md                    # This file
├── rocket_game_v1.0.py         # Main game file (complete version)
├── rocket_simulation.py        # Physics engine and simulation
├── auto_rocket_game.py         # Automatic demo version
└── .gitignore                  # Python gitignore
```

## 🎯 Game Modes

### 1. Interactive Mode
- Full pygame GUI with visual effects
- Real-time flight simulation
- Interactive recovery mini-game

### 2. Auto Demo Mode
```bash
python3 auto_rocket_game.py
```
- Automated flight demonstrations
- Physics simulation without GUI
- Perfect for headless environments

## 🏆 Scoring & Statistics

- **Field Landing**: Mission success! (Points: A=10, B=15, C=20)
- **Tree Recovery**: Baseball mini-game challenge (+5 points if successful)
- **Wind Challenge**: Higher wind speeds increase difficulty
- **Engine Strategy**: Higher power = higher altitude but more tree risk

## 🤝 Contributing

This project was created as a realistic model rocket simulation. Feel free to:
- Report bugs or issues
- Suggest new features
- Improve physics accuracy
- Add new rocket models

## 📝 License

MIT License - Feel free to use, modify, and distribute.

## 🙏 Acknowledgments

- **Estes Rockets** for Alpha III specifications
- **Real model rocket physics** research and data
- **Pygame community** for excellent game development framework

---

**Ready for launch? Fire up the game and experience the thrill of model rocketry!** 🚀

*Generated with [Claude Code](https://claude.ai/code)*