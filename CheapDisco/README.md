# Cheap Disco for BombSquad

A dynamic lighting mod that transforms BombSquad's visuals with randomly changing dark color backgrounds in both main menu and gameplay.

## Description

Cheap Disco adds a vibrant, ever-changing color system to BombSquad that cycles through random dark colors in the background. This creates a disco-like atmosphere with moody, aesthetically pleasing color transitions that enhance the visual experience without being overwhelming.

## Features

- **Dynamic Color Cycling**: Background colors change automatically at customizable intervals
- **Dark Color Palette**: Uses carefully selected dark colors (0.0-0.5 range) for optimal visibility
- **Dual Mode Support**: Works in both main menu and in-game environments
- **Customizable Timing**: Adjust color change frequency from 0.1 to 60.0 seconds
- **Selective Activation**: Choose whether to enable effects in main menu, gameplay, or both
- **Configurable Settings**: Easy-to-use settings window with checkboxes and sliders
- **Language Support**: Includes special "Gibberish" language mode with fun alternative text
- **Non-Intrusive**: Doesn't affect gameplay mechanics or performance

## Installation

1. Download the `CheapDisco.py` file
2. Place it in your BombSquad mods folder
3. Ensure you have API version 9 or compatible version of BombSquad

## Usage

### Automatic Usage
1. Launch BombSquad with the mod installed
2. The disco effects will start automatically based on your settings
3. Colors will cycle in the background while you play or browse menus

### Configuration
1. Access the settings through the mods menu or settings interface
2. Open the "Disco Settings" window
3. Adjust the following options:
   - **Disco in Mainmenu**: Toggle effects in the main menu
   - **Disco in GamePlay**: Toggle effects during actual gameplay
   - **Disco Color Time**: Set how frequently colors change (0.1-60.0 seconds)

## Settings Details

### Mainmenu vs GamePlay
- **Mainmenu Mode**: Affects only the main menu and lobby screens
- **GamePlay Mode**: Affects only during active gameplay sessions
- **Both**: Enjoy colorful backgrounds everywhere in the game

### Color Timing
- **Fast Changes** (0.1-1.0s): Creates a rapid, energetic disco effect
- **Medium Changes** (1.0-5.0s): Balanced pacing for most users
- **Slow Changes** (5.0-60.0s): Subtle, gradual color shifts for a calm atmosphere

### Color Range
The mod uses a carefully calibrated dark color range:
- Red: 0.0 - 0.5
- Green: 0.0 - 0.5  
- Blue: 0.0 - 0.5
This ensures text and UI elements remain readable while providing visual interest.

## Requirements

- BombSquad version with API 9 support
- Python modding environment setup

## Technical Details

This mod implements a sophisticated color management system:

- **Global Node Manipulation**: Modifies the `globalsnode.tint` property for global color effects
- **Activity Detection**: Automatically detects whether you're in main menu or gameplay
- **Configuration Persistence**: Saves settings to BombSquad's config system
- **Custom UI Elements**: Implements modified ConfigNumberEdit for timing control
- **Efficient Timers**: Uses ba.AppTimer for precise, performance-friendly color changes

## Visual Effects

The mod creates:
- Smooth color transitions between random dark hues
- Atmospheric background lighting that complements game visuals
- Non-distracting color schemes that maintain gameplay clarity
- Consistent visual experience across different game modes

## Compatibility

- Works with most other visual and UI mods
- Compatible with all game modes and maps
- No conflicts with character mods or custom content
- Settings persist between game sessions

## Performance

- Minimal performance impact due to efficient timer system
- Only modifies global tint property, not individual objects
- Automatic cleanup when mod is disabled
- No additional textures or meshes loaded

## Customization Tips

### For Party Atmosphere:
- Set timer to 0.5 seconds
- Enable both main menu and gameplay modes

### For Subtle Ambiance:
- Set timer to 10.0+ seconds  
- Use only in main menu for lobby atmosphere

### For Thematic Gameplay:
- Enable only during gameplay for match-specific moods
- Combine with night maps for enhanced atmosphere

## Screenshots

<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/d7ffaf07-78bd-4611-9fc0-63284ab238a2" />

## Video

https://github.com/user-attachments/assets/3a73f069-251a-4a97-84ea-fc6750992346

## Credits

Created by the [BombSquad modding community](https://github.com/bombsquad-community)  
Forked by [Less](https://github.com/danigomezdev)
