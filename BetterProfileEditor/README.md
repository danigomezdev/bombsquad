# Better Profile Editor for BombSquad

A mod that enhances the profile editor in BombSquad with an advanced live preview system.

## Description

Better Profile Editor replaces the standard profile editor with an improved version that features a live character preview. As you make changes to your profile's character, color, and highlight settings, you can see the character update in real-time within a 3D environment.

## Features

- Live character preview that updates immediately when changing profile settings
- 3D environment with proper lighting and physics
- Real-time visual feedback for character selections
- Maintains all original profile editor functionality
- Seamless integration with the main menu system
- Support for all character types and customizations

## Installation

1. Download the `betterProfileEditor.py` file
2. Place it in your BombSquad mods folder
3. Ensure you have API version 9 or compatible version of BombSquad

## Usage

1. Launch BombSquad with the mod installed
2. Navigate to the profile section as usual
3. When creating or editing a profile, you'll see the enhanced editor with live preview
4. The character in the preview area will update automatically as you change settings

## Requirements

- BombSquad version with API 9 support
- Python modding environment setup

## Technical Details

This mod replaces the standard `EditProfileWindow` and `ProfileBrowserWindow` classes with enhanced versions that include:
- Custom `BetterProfileActivity` for the 3D preview environment
- `ProfileSpaz` class for the preview character with proper bounds handling
- Modified UI elements that sync with the live preview

## Screenshots

<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/6d887c84-2776-4444-a61c-35fb22beea8a" />

<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/18d1d0de-42be-4201-adb1-975b9120780e" />

<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/ccf2c60c-e3cc-487f-ad0d-a2426c56ed5e" />


## Video

https://github.com/user-attachments/assets/5e3d54ad-ee35-4a6a-9049-fdfac0b29a37

## Credits

Created by the [BombSquad modding community](https://github.com/bombsquad-community)  
Forked by [Less](https://github.com/danigomezdev)
