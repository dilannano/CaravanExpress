# Police Chase - Escape in Your Minivan!

A unique police chase endless runner game built with Python and Pygame. Drive your 2009 Dodge Caravan through traffic while evading the cops!

## 🚨 Game Story

You're driving your trusty white Dodge Caravan when suddenly the police are on your tail! Navigate through three lanes of traffic, avoid obstacles, and don't get caught. Every mistake brings the police closer - hit too many obstacles and you're BUSTED!

## Features

- **Unique Police Chase Mechanic**: Police chase you from behind - hit obstacles and they get closer!
- **Dynamic Difficulty**: The closer the police get, the more intense the game becomes
- **Realistic Obstacles**: 
  - Red traffic lights (running a red light!)
  - Stop signs (failure to stop!)
  - Police roadblocks
- **Money Bag Collectibles**: Grab cash bags to speed away from the cops
- **Progressive Speed**: Game gets faster as you travel further
- **警告 Warning System**: Visual warnings when police are dangerously close
- **Score System**: Points for distance, obstacles avoided, and money collected

## Controls

- **Arrow Keys (Left/Right)**: Move between lanes
- **Space Bar / Up Arrow**: Jump
- **Down Arrow**: Slide
- **Space Bar (Game Over)**: Restart game

## Installation

1. Make sure you have Python 3.7+ installed
2. Install Pygame:
```bash
pip install pygame
```

## How to Run

```bash
python main.py
```

## Game Mechanics

- **Police Distance System**: 
  - Start with police 300m behind you
  - Successfully dodge obstacles: Police get +15m further away
  - Hit an obstacle: Police get -80m closer
  - Collect money: Police get +25m further away (speed boost!)
  - Police slowly gain on you over time
  - If police get within 50m and you hit an obstacle: **GAME OVER**
  
- **Score**: 
  - +10 points for each obstacle passed
  - +50 points for each money bag collected
  
- **Speed**: Increases every 1000 distance units

- **警告 Warnings**:
  - GREEN (200m+): You're safe, keep going!
  - ORANGE (100-200m): Police are getting closer!
  - RED (<100m): DANGER! One more mistake and you're caught!

## Project Structure

```
subway_runner/
├── main.py           # Main game loop and chase mechanics
├── player.py         # 2009 Dodge Caravan (white minivan)
├── police.py         # Police car chaser with flashing sirens
├── obstacle.py       # Traffic lights, stop signs, roadblocks
├── collectible.py    # Money bags
├── background.py     # Highway/road rendering
└── README.md         # This file
```

## Portfolio Highlights

This project demonstrates:
- Creative game design with unique chase mechanics
- Object-oriented programming in Python
- Dynamic difficulty system (police distance)
- Collision detection and game state management
- Visual feedback systems (color-coded warnings)
- Smooth animations and police siren effects
- Clean, modular code structure
- Original twist on the endless runner genre

## Future Enhancements

Potential features to add:
- Multiple police cars as you progress
- Power-ups (turbo boost, shield, decoy)
- Different vehicle choices
- Sound effects (sirens, engine, crashes)
- Different road environments (city, highway, rural)
- Multiplayer mode
- Police helicopter that appears at high scores
- Day/night cycle

## License

Free to use for educational and portfolio purposes.

## Author

Created as a portfolio project showcasing game development skills with Python and Pygame.
