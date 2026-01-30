# Hidden Features For Developers Of SkyscraperLIVE
This document outlines some hidden features in SkyscraperLIVE that are primarily intended for developers and testers. These features can help in testing various aspects of the game without going through the normal gameplay mechanics.

## 1. Time Warp Toggle
Press `Ctrl + T` to toggle time warp mode. When enabled, this allows the simulation time to progress faster, useful for testing long climbs quickly.
### Controls
- **`Ctrl + T`**: Toggle time warp mode
- **`.`**: Increase time warp speed
- **`,`**: Decrease time warp speed
### Implementation
In `main.py`, the time warp functionality is controlled by the `allow_timewarp` boolean variable. When enabled, the time increment per frame is multiplied by the `timewarp` factor.

## 2. Spectator Mode
Press `Ctrl + S` to toggle spectator mode. In this mode, the player can freely move around the building without climbing constraints, useful for inspecting the building model.
### Controls
- **`Ctrl + S`**: Toggle spectator mode
- **`Arrow Up/Down/Left/Right`**: Move in respective directions
- No other key controls affect movement
### Implementation
In `main.py`, the spectator mode is controlled by the `spectator_mode` boolean variable. When enabled, the `move_simple()` function is called instead of the climbing logic(`move()` function), allowing free movement.
