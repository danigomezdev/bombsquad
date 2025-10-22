# Camera Mapper for BombSquad

A professional camera mapping tool that allows you to create custom camera setups, take screenshots from unique angles, and visualize camera perspectives in 3D space.

## Description

Camera Mapper transforms BombSquad into a photography studio by providing advanced camera control and visualization tools. Create custom camera positions and targets, visualize camera frustums in real-time, and capture stunning screenshots from impossible angles.

## Features

- **3D Camera Visualization**: See exactly what your camera sees with real-time frustum visualization
- **Precise Positioning**: Move the camera object with six degrees of freedom
- **Interactive Controls**: Intuitive button mapping for all camera operations
- **Position Marking**: Set camera position and target points with visual guides
- **Configuration Saving**: Save and load camera setups for repeated use
- **Clipboard Export**: Copy camera commands to paste in developer console
- **Real-time Coordinates**: Live position and coordinate display
- **Cross-platform Controls**: Works with keyboard, gamepad, and touch inputs

## Installation

1. Download the `cameraMapper.py` file
2. Place it in your BombSquad mods folder
3. Ensure you have API version 9 or compatible version of BombSquad

## Usage

### Starting the Camera Tool
1. Launch BombSquad and join any game
2. Open the in-game menu (Esc key or menu button)
3. Click the "Camera" button in the menu
4. Select "3D Camera mapper" to spawn the camera object

### Camera Controls
- **Jump Button**: Move camera down (vertical movement)
- **Pick Up Button**: Move camera up (vertical movement)
- **Left/Right**: Move camera horizontally
- **Punch Button**: Mark camera position and target points
- **Bomb Button**: Destroy camera and apply/abort setup

### Camera Setup Process
1. **Mark Position**: Press Punch to set the camera's position (blue dot)
2. **Mark Target**: Move to desired look-at point and press Punch again
3. **Apply**: Press Bomb to activate the camera setup
4. **Cancel**: Press Bomb before completing setup to abort

## Advanced Features

### Configuration Management
- **Last Mapped Config**: Load your previous camera setup
- **Last Dev Command**: Copy Python commands for developer console
- **Reset Settings**: Return to default camera behavior

### Visual Guides
- **Frustum Visualization**: See the camera's field of view as a pyramid
- **Position Markers**: Blue dots show camera position and target
- **Coordinate Display**: Real-time XYZ coordinates overlay
- **Control HUD**: On-screen button guides with color feedback

## Requirements

- BombSquad version with API 9 support
- Python modding environment setup
- Host privileges for mapping (loading works for all players)

## Technical Details

This mod creates a comprehensive camera system:

- **Camera Object**: Interactive TNT prop that serves as the camera controller
- **Material System**: Custom physics materials for smooth movement
- **Node Hierarchy**: Complex node structure for visuals and calculations
- **Animation System**: Smooth transitions and visual feedback
- **UI Integration**: Seamless menu integration and overlay system
- **Configuration Storage**: Persistent storage of camera setups

## Use Cases

- **Cinematic Screenshots**: Capture professional-looking game moments
- **Map Exploration**: View levels from unique perspectives
- **Content Creation**: Create videos and promotional material
- **Game Development**: Test and visualize level designs
- **Educational Purposes**: Understand 3D camera mathematics

## Control Overlay

The mod provides a comprehensive HUD showing:
- Current position coordinates (X, Y, Z)
- Active control buttons with visual feedback
- Movement direction indicator
- Operation status and instructions

## Export Features

### Developer Console Commands
The mod can generate Python code for the developer console:
```python
from _babase import set_camera_manual, set_camera_target, set_camera_position
set_camera_manual(True)
set_camera_position((x1, y1, z1))
set_camera_target((x2, y2, z2))
```

## Compatibility

- Works in all game modes
- Compatible with most other visual mods
- Requires host privileges for mapping operations
- All players can load existing configurations

## Important Notes

- Camera mapping requires host privileges
- The camera object can be destroyed by game physics
- Some game modes may override camera settings
- Export commands work in the developer console

## Screenshots
<img width="2408" height="1080" alt="Image" src="https://github.com/user-attachments/assets/05831378-00b9-4f49-8844-1ba082d0dd9b" />

## Video
https://github.com/user-attachments/assets/1f9ee924-0438-4424-aeee-75a805e44bac

## Credits

Created by the [[BrotherBoard](https://github.com/BrotherBoard)](https://github.com/BrotherBoard)  
Forked by [Less](https://github.com/danigomezdev)
