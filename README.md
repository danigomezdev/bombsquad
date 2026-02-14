# BombSquad Less Server Scripts v1.1.1
#### A handy BombSquad server manager that makes it easy to keep your server up to date with the latest versions — packed with features and ready to use or tweak however you like.

> [!NOTE]
>  ### Running on **Bombsquad 1.7.51 (API 9)**

---

## Quick Start

### What You'll Need

**Option 1: Docker (Recommended)**
- **Docker** and **Docker Compose** installed
- **A VPS** - Amazon Web Services, Google Cloud, Microsoft Azure, or your favorite provider
- **Memory** - 1 GB minimum (2 GB recommended)

**Option 2: Manual Installation**
- **Basic Linux knowledge**
- **A VPS** - Amazon Web Services, Google Cloud, Microsoft Azure, or your favorite provider
- **Linux distro** - Ubuntu 22+ recommended
- **Python 3.13**
- **Memory** - 1 GB minimum (2 GB recommended)

---

## Installation Guide

### 🐳 Docker Installation (Recommended)

#### Step 1: Download Server Files
```bash
git clone --depth=1 https://github.com/danigomezdev/bombsquad
cd bombsquad
```

#### Step 2: Configure Environment Variables
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your settings
nano .env
```

**Environment Variables:**
- `ENVIRONMENT`: `development` or `production`
  - `development`: deploys to `/home/ubuntu/tests/SERVER_NAME`
  - `production`: deploys to `/home/ubuntu/servers/SERVER_NAME`
- `SERVER_NAME`: Folder name on remote server (e.g., `less_east_c1`)
- `PARTY_NAME`: Server name shown in public list
- `PORT`: UDP port (default: 6666)
- `SSH_HOST`: Remote server address
- `SSH_KEY`: Path to SSH private key

#### Step 3: Configure Server Settings
Edit `config.toml` for advanced settings (admins, playlist, team names, etc.)

**Note:** `party_name` and `port` in `config.toml` will be overridden by `.env` values during deployment.

#### Step 4: Deploy to Remote Server
```bash
# Deploy to remote server (uses .env configuration)
./deploy.sh
```

The deployment script will:
- Read configuration from `.env`
- Update `config.toml` with your party name and port
- Deploy to the correct environment path
- Restore original `config.toml` after deployment

#### Step 5: Start the Server

**On Remote Server (SSH into it first):**
```bash
# Navigate to deployed directory
cd /home/ubuntu/tests/less_east_c1  # or /home/ubuntu/servers/less_east_c1 for production

# Start server using interactive menu
./docker-start.sh
```

The script will:
- Check if Docker is installed
- Build image only on first run or when explicitly requested
- Smart restart without rebuild for code changes
- Provide interactive menu for all operations

#### Server Management Commands

**Interactive Menu:**
```bash
./docker-start.sh
```
Options:
1. Start server (builds only if needed)
2. Stop server
3. Restart server (quick reload without rebuild)
4. View logs (live)
5. View logs (last 200 lines)
6. Force rebuild image
7. Server status
8. Enter container shell
9. Stop and remove container

**Direct Docker Commands:**
```bash
# View logs in real-time
docker compose logs -f

# Check server status
docker compose ps

# Restart after config changes
docker compose restart
```

#### 🚀 Multi-Server Deployment

You can deploy multiple servers using different `.env` configurations:

```bash
# Server 1: US East Development
ENVIRONMENT=development
SERVER_NAME=us_east_dev
PARTY_NAME=Test Server US East
PORT=6666

# Server 2: EU West Production
ENVIRONMENT=production
SERVER_NAME=eu_west_prod
PARTY_NAME=Official EU West Server
PORT=6667
```

Simply change `.env` values and run `./deploy.sh` to deploy to different locations

---

### 📦 Manual Installation

#### Step 1: Install Python 3.13
```bash
sudo apt install python3.13 python3.13-dev python3.13-venv python3-pip -y
```

#### Step 2: Update System Packages
```bash
sudo apt update && sudo apt upgrade -y
```

#### Step 3: Start a tmux Session
```bash
tmux new -s server
```

#### Step 4: Download Server Files
```bash
git clone --depth=1 https://github.com/danigomezdev/bombsquad
cd bombsquad
```

#### Step 5: Make Files Executable
```bash
chmod +x bombsquad_server
chmod +x dist/bombsquad_headless
```

#### Step 6: Configure Your Server
Edit `config.toml` in the root directory to set your server name, port, admins, playlist, and team names.

#### Step 7: Start Your Server
```bash
./bombsquad_server
```

<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/ccb85dc6-86ca-45a7-816f-11b86ab23be3" />

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
