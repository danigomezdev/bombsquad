# Discord Rich Presence for BombSquad

A comprehensive Discord integration that displays your BombSquad gameplay activity, server information, and allows friends to join your games directly from Discord.

## Description

Discord Rich Presence provides deep integration between BombSquad and Discord, showing real-time game information in your Discord profile. See what maps your friends are playing, view server details, and even join their games directly through Discord with one click.

## Features

- **Real-time Status Updates**: Shows current game mode, map, and activity
- **Server Information Display**: Shows player counts and server names
- **Direct Join Functionality**: Join friends' games directly from Discord
- **Cross-platform Support**: Works on Windows, Linux, Mac, and Android
- **Detailed Game Information**: Shows specific game stats like survival counts, scores, and timers
- **Custom Images**: Displays map previews and game mode icons
- **AFK Detection**: Automatically updates status when inactive
- **Secure Authentication**: Optional Discord login for enhanced features
- **Multi-language Support**: Includes special "Gibberish" language mode

## Installation

1. Download the `DiscordRichPresence.py` file
2. Place it in your BombSquad mods folder
3. Ensure you have API version 9 or compatible version of BombSquad
4. Restart BombSquad

### Platform-specific Notes:
- **Windows/Linux/Mac**: Automatically installs required pypresence library
- **Android**: Uses lightweight custom implementation
- **All Platforms**: No additional software required for basic functionality

## Usage

### Basic Usage
1. Launch BombSquad with the mod installed
2. Your Discord status will automatically update with:
   - Current game/menu you're in
   - Map name and preview image
   - Player count and server information
   - Platform and game version

### Advanced Features

#### Joining Games via Discord
1. Friends can see your game in Discord
2. They can click "Ask to Join" to request invitation
3. You'll receive a notification in-game
4. Approve to let them join your session

#### Discord Login (Optional)
1. Access settings through mods menu
2. Log in with Discord credentials for enhanced features
3. Supports 2FA and backup codes
4. **Warning**: Use at your own risk - may violate Discord TOS

## Display Information

### Activity Types Shown:
- **Main Menu**: When browsing menus or lobbies
- **Game Sessions**: Current game mode and map
- **Local Games**: "Local" status for offline sessions
- **Online Servers**: Server name and player count
- **Replay Viewer**: When watching replays
- **Ranking Screens**: When viewing results

### Game-specific Stats:
- **Elimination**: Players remaining
- **The Last Stand**: Current score
- **Meteor Shower**: Survival time
- **Football**: Current score
- **Easter Egg Hunt**: Eggs collected
- **And more**: Various game-specific statistics

## Requirements

- BombSquad version with API 9 support
- Discord desktop app running (for non-Android platforms)
- Internet connection for server information and images

## Technical Details

### Platform Implementation:
- **Non-Android**: Uses pypresence library with full RPC features
- **Android**: Custom HTTP server implementation for mobile compatibility

### Features Include:
- **Activity Tracking**: Monitors game state changes
- **Image Assets**: Over 50 custom images for maps and modes
- **Join Secrets**: Encrypted server connection information
- **Event Handling**: Manages join requests and notifications
- **Configuration**: Persistent settings storage

### Security Features:
- Encrypted token storage for Discord login
- Secure join secret generation
- Local HTTP server for Android data sharing
- Permission-based access controls

## Compatibility

- **Discord Versions**: Works with most modern Discord versions
- **BombSquad Builds**: Compatible with build 20884+
- **Cross-platform**: Server information shared across all platforms
- **Mod Compatibility**: Works alongside most other mods

## Settings and Customization

Accessible through the mod settings menu:
- **Discord Login**: Optional account linking
- **Status Updates**: Control what information is shared
- **Join Permissions**: Manage who can join your games
- **Privacy Controls**: Limit visible information

## Troubleshooting

### Common Issues:
- **Status not updating**: Ensure Discord is running (desktop)
- **Join not working**: Check firewall and network settings
- **Images missing**: Some custom maps may not have previews
- **Login failures**: Verify credentials and 2FA codes

### Android Specific:
- Uses local HTTP server on port 26000
- May require network permissions
- Limited to basic status information

## Privacy and Security

- **No data collection**: All information stays local
- **Optional features**: Discord login is completely optional
- **Transparent operation**: Open source code for verification
- **User control**: Can disable specific features

## Screenshots

<img width="286" height="508" alt="Image" src="https://github.com/user-attachments/assets/ef14a56a-a8f8-4219-ace1-481339500ced" />

<img width="286" height="508" alt="Image" src="https://github.com/user-attachments/assets/dc49b967-4f3c-46c9-a973-08ffdae9c292" />

## Video

*Demonstration of real-time status updates and join functionality(This will remain pending...)*

## Credits

Created by the @brostos & @Dliwk
Forked by [Less](https://github.com/danigomezdev)
