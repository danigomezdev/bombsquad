# Character Maker for BombSquad

A comprehensive mod that allows you to create custom characters by mixing and matching parts from existing characters in the game.

## Description

Character Maker transforms BombSquad into a powerful character creation studio. This mod provides a fully-featured game mode where players can design their own unique characters by combining different body parts, textures, colors, and styles from all available characters in the game.

## Features

- **Complete Character Customization**: Mix and match heads, torsos, limbs, and more from different characters
- **Real-time 3D Preview**: See your character come to life immediately as you make changes
- **Color Customization**: Choose from preset colors or create your own color combinations
- **Texture Swapping**: Apply different texture sets to your custom character
- **Export/Import System**: Save your creations as JSON files and share them with others
- **Multiplayer Support**: Multiple players can create characters simultaneously
- **Chat Commands**: Use in-game commands to manage your character creations
- **Preset Library**: Access to all default character parts and textures

## Installation

1. Download the `characterMaker.py` file
2. Place it in your BombSquad mods folder
3. Ensure you have API version 9 or compatible version of BombSquad

## Usage

### Starting the Character Maker
1. Launch BombSquad with the mod installed
2. Create or join a game using the "Character Maker" game type
3. Use the on-screen controls to navigate the creation interface

### Controls
- **Jump Button**: Cycle through character components (head, torso, arms, etc.)
- **Pick Up Button**: Cycle backwards through components
- **Punch Button**: Cycle through available models/textures for selected component
- **Bomb Button**: Cycle backwards through models/textures

### Chat Commands
- `/info` - Display current character configuration
- `/export <character-name>` - Save your current character as a JSON file
- `/import <character-name>` - Load a previously saved character

## Requirements

- BombSquad version with API 9 support
- Python modding environment setup
- Sufficient disk space for saving character files

## Technical Details

This mod creates a complete game activity with advanced features:

- **Custom Game Mode**: Full TeamGameActivity implementation with scoring and respawn systems
- **Dynamic Mesh System**: Real-time swapping of character body parts and textures
- **JSON Export System**: Saves character configurations to the CustomCharacters folder
- **Appearance Registration**: Automatically registers custom characters with the game's appearance system
- **Chat Integration**: Modified chat system to handle character creation commands
- **Multiplayer Sync**: Supports multiple players creating characters simultaneously

## Character Components Available

### Body Parts:
- Head, Hands, Torso, Pelvis
- Upper Arms, Forearms
- Upper Legs, Lower Legs, Toes

### Styles:
- spaz, female, ninja, kronk, mel, pirate
- santa, frosty, bones, bear, penguin
- ali, cyborg, agent, pixie, bunny

### Textures & Colors:
- Multiple color textures and masks
- Custom color selection for main and highlight colors
- Various special textures and patterns

## Export Location

Custom characters are saved to:
`BombSquad/python_directory_user/CustomCharacters/`

## Compatibility

- Works with most other character and appearance mods
- Compatible with multiplayer sessions
- No conflicts with existing character data
- Preserves all original game characters

## Screenshots

<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/9d6263dc-2178-4529-817e-932a26077dea" />
<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/0a319ec2-a1bb-4644-acdb-47f59697b064" />

## Video

https://github.com/user-attachments/assets/05868efe-1c29-4cdd-b4ca-a2b984a38e4f

## Credits

Originally created by HeySmoothy  
Forked by [Less](https://github.com/danigomezdev)
