# Hidden Features for Developers of SkyscraperLIVE

> ⚠ **Debug Only / Cheat Features**  
>  
> The features described in this document are **intended strictly for developers and testers**.  
> They bypass normal gameplay mechanics and **should not be enabled in production or release builds**.

This document outlines several hidden features in **SkyscraperLIVE** that are primarily intended for debugging, testing, and development purposes. These features allow rapid testing and inspection without relying on standard gameplay flow.

---

## 1. Time Warp Toggle

Press `Ctrl + T` to toggle **Time Warp Mode**. When enabled, the simulation time progresses faster, allowing developers to quickly test long climbs or time-dependent mechanics.

### Controls
- **`Ctrl + T`**: Toggle Time Warp Mode  
- **`.`**: Increase time warp speed  
- **`,`**: Decrease time warp speed  

### Behavior Notes
- Skips real-time progression
- May cause physics or animation desynchronization
- Not suitable for gameplay balance testing

### Implementation
In `main.py`, the time warp functionality is controlled by the `allow_timewarp` boolean variable.  
When enabled, the time increment per frame is multiplied by the `timewarp` factor.

---

## 2. Spectator Mode

Press `Ctrl + S` to toggle **Spectator Mode**. This mode removes all climbing constraints and allows free camera movement, making it useful for inspecting level geometry and building models.

### Controls
- **`Ctrl + S`**: Toggle Spectator Mode  
- **Arrow Keys (`Up / Down / Left / Right`)**: Move in the corresponding directions  
- **`+ / -`**: Zoom in / out  
- All other key inputs are ignored for movement  
- Cannot increase / decrease time warp speed in this mode

### Behavior Notes
- Player collision and climbing logic are bypassed
- Intended for visual inspection and layout verification
- Not compatible with normal gameplay flow

### Implementation
In `main.py`, Spectator Mode is controlled by the `spectator_mode` boolean variable.  
When enabled, the `move_simple()` function is used instead of the standard climbing logic (`move()`), allowing unrestricted movement.

---

## ⚠ Important Notes

- These features are **cheats by design**
- Must be disabled or stripped from release builds
- Recommended to guard with:
  - `DEBUG` flags
  - developer-only configuration
  - or build-time conditions
