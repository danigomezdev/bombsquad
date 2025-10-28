# BombSquad Less Server Scripts v1.1.1
#### A handy BombSquad server manager that makes it easy to keep your server up to date with the latest versions — packed with features and ready to use or tweak however you like.

> [!NOTE]
>  ### Running on **Bombsquad 1.7.51 (API 9)**

---

## Quick Start

### What You'll Need

- **Basic Linux knowledge**
- **A VPS** - Amazon Web Services, Google Cloud, Microsoft Azure, or your favorite provider
- **Linux distro** - Ubuntu 22+ recommended
- **Python 3.13**
- **Memory** - 1 GB minimum (2 GB recommended)

---

## Installation Guide

### Step 1: Install Python 3.13
```
sudo apt install python3.13 python3.13-dev python3.13-venv python3-pip -y
```

### Step 2: Update System Packages
```
sudo apt update && sudo apt upgrade -y
```

### Step 3: Start a tmux Session
```
tmux new -s server
```

### Step 4: Download Server Files
```
git clone --depth=1 https://github.com/danigomezdev/bombsquad
```

### Step 5: Make Files Executable
```
chmod 777 bombsquad_server
chmod 777 dist/bombsquad_headless
```

### Step 6: Configure Your Server
Edit `config.yaml` in the root directory to set your server name, port, admins, playlist, and team names.

---

## Starting Your Server

```
./bombsquad_server.py
```

<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/9cd5cb30-93c9-4f80-8477-f4b2d389b2d4" />

---

## Advanced Configuration

### Server Settings
Open `dist/ba_root/mods/setting.json` to customize your server settings.

<!--
**Useful Resources:**
- [How to edit settings.json](https://github.com/imayushsaini/Bombsquad-Ballistica-Modded-Server/wiki/Server-Settings)
- [Available chat commands](https://github.com/imayushsaini/Bombsquad-Ballistica-Modded-Server/wiki/Chat-commands)
-->

### Adding Yourself as Owner
1. Open `dist/ba_root/mods/playersData/roles.json`
2. Add your Pb-id to the owner list
3. Restart your server

### Player Management
Manage your community in `dist/ba_root/mods/playersData/profiles.json`:
- Ban players
- Mute players
- Disable kick votes

---

## Features

### Ranking & Social Systems
- Advanced Rank System with progression tracking
- Live Leaderboard displaying top 5 players
- Team Chat using comma prefix for team-only messages
- In-game Popup Chat using dot prefix for prominent messages

### Gameplay Enhancements
- Character Chooser allowing players to select characters when joining
- Custom Characters support with easy loading from character maker
- Floater system for enhanced visual effects
- Ping checking using /ping command to monitor connection quality

### Server Management
- V2 Account System with cloud console for remote management
- Flexible Role System supporting unlimited custom roles with specific commands
- Rejoin Cooldown to prevent spam rejoining
- Automatic Stats Reset on configured schedule

### Moderation & Voting
- Custom Voting System activated by end, sm, nv, dv commands
- Player ID hiding with /hideid and /showid commands
- Automatic update checking to keep server current
- Spectator control to hide player specs from clients

### Customization Options
- Configurable Server Host Names
- Centralized Settings in settings.json file (no coding required)
- Easy role management with custom tags and permissions

---

## Screenshots

![Gameplay 1](https://github.com/user-attachments/assets/4c8024c0-4562-41b6-83a5-f493a960245f)

![Gameplay 2](https://github.com/user-attachments/assets/5b95068c-1286-4aa7-914e-a8eb760ebf24)

- ### More characters

<div align="center">

| | |
|:---:|:---:|
| <img src="https://github.com/user-attachments/assets/0b34cf2f-27d1-4998-b04e-196abea0c703" width="100%"> | <img src="https://github.com/user-attachments/assets/7728892e-f71a-40f8-9ce4-cefb3008c1d2" width="100%"> |
| <img src="https://github.com/user-attachments/assets/3556ac0a-8885-4945-bc87-3ea699ca4f58" width="100%"> | <img src="https://github.com/user-attachments/assets/a03d32c7-953d-47a8-864c-3e299e551716" width="100%"> |

</div>

---

## Videos


- ###  Effects

https://github.com/user-attachments/assets/a03445ed-0081-4cf6-a24a-335c49ef3f02

---

## Credits

**Original Creation:** [Bombsquad Community](https://github.com/bombsquad-community/)  
**Maintained by:** [Less](https://github.com/danigomezdev)
