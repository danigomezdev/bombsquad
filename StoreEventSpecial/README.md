# Events Special Store for BombSquad

A mod that unlocks special seasonal characters and exclusive content in the store year-round.

## Description

Events Special Store modifies the in-game store to make seasonal and event-exclusive characters and minigames available for purchase at any time. No longer wait for specific holidays or events to access your favorite special content!

## Features

- **Unlocks Seasonal Characters**: Makes seasonal characters available permanently:
  - Bunny (Easter character)
  - Taobao Mascot (special event character) 
  - Santa (Christmas character)
- **Unlocks Special Minigames**: Adds exclusive minigames to the store:
  - Easter Egg Hunt minigame
- **Permanent Access**: Buy and use special content regardless of the current season
- **Seamless Integration**: Automatically integrates with the existing store layout
- **No Gameplay Changes**: Doesn't alter gameplay mechanics, only unlocks purchasing options

## Installation

1. Download the `eventsSpecialStore.py` file
2. Place it in your BombSquad mods folder
3. Ensure you have API version 9 or compatible version of BombSquad

## Usage

1. Launch BombSquad with the mod installed
2. Navigate to the store as usual
3. You'll now see additional characters and minigames available for purchase:
   - **Characters Tab**: Bunny, Taobao Mascot, and Santa characters
   - **Minigames Tab**: Easter Egg Hunt minigame
4. Purchase these items using in-game currency like any other store item

## Requirements

- BombSquad version with API 9 support
- Python modding environment setup
- Sufficient in-game currency to purchase unlocked items

## Technical Details

This mod uses function replacement to modify the store layout:
- Replaces `bui.app.classic.store.get_store_layout` method
- Adds special characters to the characters section
- Adds special minigames to the minigames section
- Maintains compatibility with original store functionality
- Uses type hints for better code clarity

## Unlocked Content

### Characters:
- **Bunny**: Easter-themed character normally available during spring events
- **Taobao Mascot**: Special promotional character
- **Santa**: Christmas-themed character normally available during winter holidays

### Minigames:
- **Easter Egg Hunt**: Seasonal minigame typically available during Easter events

## Compatibility

- Works with most other store and UI mods
- Compatible with all game modes
- No conflicts with existing save data or profiles
- Maintains original pricing and purchase mechanics

## Screenshots

<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/adb62254-7fe4-4bbf-bac7-d8c982a2a2fe" />

## Credits

Created by the [BombSquad modding community](https://github.com/bombsquad-community)  
Forked by [Less](https://github.com/danigomezdev)
