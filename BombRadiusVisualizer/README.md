# Bomb Radius Visualizer for BombSquad

A mod that displays dynamic visual indicators showing the blast radius of all explosives in BombSquad with colorful animations.

## Description

Bomb Radius Visualizer adds vibrant, animated visual indicators to all bombs and explosives in the game. This enhanced version not only shows the exact blast radius but also features dynamic color-changing effects that cycle through random colors, creating a visually striking experience while maintaining strategic utility.

## Features

- **Dynamic Color System**: Bomb indicators cycle through random colors every 0.5 seconds
- **Animated Radius Indicators**: Smooth animations showing the blast radius growing into place
- **Dual Visual System**: 
  - Opaque circle showing the damaging area (starts blue)
  - Outline circle marking the exact blast radius (starts white)
- **Real-time Visualization**: Indicators appear immediately when bombs are created
- **Automatic Cleanup**: Visuals automatically disappear when bombs explode or are destroyed
- **Compatible with All Explosives**: Works with regular bombs, sticky bombs, landmines, and more
- **Rainbow Effects**: Continuously changing colors create a festive, dynamic appearance

## Installation

1. Download the `bombRadiusVisualizer.py` file
2. Place it in your BombSquad mods folder
3. Ensure you have API version 9 or compatible version of BombSquad

## Usage

1. Launch BombSquad with the mod installed
2. Join any game mode that includes explosives
3. Whenever any player throws or places a bomb, you'll see:
   - A growing circle showing the damaging area (initially blue)
   - An outline showing the exact blast radius (initially white)
   - Both elements will cycle through random colors every 0.5 seconds
4. The visuals automatically follow the bomb until it explodes

## Requirements

- BombSquad version with API 9 support
- Python modding environment setup

## Technical Details

This mod extends the existing Bomb class with enhanced visual features:
- Modifies `bascenev1lib.actor.bomb.Bomb.__init__` method
- Adds two locator nodes for visualization:
  - Circle shape for damage area (semi-transparent)
  - CircleOutline shape for blast radius (additive)
- Global timer system changes colors every 0.5 seconds
- Uses smooth animations for visual appeal
- Properly handles node ownership and cleanup
- Maintains a global list of active bombs for color management

## Visual Examples

The mod creates two dynamic visual elements for each bomb:

1. **Damage Area Circle**: A semi-transparent circle that grows to show the area affected by the explosion, with colors that cycle randomly
2. **Blast Radius Outline**: An outline that appears around the exact blast radius, with independently cycling colors

These visuals help players:
- Judge safe distances from explosives with enhanced visibility
- Plan strategic throws and placements
- Understand explosive mechanics better
- Enjoy colorful, dynamic visual effects

## Compatibility

- Works with most other mods due to careful function wrapping
- Compatible with all game modes
- No known conflicts with other visual or gameplay mods

## Screenshots

<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/335a3b1e-b01c-41a7-9c27-418f6fe16912" />
<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/5f026773-f2fd-4607-ac5f-57a7666bce54" />
<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/952e6ee6-3b92-4340-8e7f-ea4ea48ed1b4" />

## Video

https://github.com/user-attachments/assets/bfeae51c-d86b-4c35-9247-53e0d50e5b39

## Credits

Created by the [BombSquad modding community](https://github.com/bombsquad-community)  
Forked by [Less](https://github.com/danigomezdev)
