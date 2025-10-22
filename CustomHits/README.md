# Custom Hits for BombSquad

A dynamic visual feedback mod that shows custom reactions and effects when you hit players, with escalating responses based on damage dealt.

## Description

Custom Hits enhances BombSquad's combat feedback by displaying custom text messages and particle effects whenever you successfully hit other players. The mod provides escalating visual rewards that correspond to the amount of damage dealt, making combat more satisfying and visually engaging.

## Features

- **Damage-Based Reactions**: Different messages and effects based on damage amounts
- **Escalating Visual Feedback**: More impressive effects for higher damage hits
- **Floating Text Display**: Custom animated text that floats up from hit positions
- **Particle Effects**: Unique particle effects for different damage tiers
- **Real-time Feedback**: Instant visual responses to successful attacks
- **Non-Intrusive Design**: Enhances gameplay without disrupting the experience
- **Six Damage Tiers**: Progressive system from light taps to massive hits

## Installation

1. Download the `CustomHits.py` file
2. Place it in your BombSquad mods folder
3. Ensure you have API version 9 or compatible version of BombSquad

## Usage

1. Launch BombSquad with the mod installed
2. Join any game mode with combat
3. Hit other players to see custom reactions:
   - **Light hits** (<200 damage): "XD" with rock particles
   - **Medium hits** (<500 damage): "LOL" with slime particles  
   - **Strong hits** (<800 damage): "NICE" with splinter particles
   - **Heavy hits** (<1000 damage): "UPPS" with ice particles
   - **Massive hits** (1000+ damage): "ONE PUNCH" with spark particles

## Visual Effects

### Text Animations:
- Smooth floating animation from hit position
- Color-coded messages for different damage levels
- Fade-out effect over 2 seconds
- Scale animations for emphasis

### Particle Effects:
- **Rock Particles**: Small rock chunks for light impacts
- **Slime Particles**: Green slime splatters for medium hits
- **Splinter Particles**: Wood splinters for strong impacts
- **Ice Particles**: Ice crystal shatters for heavy hits
- **Spark Particles**: Dramatic spark bursts for massive damage
- **Metal Particles**: Metallic fragments for various hits

## Damage Tiers

| Damage Range | Message | Color | Effect Type |
|--------------|---------|-------|-------------|
| <200 | XD | Green (0,1,0) | Rock |
| 200-499 | LOL | Cyan (0,1,1) | Slime |
| 500-799 | NICE | Purple (0.8,0.4,1) | Splinter |
| 800-999 | UPPS | Yellow (1,1,0) | Ice |
| 1000+ | ONE PUNCH | Red (1,0,0) | Spark |

## Requirements

- BombSquad version with API 9 support
- Python modding environment setup

## Technical Details

This mod extends the Spaz class with enhanced hit feedback:

- **on_punched Override**: Modifies the existing punch handler to add custom effects
- **Node-based Text System**: Creates temporary text nodes with smooth animations
- **Particle Effect System**: Uses bascenev1.emitfx for various particle types
- **Damage Calculation**: Reads damage values to determine appropriate reactions
- **Position Tracking**: Uses exact hit positions for accurate effect placement

## Animation System

The mod features sophisticated animations:
- **Text Float**: Smooth upward movement over 2 seconds
- **Fade Out**: Gradual opacity reduction for clean disappearance
- **Scale Animation**: Dynamic text scaling for emphasis
- **Automatic Cleanup**: Automatic node deletion after animations complete

## Compatibility

- Works with all game modes featuring combat
- Compatible with most character and weapon mods
- No conflicts with existing damage systems
- Works in both singleplayer and multiplayer

## Customization

You can easily modify the mod by changing the constants:
- Edit message text and colors
- Adjust damage thresholds
- Change particle effect types and parameters
- Modify animation timing and styles

## Performance

- Minimal performance impact
- Effects automatically clean up after completion
- Uses BombSquad's built-in particle systems
- No persistent objects or memory leaks

## Use Cases

- **Casual Play**: Adds fun visual feedback to regular gameplay
- **Content Creation**: Creates more dynamic footage for videos and streams
- **Competitive Play**: Provides immediate visual confirmation of hit effectiveness
- **Training**: Helps players understand damage values and hit strength

## Video

https://github.com/user-attachments/assets/997ccbb8-8fda-442f-afc0-df314391200e

## Credits

Created by the [BombSquad modding community](https://github.com/bombsquad-community)  
Forked by [Less](https://github.com/danigomezdev)
