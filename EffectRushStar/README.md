# Effect Rush Star for BombSquad

A stunning visual effects mod that creates animated floating stars with dynamic colors and text that move around the game map.

## Description

Effect Rush Star adds beautiful, animated visual elements to BombSquad games. Two glowing stars with colorful particle effects and animated text float gracefully around the map, creating a mesmerizing visual experience that enhances the game's atmosphere without affecting gameplay.

## Features

- **Dual Animated Stars**: Two independent stars with unique movement patterns
- **Dynamic Color Cycling**: Continuous color transitions through rainbow spectrums
- **Particle Effects**: Glowing shield effects with flash attachments
- **Animated Text Display**: Floating text with synchronized color animations
- **Smooth Movement Paths**: Predefined flight patterns that cover the entire map
- **Non-Intrusive Design**: Pure visual enhancement that doesn't interfere with gameplay
- **Automatic Activation**: Works in all game modes except main menu

## Installation

1. Download the `effectRushStar.py` file
2. Place it in your BombSquad mods folder
3. Ensure you have API version 9 or compatible version of BombSquad

## Usage

1. Launch BombSquad with the mod installed
2. Start any game mode (except main menu)
3. The effect stars will automatically appear and begin their animation cycle
4. Watch as they float around the map with changing colors and effects

## Visual Elements

### Star 1:
- **Movement Path**: Travels from (-10,3,-5) to (10,6,-5) to (-10,3,5) in a 20-second loop
- **Color Cycle**: Random colors transitioning through purple, yellow, green, and light blue
- **Text**: Displays animated text with rainbow color cycle

### Star 2:
- **Movement Path**: Opposite path to Star 1, creating complementary movement
- **Color Cycle**: Different color sequence including teal, purple, yellow, and green
- **Text**: Same text but with reverse color animation

## Requirements

- BombSquad version with API 9 support
- Python modding environment setup

## Technical Details

This mod extends the Map class initialization to add visual effects:

- **Shield Nodes**: Creates glowing spherical shields as the base stars
- **Flash Effects**: Adds particle flash effects attached to each star
- **Text Nodes**: Displays animated text above each star
- **Math Nodes**: Handles positional calculations for text placement
- **Animation System**: Uses bs.animate_array for smooth color and position transitions
- **Timer System**: Delays effect creation to ensure proper game initialization

## Customization

You can easily modify the following constants in the code:

- `TEXT_CONTENT`: Change the displayed text
- `TEXT_SIZE`: Adjust text scale
- `TEXT_COLOR`: Set initial text color
- Movement paths and timing in the animation dictionaries
- Color sequences in the color animation dictionaries

## Compatibility

- Works with all game modes except main menu
- Compatible with most other visual and gameplay mods
- No conflicts with game mechanics or physics
- Performance-friendly design

## Screenshots

<img width="341" height="192" alt="Image" src="https://github.com/user-attachments/assets/694f7387-6024-4e5a-924a-baae0f4e5e85" />

## Video

https://github.com/user-attachments/assets/94df65fa-a865-40ac-82cc-d54c67129736

## Credits

Originally created by Taha_OstadSharif  
Forked by [Less](https://github.com/danigomezdev)
