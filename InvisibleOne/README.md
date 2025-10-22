# Invisible One for BombSquad

A thrilling game mode where players compete to become and remain the invisible one by touching a flag, gaining invisibility powers while others hunt them down.

## Description

Invisible One is an intense game mode where players battle to control a special flag that grants invisibility. The player who holds the flag becomes completely invisible and must survive for a set amount of time to win, while all other players try to hunt them down and take the flag for themselves.

## Features

- **Dynamic Invisibility System**: Players become completely invisible when touching the flag
- **Visual Transformation**: Invisible players lose all character meshes and textures
- **Audio Stealth**: Invisible players make no sounds (jumping, attacking, impacts, etc.)
- **Strategic Gameplay**: Balance between hunting the invisible player and becoming the target
- **Customizable Settings**: Adjust invisible time, lazy mode, night mode, and more
- **Competitive Scoring**: Teams earn points based on time spent as the invisible one
- **Epic Mode Support**: Slow-motion option for dramatic gameplay

## Installation

1. Download the `InvisibleOne.py` file
2. Place it in your BombSquad mods folder
3. Ensure you have API version 9 or compatible version of BombSquad

## Game Rules

### Objective
- Be the invisible one for the required amount of time to win
- Kill the current invisible one to become the new invisible one
- Work with your team to protect your invisible player

### How to Play
1. The game starts with a flag available in the center
2. Any player can touch the flag to become the invisible one
3. The invisible player becomes completely invisible and silent
4. Other players must hunt and eliminate the invisible player
5. When the invisible player is killed, the killer becomes the new invisible one
6. First team/player to accumulate the required time wins

## Game Settings

### Core Settings:
- **Invisible One Time**: Required time to win (10-30+ seconds)
- **Invisible One is Lazy**: Disables punch, pickup, and bomb for invisible player
- **Night Mode**: Darkens the entire map for enhanced stealth
- **Time Limit**: Overall match duration
- **Respawn Times**: How quickly players respawn after death
- **Epic Mode**: Enables slow-motion effects

## Strategies

### As the Invisible One:
- Use your invisibility to hide and evade hunters
- Move unpredictably to avoid being tracked
- In lazy mode, focus purely on survival
- Use the environment for cover

### As a Hunter:
- Watch for environmental clues (footsteps, dust)
- Listen carefully for any sounds (though invisible players are silent)
- Coordinate with teammates to corner the invisible player
- Control the flag area to quickly become invisible when available

## Visual Effects

When a player becomes invisible:
- All character meshes are removed (head, torso, limbs, etc.)
- Textures and color masks are cleared
- Character style changes to 'cyborg' (minimal visual presence)
- Name tag is hidden
- All sound effects are disabled

## Requirements

- BombSquad version with API 9 support
- Python modding environment setup
- Supported maps: All "keep_away" compatible maps

## Technical Details

This mod extends BombSquad's TeamGameActivity with:

- **Flag-based Role System**: Touch-based role assignment mechanism
- **Material Collision Detection**: Special regions for flag interaction
- **Real-time Character Modification**: Dynamic mesh and texture removal
- **Sound System Override**: Complete audio stealth for invisible players
- **Score Tracking**: Precise time-based scoring system
- **Visual Effects System**: Flash effects and lighting for flag events

## Supported Maps

All maps compatible with "keep_away" game mode including:
- Rampage
- Doom Shroom
- Happy Thoughts
- Step Right Up
- And other keep-away style maps

## Compatibility

- Works with most character mods and skins
- Compatible with power-up systems
- Supports team and free-for-all sessions
- No conflicts with standard game mechanics

## Important Notes

- In "lazy mode", invisible players cannot attack - focus on survival
- Night mode significantly reduces visibility for all players
- The invisible player can still be damaged and killed
- Respawn times affect how quickly hunters can rejoin the chase
- Epic mode creates cinematic slow-motion moments

## Screenshots

<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/1da1f5a7-a67b-44bd-aa6d-86630a49c6f2" />
<img width="433" height="397" alt="Image" src="https://github.com/user-attachments/assets/d12ada45-cd33-4891-98ed-2a01688f6c55" />


## Video

https://github.com/user-attachments/assets/ab99a96f-3178-443f-946c-676deccb4d93

## Credits

Created by the [BombSquad modding community](https://github.com/bombsquad-community)  
Forked by [Less](https://github.com/danigomezdev)
