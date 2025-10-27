# Server Finder for BombSquad

An advanced server discovery and friend management system that helps you find the best BombSquad servers and track your friends across different game sessions.

## Description

Server Finder is a comprehensive mod that revolutionizes how you find and connect to BombSquad servers. It provides real-time server discovery, latency testing, automatic server cycling, and a sophisticated friend tracking system that shows when your friends are playing on public servers.

## Features

- **Real-time Server Discovery**: Find and ping all available public BombSquad servers
- **Latency-Based Sorting**: Automatically sort servers by ping for optimal connection quality
- **Smart Server Cycling**: Automatically cycle through top servers to gather player information
- **Friend Tracking System**: Track when your friends are playing on public servers
- **One-Click Connection**: Connect to any server directly from the interface
- **Best Friends List**: Maintain a personal friends list with automatic online detection
- **Server Information Display**: View detailed server info including player roster and connection details
- **Multi-language Support**: Spanish and English interface with automatic language detection
- **Persistent Data**: Friend lists and preferences saved between sessions

## Installation

1. Download the `serverFinder.py` file
2. Place it in your BombSquad mods folder
3. Ensure you have API version 9 or compatible version of BombSquad
4. Restart BombSquad

## Usage

### Accessing the Server Finder
1. Launch BombSquad with the mod installed
2. Open the party window (default Tab key)
3. Click the new "Buscar" (Search) button in the interface
4. The Server Finder window will open with all available features

### Finding Servers
1. Click "Buscar" to search for all available public servers
2. The mod will ping each server and display latency information
3. Servers are automatically sorted by ping (lowest first)
4. View player counts and server names in the results

### Server Cycling
1. Set the server limit using the "Límite de Servidores" field
2. Click "Ciclar" to automatically cycle through the best servers
3. The mod will briefly connect to each server to gather player information
4. Player data is collected and displayed in the interface

### Friend Management
1. Click the friends button (users icon) to open the friends panel
2. Add friends manually using the "Agregar Manualmente" feature
3. View which friends are currently online in public servers
4. Remove friends from your list as needed
5. Online friends are automatically detected during server cycling

### Connecting to Servers
1. Select any server or player from the lists
2. View detailed connection information
3. Click "Conectar" to join the server directly
4. For friends, connect to the server they're currently playing on

## Interface Sections

### Main Panel
- **Server Search**: Find and ping all public servers
- **Server Cycling**: Automatically cycle through top servers
- **Server Limit**: Set maximum number of servers to cycle
- **Player List**: Display all players found during cycling
- **Server Info**: Detailed information for selected servers/players

### Friends Panel
- **Friends List**: All saved friends with online status
- **Online Friends**: Friends currently playing on public servers
- **Manual Addition**: Add friends by name
- **Friend Management**: Remove friends from your list
- **Connection Options**: Quick connect to friends' servers

## Technical Details

This mod implements several advanced systems:

- **Server Discovery**: Uses BombSquad's public party query system
- **Latency Testing**: Custom UDP ping implementation for accurate latency measurement
- **Multi-threading**: Simultaneous server pinging for faster results
- **Data Persistence**: Friend lists stored in `BestFriends.txt` file
- **UI Integration**: Seamless integration with BombSquad's existing party interface
- **Connection Management**: Automatic server cycling and connection handling

## Friend Tracking System

### How It Works:
1. During server cycling, player rosters are collected from each server
2. The system checks if any players match your friends list
3. Online friends are displayed in the "En linea" section
4. You can see which server they're playing on and connect directly

### Features:
- Real-time online status detection
- Server information for online friends
- One-click connection to friends' servers
- Persistent friend list storage

## Server Cycling Process

1. **Server Selection**: Top servers are selected based on ping
2. **Automatic Connection**: The mod briefly connects to each server
3. **Data Collection**: Player rosters and server info are gathered
4. **Friend Detection**: System checks for friends in each server
5. **Interface Update**: All collected data is displayed

## Requirements

- BombSquad version with API 9 support
- Python modding environment setup
- Internet connection for server discovery
- Public server access for friend tracking

## Customization

### Server Limits:
- Adjust how many servers to cycle through
- Balance between comprehensive data and cycling time
- Default limit: 25 servers

### Friend Management:
- Add friends manually by name
- Remove friends as needed
- Automatic online status detection
- Persistent storage between sessions

## Compatibility

- Works with all public BombSquad servers
- Compatible with most other UI and gameplay mods
- Supports both IPv4 and IPv6 connections
- Works in all game modes

## Performance Considerations

- **Server Cycling**: May take 1-3 minutes depending on server limit
- **Network Usage**: Moderate bandwidth during server discovery
- **Memory Usage**: Efficient data storage and management
- **Processing**: Multi-threaded design minimizes impact on gameplay

## Use Cases

### For Regular Players:
- Find servers with good connection quality
- Track when friends are playing
- Quick connection to popular servers
- Discover new communities and players

### For Community Managers:
- Monitor server populations
- Track member activity across servers
- Build and maintain friend networks
- Discover new servers and communities

### For Server Hosts:
- See how your server compares in latency
- Monitor player traffic patterns
- Understand server discovery patterns

## Important Notes

- Friend tracking only works for players on public servers with available slots
- Server cycling involves brief connections but doesn't join games
- Some servers may have anti-bot measures that limit cycling
- Friend detection requires the player to be online during cycling
- Manual friend addition requires exact player names

## Troubleshooting

### Common Issues:
- **No servers found**: Check internet connection and try again
- **Friends not detected**: Ensure friends are on public servers during cycling
- **Connection failures**: Some servers may reject automatic connections
- **Performance issues**: Reduce server limit for faster cycling

### Data Management:
- Friend list stored in `python_directory_user/BestFriends.txt`
- Server data is temporary and resets each session
- Configuration persists between game launches

## Screenshots

<img width="764" height="475" alt="Image" src="https://github.com/user-attachments/assets/37f1a0bf-d5e7-43a0-bfa2-db405cbda927" />

## Video

https://github.com/user-attachments/assets/f64fd5dd-88e6-430d-8e02-a0fb0fcad1af

## Credits

Created by the [BrotherBoard](https://github.com/BrotherBoard)  
Forked by [Less](https://github.com/danigomezdev)
