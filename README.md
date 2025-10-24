# Mod Manager for BombSquad

A powerful mod management system that allows you to easily install, update, and delete multiple mods from a remote repository.

## Description

Mod Manager is a comprehensive mod management solution for BombSquad that provides a centralized interface for discovering, installing, and managing community-created mods. This mod acts as a package manager for your BombSquad experience, featuring automatic updates, dependency handling, and a user-friendly interface.

## Features

- **One-Click Installation**: Install mods with a single click from the integrated repository
- **Automatic Updates**: Keep your mods up-to-date with automatic version checking
- **Mod Management**: Easily enable, disable, or uninstall mods through a clean interface
- **Repository Support**: Access curated mod collections from community repositories
- **Search & Filter**: Find mods quickly with search functionality and category filtering
- **Settings Integration**: Access mod settings directly from the manager interface
- **Update Notifications**: Get notified when new mods or updates are available
- **Multi-language Support**: Spanish and English interface support
- **Safety Features**: MD5 checksum verification for secure downloads

## Installation

### Automatic Installation (Recommended)
1. Download the latest `ModManager.py` file
2. Place it in your BombSquad mods folder:
   - Windows: `%appdata%/BombSquad/mods/`
   - Linux: `~/.bombsquad/mods`
   - macOS: `~/Library/Application Support/BombSquad/mods/`
   - Android: `/storage/sdcard0/Android/data/net.froemling.bombsquad/files/mods/`
3. Restart BombSquad

### Manual Installation
1. Download the mod file from the repository
2. Copy to your BombSquad mods directory
3. Ensure you have API version 9 or compatible version of BombSquad
4. Launch the game

## Usage

### Accessing Mod Manager
1. Launch BombSquad with the mod installed
2. Go to Settings → Mod Manager
3. The mod manager interface will open automatically

### Basic Navigation
- **Browse Mods**: View all available mods in the main list
- **Search**: Use the search bar to find specific mods
- **Categories**: Filter mods by category using the category dropdown
- **Mod Details**: Click on any mod to view detailed information and actions

### Mod Actions
- **Install**: Download and install a new mod
- **Update**: Update an installed mod to the latest version
- **Enable/Disable**: Toggle mod functionality without uninstalling
- **Uninstall**: Remove a mod completely
- **Settings**: Access mod-specific configuration (if available)

### Color Coding System
- **🟢 GREEN**: Mod is installed, enabled, and up-to-date
- **🔵 BLUE**: Update available for installed mod
- **🟠 ORANGE**: Mod is installed but currently disabled
- **🔴 RED**: Mod was installed manually (not via Mod Manager)
- **⚫ GRAY**: Mod is not installed

## Configuration

### Automatic Settings
Access mod manager settings through the gear icon:
- **Auto Update Mod Manager**: Automatically check for manager updates
- **Auto Update Mods**: Automatically update installed mods
- **Auto Enable After Installation**: Enable mods immediately after installation
- **Notify New Mods**: Show notifications when new mods are available

### Manual Configuration
Advanced users can modify settings in the BombSquad config file under the "Mod Manager" section.

## Repository System

### Default Repository
The mod comes pre-configured with a curated repository of community-approved mods featuring:
- Quality-tested mods
- Regular updates
- Compatibility checking
- Safe downloads

### Custom Sources
Advanced users can add custom mod repositories:
1. Open Mod Manager settings
2. Navigate to custom sources
3. Add repository URLs for additional mod collections

## Technical Details

### Architecture
- **Plugin System**: Modular architecture for easy extensibility
- **Async Operations**: Non-blocking downloads and updates
- **Caching System**: Efficient network usage with smart caching
- **Error Handling**: Robust error recovery and user feedback

### Security Features
- **MD5 Verification**: Ensures file integrity during downloads
- **Source Validation**: Validates mod sources before installation
- **Network Safety**: Secure HTTP handling with proper headers

### Compatibility
- **API Version 9**: Designed for BombSquad's latest modding API
- **Cross-Platform**: Works on Windows, Linux, and macOS
- **Multi-language**: Supports English and Spanish interfaces

## Requirements

- BombSquad version with API 9 support
- Internet connection for mod browsing and downloads
- Python modding environment setup
- Approximately 10MB of free space for mod storage

## Troubleshooting

### Common Issues

**Mods Not Appearing**
- Check your internet connection
- Verify the repository URL is accessible
- Restart BombSquad and check again

**Installation Failures**
- Ensure sufficient disk space
- Check file permissions in mods directory
- Verify MD5 checksums aren't failing

**Performance Issues**
- Disable auto-update features if needed
- Clear mod manager cache through settings
- Reduce number of simultaneously updating mods

**Settings Not Saving**
- Verify write permissions in config directory
- Check for corrupted configuration files
- Restart game to reset configuration

### Network Troubleshooting
The mod includes DNS workarounds for common ISP blocks. If you experience connection issues:
1. The mod automatically attempts alternative DNS resolution
2. Manual network configuration may be required in restricted environments
3. Check firewall settings for BombSquad network access

## Features in Detail

### Smart Update System
- Background update checks
- Version compatibility validation
- Batch update capabilities
- Update rollback protection

### User Interface
- Intuitive category browsing
- Search with fuzzy matching
- Detailed mod information panels
- Visual status indicators
- Responsive design for all screen sizes

### Mod Management
- Dependency tracking
- Conflict detection
- Storage optimization
- Backup and restore functionality

## Community Features

### Discord Integration
- Quick access to community Discord server
- Direct support channels
- Mod discussion forums
- Update announcements

### GitHub Repository
- Open source development
- Issue tracking
- Feature requests
- Community contributions

## Important Notes

- Always backup your saves before installing new mods
- Some mods may conflict with each other
- Disable mods individually to isolate issues
- Report problematic mods through the appropriate channels
- The mod manager only manages mods installed through its system

## Screenshots

<img width="524" height="386" alt="Image" src="https://github.com/user-attachments/assets/fe199c0a-7b2b-442b-aae1-41616cbe19a2" />
<img width="525" height="418" alt="Image" src="https://github.com/user-attachments/assets/a39dfbdc-5618-49cc-94fd-dfc20d7841bb" />

## Video Tutorial

https://github.com/user-attachments/assets/cfd88288-e5a8-42bf-a3a7-765b4aa2d935

## Credits

Created by the [BombSquad modding community](https://github.com/bombsquad-community)  
Forked by [Less](https://github.com/danigomezdev)

### Repository
- **Main Repository**: https://github.com/danigomezdev/bombsquad/tree/modmanager
- **Issue Tracker**: https://github.com/danigomezdev/bombsquad/issues
- **Discord Community**: https://discord.gg/q5GdnP85Ky

---

**Version**: 1.1.2  
**Last Updated**: January 2024  
**Compatibility**: BombSquad API 9+  
**Support**: Community Discord Server
